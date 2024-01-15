from pathlib import Path, PosixPath

import pytest
from pytest_mock import MockerFixture

from app.libs.app_loader.middlewares.app_loaders import AutoImportAppLoader
from app.libs.app_loader.middlewares.exceptions import AppNameAlreadyRegistered
from app.libs.app_loader.middlewares.tests.fixture import get_base_bootstrap_config_fixture


def get_fixture_path(base_dir: Path, fixture_path: str):
    return str(base_dir.joinpath(Path(__file__).parent.joinpath("fixture_app_loader", fixture_path, "app.py")))


def get_mocked_success_flow(base_dir: Path) -> list:
    return [
        get_fixture_path(base_dir, "app_a"),
        get_fixture_path(base_dir, "app_b")
    ]


def get_expected_result_on_success_flow():
    return {
        'app_a': {
            'name': 'app_a',
            'module_path': 'app.core.app_loader.middlewares.tests.fixture_app_loader.app_a',
            'folder_path':
                PosixPath('/app/libs/app_loader/middlewares/tests/fixture_app_loader/app_a')
        },
        'app_b': {
            'name': 'app_b',
            'module_path': 'app.core.app_loader.middlewares.tests.fixture_app_loader.app_b',
            'folder_path':
                PosixPath('/app/libs/app_loader/middlewares/tests/fixture_app_loader/app_b')
        }
    }


def get_mocked_already_registered_flow(base_dir: Path) -> list:
    return [
        get_fixture_path(base_dir, "app_a"),
        get_fixture_path(base_dir, "app_b"),
        get_fixture_path(base_dir, "app_c")
    ]


class TestAppLoader:

    @pytest.fixture
    def app_loader(self) -> AutoImportAppLoader:
        return AutoImportAppLoader()

    def test_autoloader(self, mocker: MockerFixture, app_loader: AutoImportAppLoader, base_dir: Path):
        mock_get_app_folder_list = mocker.patch(
            "app.core.app_loader.middlewares.app_loaders.AutoImportAppLoader.get_app_folder_list"
        )
        mock_get_app_folder_list.return_value = get_mocked_success_flow(base_dir)

        context = app_loader.load(context=get_base_bootstrap_config_fixture(base_dir, "fixture_app_loader"), config={})
        assert "apps" in context.keys()
        expected_result = get_expected_result_on_success_flow()
        assert context["apps"] == expected_result

    def test_app_name_already_registered(self, mocker: MockerFixture, app_loader: AutoImportAppLoader, base_dir: Path):
        mock_get_app_folder_list = mocker.patch(
            "app.core.app_loader.middlewares.app_loaders.AutoImportAppLoader.get_app_folder_list"
        )
        mock_get_app_folder_list.return_value = get_mocked_already_registered_flow(base_dir)
        with pytest.raises(AppNameAlreadyRegistered):
            app_loader.load(context=get_base_bootstrap_config_fixture(base_dir, "fixture_app_loader"), config={})
