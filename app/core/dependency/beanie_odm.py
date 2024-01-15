from typing import Type

import motor.motor_asyncio
from beanie import init_beanie
from pydantic import BaseModel


async def init_beanie_db(settings: Type[BaseModel],  models_list: list):
    """

    Args:
        settings:
        models_list:

    Returns:

    """
    client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.MONGO_URL))
    await init_beanie(database=client.db_name, document_models=models_list)
