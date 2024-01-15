from fastapi import APIRouter

from app.apps.registration.api import endpoints
from app.apps.registration.app import app_name, route_prefix

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix=f"/{route_prefix}", tags=[app_name])
