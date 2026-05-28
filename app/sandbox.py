from collections.abc import Callable
from functools import wraps

from pydantic_settings import BaseSettings
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import _SESSION, AsyncClientSession


class MongoDBSettings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"


settings = MongoDBSettings()

_mongo_client = None


def get_client() -> "AsyncMongoClient":
    # Function that return current Mongo client
    if not _mongo_client:
        global _mongo_client
        _mongo_client = AsyncMongoClient(settings.MONGO_URI)
        return _mongo_client

    return _mongo_client


def auto_session(**session_kwargs) -> Callable:
    """Decorator that sets session automatically"""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args, **kwargs):
            client = get_client()  # Return MongoClientAsync
            async with client.start_session(**session_kwargs) as s:
                async with s.bind():
                    return await f(*args, **kwargs)

        return wrapper

    return decorator


def wrap_in_transaction(**transaction_kwargs) -> Callable:
    """Decorator that sets transaction automatically with bind session"""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args, **kwargs):
            db_session: AsyncClientSession | None = _SESSION.get()
            if not db_session:
                raise Exception("Session not initialized, start session with using .bind() method")

            async with await db_session.start_transaction(**transaction_kwargs):
                return await f(*args, **kwargs)

        return wrapper

    return decorator
