from pathlib import Path

from asyncclick.testing import CliRunner
import pytest
from pytest_mock import MockerFixture

from app.libs.click_cli.fast_api_cli import FastAPICli
from app.libs.utils.managment import get_fast_api_cli

fast_api_import_str = "app.core.click_cli.tests.fixture_commands.fixture_fast_api_init:test_fast_api_app"
fast_api_cli = get_fast_api_cli()


def get_fixture_path(base_dir: Path, fixture_path: list[str]):
    return str(base_dir.joinpath(Path(__file__).parent.joinpath(*fixture_path)))


class TestCommandCli:

    @pytest.fixture
    def fast_api_cli_app(self) -> FastAPICli:
        return get_fast_api_cli("app.core.click_cli.tests.fixture_commands.fixture_fast_api_cli:fast_api_cli_test")

    @staticmethod
    def get_expected_commands() -> list[str]:
        return [
            "command-a-one",
            "command-a-two",
            "command-a-three",
            "command-b-one",
            "command-b-two",
        ]

    @pytest.fixture
    def cli_runner(self):
        return CliRunner()

    @pytest.mark.asyncio
    async def test_command_imports(self, cli_runner: CliRunner, fast_api_cli_app: FastAPICli) -> None:
        await cli_runner.invoke(fast_api_cli_app, [])
        expected_result = self.get_expected_commands()
        for command in fast_api_cli_app.commands.values():
            assert command.name in expected_result

    @pytest.mark.asyncio
    async def test_fast_api_triggered_lifespan(
        self, mocker: MockerFixture, cli_runner: CliRunner, fast_api_cli_app: FastAPICli
    ) -> None:
        mock_start_lifespan = mocker.patch(
            "app.core.click_cli.tests.fixture_commands.fixture_fast_api_init.mock_start_something"
        )
        mock_close_lifespan = mocker.patch(
            "app.core.click_cli.tests.fixture_commands.fixture_fast_api_init.mock_close_something"
        )

        result = await cli_runner.invoke(fast_api_cli_app, ["command-a-one"])
        assert result.stdout == "ok\n"
        mock_start_lifespan.assert_called()
        mock_close_lifespan.assert_called()
