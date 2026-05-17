import pytest
import pytest_asyncio
from asyncclick.testing import CliRunner
from pymongo.asynchronous.client_session import AsyncClientSession
from pytest_mock import MockerFixture

from app.libs.beanie_odm_ext.session import WireSession
from app.libs.beanie_odm_ext.tests.fixtures.models import Product, Category
from app.libs.beanie_odm_ext.transaction import Atomic
from app.libs.click_cli.command_cli import FastApiCli
from app.libs.click_cli.fast_api_cli import FastAPICli
from app.libs.managment import get_fast_api_cli


class TestCommandCliIntegration:
    @pytest_asyncio.fixture(autouse=True)
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

    @pytest_asyncio.fixture(scope="class", autouse=True)
    def fast_api_beanie_cli_app(self) -> FastApiCli:
        return get_fast_api_cli("app.libs.beanie_odm_ext.tests.fixtures.click_async:fast_api_cli_test")

    @pytest_asyncio.fixture(scope="class", autouse=True)
    def cli_runner(self):
        return CliRunner(mix_stderr=False)

    @pytest.mark.asyncio
    async def test_cli_with_session_and_transaction(
        self, mocker: MockerFixture, cli_runner: CliRunner, fast_api_beanie_cli_app: FastAPICli
    ) -> None:
        spy_session_enter = mocker.spy(WireSession, "__aenter__")
        spy_session_exit = mocker.spy(WireSession, "__aexit__")

        spy_transaction_enter = mocker.spy(Atomic, "__aenter__")
        spy_transaction_exit = mocker.spy(Atomic, "__aexit__")
        spy_transaction_commit = mocker.spy(Atomic, "_commit_with_retry")

        result = await cli_runner.invoke(fast_api_beanie_cli_app, ["create-products"])

        assert spy_session_enter.called, "Session was not created!"
        assert spy_session_exit.called, "Session was not Closed!"

        assert spy_transaction_enter.called, "Atomic transaction was never entered!"
        assert spy_transaction_exit.called, "Atomic transaction was never exited!"
        assert spy_transaction_commit.called, "Transaction was never committed!"

        assert result.exit_code == 0
        assert result.stdout == "product_with_cli\n"
        product = await Product.find_one(Product.name == "product_with_cli")
        assert product is not None

    @pytest.mark.asyncio
    async def test_cli_transaction_rollback_on_error(
        self, mocker: MockerFixture, cli_runner: CliRunner, fast_api_beanie_cli_app: FastAPICli
    ) -> None:
        # 1. Setup Spies for the failure flow

        # We spy on the driver directly to be 100% sure the 'abort' reached the wire
        spy_abort = mocker.spy(AsyncClientSession, "abort_transaction")
        spy_commit = mocker.spy(AsyncClientSession, "commit_transaction")

        # 2. Act: Call the command that raises an Exception
        # Note: CliRunner catches exceptions by default.
        # result.exception will contain the "Product creation failed" error.
        result = await cli_runner.invoke(fast_api_beanie_cli_app, ["create-products-with-error"])

        # 3. Assertions
        # We expect an exit_code of 1 because of the unhandled Exception
        assert result.exit_code != 0
        assert "Product creation failed" in str(result.exception)

        # Infrastructure assertions
        assert spy_abort.called, "Abort transaction was NOT called!"
        assert not spy_commit.called, "Commit was called despite the error!"

        # 4. The Golden Proof: Data Integrity
        # Even though .save() was called in the CLI, the document must not exist
        product = await Product.find_one(Product.name == "product_with_cli_error")
        assert product is None, "Data was persisted despite the transaction failure!"

        category = await Category.find_one(Category.name == "Test category")
        assert category is None, "Category should have been rolled back too!"

    @pytest.mark.asyncio
    async def test_get_product_cli(
        self, mocker: MockerFixture, cli_runner: CliRunner, fast_api_beanie_cli_app: FastAPICli
    ) -> None:
        # 1. Setup: Create a product directly in the DB to read
        # We use a real object to ensure the ID exists
        category = Category(name="Read Category", description="test")
        await category.save()
        existing_product = Product(name="find_me", category=category, price=50)
        await existing_product.save()

        product_id = str(existing_product.id)

        # 2. Spy on the session to ensure read-only sessions are still wired
        spy_session_enter = mocker.spy(WireSession, "__aenter__")
        spy_session_exit = mocker.spy(WireSession, "__aexit__")
        # 3. Act: Invoke the command with the product_id argument
        result = await cli_runner.invoke(fast_api_beanie_cli_app, ["get-product", product_id])

        # 4. Assertions
        assert result.exit_code == 0
        assert product_id in result.stdout.strip()
        assert spy_session_enter.called, "Session was not opened for read operation!"
        assert spy_session_exit.called, "Session was not Closed!"
