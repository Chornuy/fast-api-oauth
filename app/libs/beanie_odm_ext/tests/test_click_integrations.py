# class TestCommandCliIntegration:
#     # FIX 1: Scope everything cleanly to function level to isolate test states completely
#     @pytest_asyncio.fixture(autouse=True, scope="function", loop_scope="function")
#     async def cleanup_mongo(self):
#         """
#         Ensure the collections are empty before and after the CLI runs.
#         """
#         yield
#
#         try:
#             await Category.get_pymongo_collection().delete_many({})
#             await Product.get_pymongo_collection().delete_many({})
#         except Exception:
#             pass
#
#     @pytest_asyncio.fixture(autouse=True, scope="function", loop_scope="function")
#     async def fast_api_beanie_cli_app(self) -> FastApiCli:
#         return get_fast_api_cli("app.libs.beanie_odm_ext.tests.fixtures.click_async:fast_api_cli_test")
#
#     @pytest_asyncio.fixture(scope="function", loop_scope="function")
#     def cli_runner(self):
#         return CliRunner()
#
#     @pytest.mark.asyncio
#     async def test_cli_with_session_and_transaction(
#         self,
#         mocker: MockerFixture,
#         cli_runner: CliRunner,
#         fast_api_beanie_cli_app: FastAPICli,
#     ) -> None:
#         spy_session_enter = mocker.spy(WireSession, "__aenter__")
#         spy_session_exit = mocker.spy(WireSession, "__aexit__")
#
#         spy_transaction_enter = mocker.spy(Atomic, "__aenter__")
#         spy_transaction_exit = mocker.spy(Atomic, "__aexit__")
#         spy_transaction_commit = mocker.spy(Atomic, "_commit_with_retry")
#
#         result = await cli_runner.invoke(fast_api_beanie_cli_app, ["create-products"])
#
#         assert result.exit_code == 0
#         assert result.stdout == "product_with_cli\n"
#
#         assert spy_session_enter.called, "Session was not created!"
#         assert spy_session_exit.called, "Session was not Closed!"
#         assert spy_transaction_enter.called, "Atomic transaction was never entered!"
#         assert spy_transaction_exit.called, "Atomic transaction was never exited!"
#         assert spy_transaction_commit.called, "Transaction was never committed!"
#
#         product = await Product.find_one(Product.name == "product_with_cli")
#         assert product is not None
#
#     @pytest.mark.asyncio
#     async def test_cli_transaction_rollback_on_error(
#         self,
#         mocker: MockerFixture,
#         cli_runner: CliRunner,
#         fast_api_beanie_cli_app: FastAPICli,
#     ) -> None:
#         spy_abort = mocker.spy(AsyncClientSession, "abort_transaction")
#         spy_commit = mocker.spy(AsyncClientSession, "commit_transaction")
#
#         result = await cli_runner.invoke(fast_api_beanie_cli_app, ["create-products-with-error"])
#
#         assert result.exit_code != 0
#         assert "Product creation failed" in str(result.exception)
#
#         assert spy_abort.called, "Abort transaction was NOT called!"
#         assert not spy_commit.called, "Commit was called despite the error!"
#
#         product = await Product.find_one(Product.name == "product_with_cli_error")
#         assert product is None, "Data was persisted despite the transaction failure!"
#
#         category = await Category.find_one(Category.name == "Test category")
#         assert category is None, "Category should have been rolled back too!"
#
#     @pytest.mark.asyncio
#     async def test_get_product_cli(
#         self,
#         mocker: MockerFixture,
#         cli_runner: CliRunner,
#         fast_api_beanie_cli_app: FastAPICli,
#     ) -> None:
#         # Pre-populate database context natively using the active test loop connection parameters
#         category = Category(name="Read Category", description="test")
#         await category.save()
#         existing_product = Product(name="find_me", category=category, price=50)
#         await existing_product.save()
#
#         product_id = str(existing_product.id)
#
#         spy_session_enter = mocker.spy(WireSession, "__aenter__")
#         spy_session_exit = mocker.spy(WireSession, "__aexit__")
#
#         result = await cli_runner.invoke(fast_api_beanie_cli_app, ["get-product", product_id])
#
#         assert result.exit_code == 0
#         assert product_id in result.stdout.strip()
#         assert spy_session_enter.called, "Session was not opened for read operation!"
#         assert spy_session_exit.called, "Session was not Closed!"
