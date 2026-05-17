import pytest
import pytest_asyncio
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession, _SESSION
from pytest_mock import MockerFixture

from app.libs.beanie_odm_ext.mongo_db import MongoDB
from app.libs.beanie_odm_ext.tests.fixtures import service
from app.libs.beanie_odm_ext.tests.fixtures.models import Product, Category
from app.libs.beanie_odm_ext.transaction import Atomic
from app.libs.managment.conf import settings
from app.utils.mongo_conf import transform_settings_to_mongo


class TestServicesIntegration:
    @pytest.fixture(autouse=True)
    async def cleanup_mongo(self):
        """
        Ensure the collections are empty before and after the CLI runs.
        """

        yield

        # 2. Post-test cleanup
        await Category.get_pymongo_collection().delete_many({})
        await Product.get_pymongo_collection().delete_many({})

    @pytest_asyncio.fixture(scope="class", autouse=True)
    async def init_beanie(self):
        await MongoDB.init_beanie_db(
            db_name=settings.MONGO_DB_NAME,
            mongo_connection_params=transform_settings_to_mongo(settings),
            models_list=[Category, Product],
        )
        yield

    @pytest.mark.asyncio
    async def test_service_decorator_success(self, mocker: MockerFixture):
        spy_commit = mocker.spy(Atomic, "_commit_with_retry")

        product = await service.create_product()

        assert product is not None
        assert spy_commit.call_count == 1
        assert await Product.count() == 1

    @pytest.mark.asyncio
    async def test_service_decorator_rollback(self, mocker: MockerFixture):
        spy_abort = mocker.spy(AsyncClientSession, "abort_transaction")

        with pytest.raises(Exception, match="Product creation failed"):
            await service.create_product_with_error()

        assert spy_abort.called
        assert await Product.count() == 0

    @pytest.mark.asyncio
    async def test_service_context_success(self, mocker: MockerFixture):
        spy_atomic = mocker.spy(Atomic, "__aenter__")

        await service.create_product_using_context()

        assert spy_atomic.called
        assert await Product.find_one({"name": "product_with_service_context"}) is not None

    @pytest.mark.asyncio
    async def test_service_context_rollback(self, mocker: MockerFixture):
        with pytest.raises(Exception, match="Product creation failed"):
            await service.create_product_using_context_error()

        assert await Product.count() == 0

    @pytest.mark.asyncio
    async def test_decorator_params_propagation(self, mocker: MockerFixture, init_beanie) -> None:
        # 1. Spy on PyMongo Async's core methods
        # We spy on the classes to catch the parameters at the "metal"
        spy_start_session = mocker.spy(AsyncMongoClient, "start_session")
        spy_start_transaction = mocker.spy(AsyncClientSession, "start_transaction")

        # 2. Act: Call the decorated function
        # Note: We are testing the successful flow here,
        # but the logic remains the same for error cases.
        await service.create_product_with_params()

        # 3. Assert Session Parameters (from @auto_session)
        assert spy_start_session.called
        _, session_kwargs = spy_start_session.call_args
        assert (
            session_kwargs.get("causal_consistency") is True
        ), "causal_consistency=True was not passed from the decorator to start_session!"

        # 4. Assert Transaction Parameters (from @transaction.atomic)
        assert spy_start_transaction.called
        _, trans_kwargs = spy_start_transaction.call_args

        rc = trans_kwargs.get("read_concern")
        assert rc is not None
        assert rc.level == "majority", f"Expected ReadConcern 'majority', but got '{rc.level if rc else 'None'}'"

        # 5. DB Verification (Sanity Check)
        count = await Product.find_all().count()
        assert count == 1

    @pytest.mark.asyncio
    async def test_context_params_propagation(self, mocker: MockerFixture, init_beanie) -> None:
        # 1. Spy on PyMongo Async's core methods
        # We spy on the classes to catch the parameters at the "metal"
        spy_start_session = mocker.spy(AsyncMongoClient, "start_session")
        spy_start_transaction = mocker.spy(AsyncClientSession, "start_transaction")

        # 2. Act: Call the decorated function
        # Note: We are testing the successful flow here,
        # but the logic remains the same for error cases.
        await service.create_product_with_params_context()

        # 3. Assert Session Parameters (from @auto_session)
        assert spy_start_session.called
        _, session_kwargs = spy_start_session.call_args
        assert (
            session_kwargs.get("causal_consistency") is True
        ), "causal_consistency=True was not passed from the decorator to start_session!"

        # 4. Assert Transaction Parameters (from @transaction.atomic)
        assert spy_start_transaction.called
        _, trans_kwargs = spy_start_transaction.call_args

        rc = trans_kwargs.get("read_concern")
        assert rc is not None
        assert rc.level == "majority", f"Expected ReadConcern 'majority', but got '{rc.level if rc else 'None'}'"

        # 5. DB Verification (Sanity Check)
        count = await Product.find_all().count()
        assert count == 1

    @pytest.mark.asyncio
    async def test_beanie_triggers_pymongo_session_lookup(self, mocker: MockerFixture, init_beanie) -> None:
        spy_get_bound = mocker.spy(AsyncMongoClient, "_get_bound_session")

        client = MongoDB.get_client()
        async with client.start_session() as session:
            async with session.bind():
                token = _SESSION.set(session)
                try:
                    await Product.find_all().to_list()

                    assert spy_get_bound.called, (
                        "CRITICAL FAILURE: Beanie performed the operation without "
                        "triggering the driver's session lookup!"
                    )
                    returned_session = spy_get_bound.spy_return
                    assert returned_session == session, "The driver found the wrong session!"

                finally:
                    _SESSION.reset(token)
