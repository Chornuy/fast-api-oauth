from fastapi import APIRouter

from app.apps.user.router import api_router as user_router
from app.apps.registration.router import api_router as registration_router
from app.apps.oauth.router import api_router as oauth_router

# Root router
root_router = APIRouter()

# Apps routes
root_router.include_router(user_router)
root_router.include_router(registration_router)
root_router.include_router(oauth_router)
