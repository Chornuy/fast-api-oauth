from pydantic_settings import BaseSettings


def transform_settings_to_mongo(settings: BaseSettings) -> dict:
    """Simple function transformer helper to transform settings into MongoDB client connection params

    Args:
        settings: Pydantic settings object

    Returns:
        dict: dict with connection params for MongoDB client
    """
    return {"host": str(settings.MONGO_URL)}
