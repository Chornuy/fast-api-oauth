import os

from app.libs.utils.managment import get_fast_api_cli

FAST_API_CLI_PATH = os.environ.setdefault("FAST_API_CLI_PATH", "app.fast_api_cli:fast_api_cli")
FAST_API_APP_PATH = os.environ.setdefault("FAST_API_APP_PATH", "app.fast_api_app:app")
CONFIG_MODULE = os.environ.setdefault("CONFIG_MODULE", "app.settings.base")

fast_api_cli = get_fast_api_cli()

if __name__ == "__main__":
    fast_api_cli()
