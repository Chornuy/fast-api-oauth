from pydantic_settings import BaseSettings

from app.libs.managment.loader import get_settings
from app.libs.utils.lazy import SimpleLazyObject


class AppSettings(BaseSettings):
    DEBUG: bool = True
    APPS_DIR_NAME: str = "apps"


settings = SimpleLazyObject(get_settings)
