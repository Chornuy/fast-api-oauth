from fastapi import APIRouter


from app.apps.user.api import endpoints
from app.apps.user.app import app_name

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix=f"/{app_name}", tags=[app_name])
