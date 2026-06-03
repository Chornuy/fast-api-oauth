from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.app_bootstrap import bootstrap
from app.apps.user.models import User
from app.apps.user.tests.factories import UserFactory
from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.libs.managment import get_fast_api_app

TEST_USER_EMAIL = "test@gmail.com"
TEST_USER_PASS = "qw123321"


@pytest.fixture(scope="session")
def base_dir():
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def app_bootstrap():
    return bootstrap


@pytest_asyncio.fixture(scope="function")
async def fast_api() -> AsyncGenerator[FastAPI, None]:
    fastapi = get_fast_api_app()
    async with LifespanManager(fastapi, startup_timeout=100, shutdown_timeout=100):
        yield fastapi


@pytest_asyncio.fixture(scope="function")
async def persistent_user(clear_db, fast_api: FastAPI) -> User:
    existing_user = await User.find_one(User.email == TEST_USER_EMAIL)
    if existing_user:
        return existing_user

    return await UserFactory.create_async(
        password=UserFactory.__model__.make_password(TEST_USER_PASS),
        email=TEST_USER_EMAIL,
    )


@pytest_asyncio.fixture(scope="function")
async def api_client(clear_db, fast_api: FastAPI):
    """api client fixture."""
    server_name = "https://localhost"
    async with AsyncClient(transport=ASGITransport(app=fast_api), base_url=server_name) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def clear_db(app_bootstrap: ApplicationBootStrap):
    for model in bootstrap.context["beanie_models"]:
        try:
            # delete_many({}) is safer and faster than dropping collection indexes entirely
            await model.get_pymongo_collection().delete_many({})
        except Exception:
            pass
