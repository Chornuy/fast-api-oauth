from pathlib import PosixPath, Path

import pytest

from app.libs.app_loader.middlewares.click import ClickCommandLoader
from app.libs.app_loader.middlewares.exceptions import RuntimeMiddlewareException
from app.libs.app_loader.middlewares.tests.fixture import get_base_bootstrap_config_fixture


def get_apps_context_fixture():
    return {
        'app_a': {
            'name': 'app_a',
            'module_path': 'app.core.app_loader.middlewares.tests.fixture_click.app_a',
            'folder_path':
                PosixPath('/app/libs/app_loader/middlewares/tests/fixture_click/app_a')
        },
        'app_b': {
            'name': 'app_b',
            'module_path': 'app.core.app_loader.middlewares.tests.fixture_click.app_b',
            'folder_path':
                PosixPath('/app/libs/app_loader/middlewares/tests/fixture_click/app_b')
        }
    }


class TestClickCommandLoader:

    @pytest.fixture()
    def command_loader(self):
        return ClickCommandLoader()

    def test_command_loader(self, base_dir: Path, command_loader: ClickCommandLoader) -> None:
        context = get_base_bootstrap_config_fixture(base_dir, "fixture_click")
        context["apps"] = get_apps_context_fixture()
        context = command_loader.load(context=context, config={})

        expected_result = [
            'app.core.app_loader.middlewares.tests.fixture_click.app_a.commands.command_a',
            'app.core.app_loader.middlewares.tests.fixture_click.app_a.commands.command_b'
        ] + command_loader.additional_cli_modules

        assert "commands_modules" in context.keys()
        assert context["commands_modules"] == expected_result

    def test_app_loader_not_run(self, base_dir: Path, command_loader: ClickCommandLoader) -> None:
        with pytest.raises(RuntimeMiddlewareException):
            command_loader.load(context={}, config={})
