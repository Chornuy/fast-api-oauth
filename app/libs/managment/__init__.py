from typing import TYPE_CHECKING

from app.libs.managment.env_loader import get_app_by_env_str

if TYPE_CHECKING:
    from app.libs.click_cli.command_cli import FastApiCli
    from fastapi import FastAPI

FAST_API_CLI_ENV_NAME = "FAST_API_CLI_PATH"
FAST_API_CLI_DEFAULT_PATH = "app.fast_api_cli:fast_api_cli"

FAST_API_APP_ENV_NAME = "FAST_API_APP_PATH"
FAST_API_APP_DEFAULT_PATH = "app.fast_api_app:app"


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
