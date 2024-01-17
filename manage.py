import os

from app.libs.utils.managment import get_fast_api_cli

FAST_API_CLI_PATH = os.environ.setdefault("FAST_API_CLI_PATH", "app.fast_api_cli:fast_api_cli")
FAST_API_APP_PATH = os.environ.setdefault("FAST_API_APP_PATH", "app.fast_api_app:app")
FAST_API_SETTINGS_DEFAULT_PATH = os.environ.setdefault(
    "FAST_API_SETTINGS_DEFAULT_PATH", "app.settings.settings:Settings"
)

fast_api_cli = get_fast_api_cli()

if __name__ == "__main__":
    fast_api_cli()
