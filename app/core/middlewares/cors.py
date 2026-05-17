from starlette.middleware.cors import CORSMiddleware

from app.libs.managment.conf import settings


def setup_cors() -> dict:
    return {
        "middleware_class": CORSMiddleware,
        "allow_origins": settings.ALLOWED_ORIGINS,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
