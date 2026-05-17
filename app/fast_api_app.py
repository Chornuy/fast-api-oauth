# Logger init
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from app.app_bootstrap import bootstrap
from app.core.exception_handler.root import root_exception_handlers
from app.core.middlewares.cors import setup_cors
from app.libs.beanie_odm_ext.mongo_db import MongoDB
from app.libs.managment.conf import settings
from app.settings.logging import logger_settings
from app.settings.routes import root_router
from app.utils.mongo_conf import transform_settings_to_mongo

dictConfig(logger_settings.model_dump())


@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    await MongoDB.init_beanie_db(
        db_name=settings.MONGO_DB_NAME,
        mongo_connection_params=transform_settings_to_mongo(settings),
        models_list=bootstrap.context["beanie_models"],
    )
    yield


# Fast Api init
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=settings.OPENAPI_URL,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOCK_URL,
    lifespan=lifespan,
    user_middleware=[setup_cors()],
    exception_handlers=root_exception_handlers(),
)

app.include_router(router=root_router)
