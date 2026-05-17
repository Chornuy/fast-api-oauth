from typing import Type

from pydantic import BaseModel

from app.libs.managment import get_app_by_env_str

FAST_API_SETTINGS_ENV_NAME = "FAST_API_SETTINGS_PATH"
FAST_API_SETTINGS_DEFAULT_PATH = "app.settings.settings:Settings"


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
    return get_app_by_env_str(FAST_API_SETTINGS_ENV_NAME, fast_api_cli_import_str)()
