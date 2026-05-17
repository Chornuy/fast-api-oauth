from contextlib import AsyncContextDecorator
from typing import Callable, TypeVar, Awaitable, Any, ParamSpec, overload, Optional

from app.libs.beanie_odm_ext.mongo_db import MongoDB

AF = TypeVar("AF", bound=Awaitable[Callable[..., Any]])
P = ParamSpec("P")
R = TypeVar("R")


class WireSession(AsyncContextDecorator):
    def __init__(self, **session_kwargs):
        self.session_kwargs = session_kwargs
        self.session = None
        self.session_context = None

    async def __aenter__(self):
        client = MongoDB.get_client()
        self.session = client.start_session(**self.session_kwargs)
        self.session_context = self.session.bind()
        await self.session.__aenter__()
        await self.session_context.__aenter__()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session_context.__aexit__(exc_type, exc_val, exc_tb)
        await self.session.__aexit__(exc_type, exc_val, exc_tb)


@overload
def auto_session(func: Callable[P, Awaitable[R]], **kwargs: Any) -> Callable[P, Awaitable[R]]: ...


@overload
def auto_session(func: Optional[Callable[P, Awaitable[R]]] = None, **kwargs: Any) -> WireSession: ...


def auto_session(func: Optional[Callable[P, Awaitable[R]]] = None, **kwargs) -> AF | WireSession:
    if callable(func):
        return WireSession(**kwargs)(func)
    return WireSession(**kwargs)
