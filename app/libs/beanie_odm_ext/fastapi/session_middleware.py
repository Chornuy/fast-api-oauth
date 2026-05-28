import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.libs.beanie_odm_ext.session import WireSession
from app.libs.beanie_odm_ext.transaction import Atomic

logger = logging.getLogger(__name__)


class MongoSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, atomic_requests: bool = False):
        super().__init__(app)
        self.atomic_requests = atomic_requests

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            async with WireSession():
                if self.atomic_requests:
                    async with Atomic():
                        return await call_next(request)
                return await call_next(request)

        except Exception as exc:
            logger.error(f"Middleware caught error on {request.url.path}: {exc}")
            raise exc
