from app.settings.settings import Settings


class TestSettings(Settings):
    MONGO_DB_NAME = "test_db"


settings = Settings()
