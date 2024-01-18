from pathlib import Path

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from app.app_bootstrap import bootstrap
from app.apps.user.models import User
from app.apps.user.tests.factories import UserFactory
from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.libs.utils.managment import get_fast_api_app

TEST_USER_EMAIL = "test@gmail.com"
TEST_USER_PASS = "qw123321"


@pytest.fixture
def base_dir():
    return Path(__file__).parent.parent


@pytest.fixture
def app_bootstrap():
    return bootstrap


@pytest_asyncio.fixture
async def fast_api() -> FastAPI:
    fastapi = get_fast_api_app()
    async with LifespanManager(fastapi, startup_timeout=100, shutdown_timeout=100):
        yield fastapi


@pytest_asyncio.fixture
async def persistent_user(fast_api: FastAPI) -> User:
    return await UserFactory.create_async(
        password=UserFactory.__model__.make_password(TEST_USER_PASS), email=TEST_USER_EMAIL
    )


@pytest_asyncio.fixture
async def api_client(clear_db, fast_api: FastAPI):
    """api client fixture."""
    server_name = "https://localhost"
    async with AsyncClient(app=fast_api, base_url=server_name) as ac:
        yield ac


@pytest_asyncio.fixture
async def clear_db(app_bootstrap: ApplicationBootStrap):
    yield
    for model in bootstrap.context["beanie_models"]:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()
