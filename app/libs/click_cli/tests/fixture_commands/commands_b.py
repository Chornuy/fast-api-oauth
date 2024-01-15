from app.libs.click_cli.tests.fixture_commands.fixture_fast_api_cli import fast_api_cli_test


class SomeClass:
    def __init__(self):
        self.name = "test"

    async def async_some_func(self):
        return f"{self.name}: test"

    def some_func(self):
        return f"{self.name}: test"


@fast_api_cli_test.command()
async def command_b_one():
    some_class = SomeClass()
    return await some_class.async_some_func()


@fast_api_cli_test.command()
async def command_b_two():
    some_class = SomeClass()
    return some_class.some_func()
