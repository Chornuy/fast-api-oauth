from app.libs.click_cli.fast_api_cli import FastAPICli
from app.libs.utils.managment import get_fast_api_app

TEST_FAST_API_STR = "app.libs.click_cli.tests.fixture_commands.fixture_fast_api_init:test_fast_api_app"

fixture_fast_api = get_fast_api_app(TEST_FAST_API_STR)


fixture_commands_modules = [
    "app.libs.click_cli.tests.fixture_commands.commands_a",
    "app.libs.click_cli.tests.fixture_commands.commands_b",
]

fast_api_cli_test = FastAPICli(fast_api=fixture_fast_api, import_modules=fixture_commands_modules)
