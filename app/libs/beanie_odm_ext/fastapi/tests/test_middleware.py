from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from pymongo.asynchronous.client_session import AsyncClientSession
from pytest_mock import MockerFixture

from app.libs.beanie_odm_ext.session import WireSession
from app.libs.beanie_odm_ext.tests.fixtures.click_async import TEST_FAST_API_STR
from app.libs.beanie_odm_ext.tests.fixtures.models import Product, Category
from app.libs.beanie_odm_ext.transaction import Atomic
from app.libs.managment import get_fast_api_app


class TestFastApiMiddleWareIntegration:
    @pytest.fixture(autouse=True)
    async def cleanup_mongo(self):
        """
        Ensure the collections are empty before and after the CLI runs.
        """
        # 1. Pre-test cleanup
        # await Category.get_pymongo_collection().delete_many({})
        # await Product.get_pymongo_collection().delete_many({})

        yield

        # 2. Post-test cleanup
        await Category.get_pymongo_collection().delete_many({})
        await Product.get_pymongo_collection().delete_many({})

    @pytest_asyncio.fixture
    async def fast_api_app(self) -> AsyncGenerator[FastAPI, None]:
        fast_api_app = get_fast_api_app(TEST_FAST_API_STR)
        async with LifespanManager(fast_api_app, startup_timeout=100, shutdown_timeout=100):
            yield fast_api_app

    @pytest_asyncio.fixture
    async def api_client(self, fast_api_app: FastAPI):
        """api client fixture."""
        server_name = "https://localhost"
        async with AsyncClient(
            transport=ASGITransport(app=fast_api_app, raise_app_exceptions=False),
            base_url=server_name,
        ) as ac:
            yield ac

    @pytest.mark.asyncio
    async def test_api_middleware_create_product_success(
        self, mocker: MockerFixture, api_client: AsyncClient, fast_api_app
    ) -> None:
        spy_session_enter = mocker.spy(WireSession, "__aenter__")
        spy_session_exit = mocker.spy(WireSession, "__aexit__")

        spy_transaction_enter = mocker.spy(Atomic, "__aenter__")
        spy_transaction_exit = mocker.spy(Atomic, "__aexit__")
        spy_transaction_commit = mocker.spy(Atomic, "_commit_with_retry")

        # Act
        response = await api_client.post(url=f"{api_client.base_url}{fast_api_app.url_path_for('create_product')}")

        assert spy_session_enter.called, "Session was not created!"
        assert spy_session_exit.called, "Session was not Closed!"

        assert spy_transaction_enter.called, "Atomic transaction was never entered!"
        assert spy_transaction_exit.called, "Atomic transaction was never exited!"
        assert spy_transaction_commit.called, "Transaction was never committed!"

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "success_product"

        product = await Product.find_one(Product.name == "success_product")
        assert product is not None

    @pytest.mark.asyncio
    async def test_api_middleware_transaction_rollback(
        self, mocker: MockerFixture, api_client: AsyncClient, fast_api_app
    ) -> None:
        spy_abort = mocker.spy(AsyncClientSession, "abort_transaction")
        spy_commit = mocker.spy(AsyncClientSession, "commit_transaction")

        response = await api_client.post(
            url=f"{api_client.base_url}{fast_api_app.url_path_for('create_product_with_error')}"
        )
        assert spy_abort.called, "Abort transaction was NOT called!"
        assert not spy_commit.called, "Commit was called despite the error!"

        assert response.status_code == 500
        assert spy_abort.called, "The transaction should have aborted on 500 error!"

        product = await Product.find_one(Product.name == "product_with_error")
        assert product is None, "Data leaked! Rollback failed."

    @pytest.mark.asyncio
    async def test_api_middleware_get_product_flow(self, mocker: MockerFixture, api_client: AsyncClient) -> None:
        spy_session_enter = mocker.spy(WireSession, "__aenter__")
        spy_session_exit = mocker.spy(WireSession, "__aexit__")

        category = Category(name="API Test", description="...")
        await category.save()
        product = Product(name="find_me_api", category=category, price=99)
        await product.save()

        response = await api_client.get(f"/products/{product.id}")
        assert spy_session_enter.called, "Session was not created!"
        assert spy_session_exit.called, "Session was not Closed!"
        assert response.status_code == 200
        assert response.json()["name"] == "find_me_api"
