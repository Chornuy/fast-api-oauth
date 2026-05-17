from app.libs.click_cli.fast_api_cli import FastAPICli
from app.libs.managment import get_fast_api_app

TEST_FAST_API_STR = "app.libs.beanie_odm_ext.tests.fixtures.fast_api:test_fast_api_app"

fixture_fast_api = get_fast_api_app(TEST_FAST_API_STR)

commands_modules = ["app.libs.beanie_odm_ext.tests.fixtures.commands_fixtures"]

fast_api_cli_test = FastAPICli(fast_api=fixture_fast_api, import_modules=commands_modules)
