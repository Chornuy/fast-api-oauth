import asyncio

from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.libs.beanie_odm_ext.exceptions import MongoDbError


class MongoClientManager:
    """
    An isolated instance of the database connection engine.
    Every instance is bound strictly to the event loop it was initialized on.
    """

    def __init__(self):
        self._client: AsyncMongoClient | None = None
        self._db_name: str | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    def get_client(self) -> AsyncMongoClient:
        current_loop = asyncio.get_running_loop()
        if not self._client or self._loop != current_loop:
            raise MongoDbError("Database engine not initialized or event loop changed. Call init_beanie_db first.")
        return self._client

    async def init_beanie_db(
        self,
        db_name: str,
        mongo_connection_params: dict,
        models_list: list,
    ) -> None:
        current_loop = asyncio.get_running_loop()

        # If a client exists but belongs to an old or closed context, force clear it
        if self._client is not None:
            if self._loop != current_loop:
                self._client = None

        self._db_name = db_name
        self._loop = current_loop

        # Instantiate fresh connection explicitly bound to the current running loop context
        self._client = AsyncMongoClient(**mongo_connection_params)
        await init_beanie(database=self._client[db_name], document_models=models_list)

    async def close(self) -> None:
        if self._client:
            try:
                await self._client.close()
            except Exception:
                pass
            finally:
                self._client = None
                self._loop = None


mongo_client_manager: MongoClientManager = MongoClientManager()
