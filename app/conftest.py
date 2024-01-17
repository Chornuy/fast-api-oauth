from pathlib import Path

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from app.app_bootstrap import bootstrap
from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.libs.utils.managment import get_fast_api_app


@pytest.fixture
def base_dir():
    return Path(__file__).parent.parent


@pytest.fixture
def app_bootstrap():
    return bootstrap


@pytest.fixture()
def fast_api() -> FastAPI:
    return get_fast_api_app()


@pytest_asyncio.fixture
async def api_client(clear_db, fast_api: FastAPI):
    """api client fixture."""
    async with LifespanManager(fast_api, startup_timeout=100, shutdown_timeout=100):
        server_name = "https://localhost"
        async with AsyncClient(app=fast_api, base_url=server_name) as ac:
            yield ac


@pytest_asyncio.fixture
async def clear_db(app_bootstrap: ApplicationBootStrap):
    yield
    for model in bootstrap.context["beanie_models"]:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()
