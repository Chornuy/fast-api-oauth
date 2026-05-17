from fastapi import APIRouter

from .api import endpoints as api_endpoints
from .app import app_name
from .view import endpoints as login_endpoints

api_router = APIRouter()
api_router.include_router(api_endpoints.router, prefix=f"/{app_name}", tags=[app_name])
api_router.include_router(login_endpoints.router, prefix=f"/{app_name}", tags=[app_name])
