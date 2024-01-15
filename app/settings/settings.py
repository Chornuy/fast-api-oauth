import pathlib
from functools import lru_cache

from pydantic import Extra, MongoDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project config
    DEBUG: bool = True
    # Secret key
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY: str = "secret"

    # Aps settings
    APPS_FOLDER_NAME: str = "apps"
    PROJECT_FOLDER_NAME: str = "app"

    # Project folders
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent
    PROJECT_DIR: pathlib.Path = BASE_DIR.joinpath(pathlib.Path(PROJECT_FOLDER_NAME))
    APPS_DIR: pathlib.Path = PROJECT_DIR.joinpath(APPS_FOLDER_NAME)

    PROJECT_NAME: str = "fast-api-websockets"

    API_V1_STR: str = "/v1"

    # Mongo Db connection config
    MONGO_URL: MongoDsn | None = None

    MONGO_DB_SCHEME: str = "mongodb"
    MONGO_DB_USER: str = ""
    MONGO_DB_PASS: str = ""
    MONGO_DB_HOST: str = "localhost"
    MONGO_DB_PORT: int | None = 0
    MONGO_DB_NAME: str = ""

    ALLOWED_ORIGINS: list = [""]

    @model_validator(mode="after")
    def assemble_db_connection(self):
        mongo_str = MongoDsn.build(
            scheme=self.MONGO_DB_SCHEME,
            username=self.MONGO_DB_USER,
            password=self.MONGO_DB_PASS,
            host=self.MONGO_DB_HOST,
            port=self.MONGO_DB_PORT,
            path=f"{self.MONGO_DB_NAME or ''}",
        )
        self.MONGO_URL = mongo_str
        return self

    # Redis config
    REDIS_URL: RedisDsn | None = None

    REDIS_DB_USER: str = ""
    REDIS_DB_PASS: str = ""
    REDIS_DB_HOST: str = "localhost"
    REDIS_DB_PORT: int = 6379
    REDIS_DB_NUMBER: int | None = 0

    @model_validator(mode="after")
    def assemble_reddis_connection(self):
        redis_str = RedisDsn.build(
            scheme="redis",
            username=self.REDIS_DB_USER,
            password=self.REDIS_DB_PASS,
            host=self.REDIS_DB_HOST,
            port=self.REDIS_DB_PORT,
            path=f"/{self.REDIS_DB_NUMBER or 0}",
        )
        self.REDIS_URL = str(redis_str)
        return self

    # Project documentation settings
    # In case for production mod can be simple not set to disable docs urls
    REDOCK_URL: str | None = None
    DOCS_URL: str | None = "/docs"
    OPENAPI_URL: str | None = "/redoc"

    # Email settings
    EMAIL_HOST: str | None = "mailhog"
    EMAIL_PORT: int | None = 1025
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_FROM: str | None = "admin@amdmin.com"
    EMAIL_FROM_NAME: str | None = "admin"
    EMAIL_USE_CREDENTIALS: bool | None = True
    EMAIL_MAIL_TLS: bool | None = False
    EMAIL_MAIL_SSL: bool | None = False
    MAIL_STARTTLS: bool = False

    # JWT token auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = Extra.ignore


@lru_cache
def get_settings():
    return Settings()


settings = Settings()
