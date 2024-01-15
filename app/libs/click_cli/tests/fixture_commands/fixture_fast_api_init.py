from contextlib import asynccontextmanager

from fastapi import FastAPI


def mock_start_something():
    pass


def mock_close_something():
    pass


@asynccontextmanager
async def lifespan_fixture(app: FastAPI):
    mock_start_something()
    yield
    mock_close_something()


test_fast_api_app = FastAPI(lifespan=lifespan_fixture)
