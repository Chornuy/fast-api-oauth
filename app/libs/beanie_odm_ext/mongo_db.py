from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.libs.beanie_odm_ext.exceptions import MongoDbException


class MongoDB:
    db_client: AsyncMongoClient | None = None

    @classmethod
    def get_client(cls) -> AsyncMongoClient:
        """

        Returns:

        """
        if not cls.db_client:
            raise MongoDbException("Mongo client was not inited, call init method first")
        return cls.db_client

    @classmethod
    def init_client(cls, **mongo_connection_kwargs) -> AsyncMongoClient | None:
        """

        Args:
            **mongo_connection_kwargs:

        Returns:

        """
        if cls.db_client:
            return cls.db_client

        cls.db_client = AsyncMongoClient(**mongo_connection_kwargs)
        return cls.db_client

    @classmethod
    async def init_beanie_db(cls, db_name: str, mongo_connection_params: dict, models_list: list):
        """

        Args:
            db_name (str):
            mongo_connection_params (dict):
            models_list (list):

        Returns:

        """
        client = cls.init_client(**mongo_connection_params)
        await init_beanie(database=client[db_name], document_models=models_list)
