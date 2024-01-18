import os
from typing import TYPE_CHECKING, Any, Type

from pydantic import BaseModel

from app.utils.module_loading import cached_import_class

if TYPE_CHECKING:
    from beanie.odm.documents import FastApiCli
    from fastapi import FastAPI

FAST_API_CLI_ENV_NAME = "FAST_API_CLI_PATH"
FAST_API_CLI_DEFAULT_PATH = "app.fast_api_cli:fast_api_cli"

FAST_API_APP_ENV_NAME = "FAST_API_APP_PATH"
FAST_API_APP_DEFAULT_PATH = "app.fast_api_app:app"

FAST_API_SETTINGS_ENV_NAME = "FAST_API_SETTINGS_PATH"
FAST_API_SETTINGS_DEFAULT_PATH = "app.settings.settings:Settings"


ATTR_SEPARATOR = ":"


def get_app_by_env_str(env_name: str, env_default: str) -> Any:
    """Small helper to get objects from python module by ENV var, with import str

    Args:
        env_name (str): name of ENV variable with import path
        env_default (str): default value for env

    Returns:
        Type: python object after import of module

    """
    app_path = os.environ.get(env_name, env_default)
    module_path, app_attr = app_path.rsplit(ATTR_SEPARATOR, 1)
    return cached_import_class(module_path, app_attr)


def get_settings(settings_import_str: str | None = None) -> Type[BaseModel]:
    """
    Examples:
        Code above will return Pydentic Settings object
        ```

        FAST_API_APP_PATH = os.environ.setdefault("FAST_API_SETTINGS_PATH", "app.settings:settings")
        settings = get_settings()

        ```
    Args:
        settings_import_str(str): str with path to import settings

    Returns:
        BaseSettings: object with pydentic settings
    """

    fast_api_cli_import_str = settings_import_str or FAST_API_SETTINGS_DEFAULT_PATH
    return get_app_by_env_str(FAST_API_SETTINGS_DEFAULT_PATH, fast_api_cli_import_str)()


def get_fast_api_cli(fast_api_cli_import_str: str | None = None) -> "FastApiCli":
    """Return FastApiCli instance by import str
    Examples:
        Code above will return FastApiCli object
        ```
        FAST_API_CLI_PATH = os.environ.setdefault("FAST_API_CLI_PATH", "app.fast_api_cli:fast_api_cli")
        fast_api_cli = get_fast_api_cli()
        ```

    Returns:
        FastApiCli: FastApiCli object from module where it was set up
    """
    fast_api_cli_import_str = fast_api_cli_import_str or FAST_API_CLI_DEFAULT_PATH
    return get_app_by_env_str(FAST_API_CLI_ENV_NAME, fast_api_cli_import_str)


def get_fast_api_app(fast_api_import_str: str | None = None) -> "FastAPI":
    """Return FastApiCli instance by import str
    Examples:
        Code above will return FastAPI object
        ```

        FAST_API_APP_PATH = os.environ.setdefault("FAST_API_APP_PATH", "app.fast_api_app:app")
        fast_api_app = get_fast_api_app()

        ```

    Returns:
        FastApi: FastAPI object from module where it was set up
    """
    fast_api_import_str = fast_api_import_str or FAST_API_APP_DEFAULT_PATH
    return get_app_by_env_str(FAST_API_APP_ENV_NAME, fast_api_import_str)
