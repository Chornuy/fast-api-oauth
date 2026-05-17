import os
from typing import Any

from app.utils.module_loading import cached_import_class

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
