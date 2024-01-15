import asyncclick as click

from app.libs.click_cli.tests.fixture_commands.fixture_fast_api_cli import fast_api_cli_test


def function_for_test():
    pass


async def async_function_for_test():
    pass


@fast_api_cli_test.command()
async def command_a_one():
    function_for_test()
    await async_function_for_test()
    click.echo("ok")


@fast_api_cli_test.command()
async def command_a_two():
    await async_function_for_test()


@fast_api_cli_test.command()
async def command_a_three():
    function_for_test()


def not_fast_api_command():
    pass


async def async_not_fast_api_command():
    pass
