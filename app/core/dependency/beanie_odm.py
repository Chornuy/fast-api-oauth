from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic_settings import BaseSettings

from app.core.dependency.exceptions import MongoDbException


class MongoDB:
    db_client: AsyncIOMotorClient | None = None

    @classmethod
    def get_client(cls):
        if not cls.db_client:
            raise MongoDbException("Mongo client was not inited, call init method first")
        return cls.db_client

    @classmethod
    def get_session(cls):
        """ """
        yield from _get_client(cls.get_client())

    @classmethod
    def init_client(cls, mongo_connect_url: str) -> AsyncIOMotorClient:
        if cls.db_client:
            return cls.db_client

        cls.db_client = AsyncIOMotorClient(mongo_connect_url)
        return cls.db_client

    @classmethod
    async def init_beanie_db(cls, model_settings: BaseSettings, models_list: list):
        """ """

        client = cls.init_client(str(model_settings.MONGO_URL))
        await init_beanie(
            database=AsyncIOMotorDatabase(client, model_settings.MONGO_DB_NAME),
            document_models=models_list,
        )


async def _get_client(client: AsyncIOMotorClient):
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                yield session
                session.commit_transaction()
            except Exception as exp:
                session.abort_transaction()
                raise exp
            finally:
                # logging.info(session.session_id)
                session.end_session()


async def init_beanie_db(model_settings: BaseSettings, models_list: list):
    """

    Args:
        model_settings:
        models_list:

    Returns:

    """
    await MongoDB.init_beanie_db(model_settings, models_list)
