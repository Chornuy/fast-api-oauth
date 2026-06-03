import logging
from collections.abc import Awaitable, Callable
from contextlib import AsyncContextDecorator
from typing import Any, ParamSpec, TypeVar, overload

from pymongo.asynchronous.client_session import _SESSION
from pymongo.errors import ConnectionFailure, OperationFailure

Param = ParamSpec("Param")
RetType = TypeVar("RetType")

logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRY = 2

AF = TypeVar("AF", bound=Awaitable[Callable[..., Any]])
P = ParamSpec("P")
R = TypeVar("R")


class Atomic(AsyncContextDecorator):
    def __init__(self, max_retry: int = DEFAULT_MAX_RETRY, **transaction_kwargs):
        self.transaction_kwargs = transaction_kwargs
        self.max_retry = max_retry

    async def __aenter__(self):
        db_session = _SESSION.get()
        if db_session is None:
            raise RuntimeError(
                "No active session found! You must wrap your entry point "
                "with 'async with session.bind():' before using TransactionManager."
            )

        # Guard against nested transactions if your logic requires it
        if db_session.in_transaction:
            logger.warning("Session already in transaction. Skipping start_transaction.")
            return db_session

        await db_session.start_transaction(**self.transaction_kwargs)
        return db_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        db_session = _SESSION.get()
        if not db_session or not db_session.in_transaction:
            return

        if exc_type is None:
            # Handle the commit logic with retries
            await self._commit_with_retry(db_session)
        else:
            # Something went wrong, rollback
            logger.error(f"Transaction failed: {exc_val}. Aborting.")
            await db_session.abort_transaction()

    async def _commit_with_retry(self, db_session):
        current_try = 0
        while True:
            try:
                await db_session.commit_transaction()
                logger.debug("Transaction committed successfully.")
                break
            except (ConnectionFailure, OperationFailure) as exc:
                if exc.has_error_label("TransientTransactionError") and current_try < self.max_retry:
                    current_try += 1
                    logger.debug(f"Transient error, retrying commit ({current_try}/{self.max_retry})...")
                    continue
                raise exc


@overload
def atomic(func: Callable[P, Awaitable[R]], **kwargs: Any) -> Callable[P, Awaitable[R]]: ...


@overload
def atomic(func: Callable[P, Awaitable[R]] | None = None, **kwargs: Any) -> Atomic: ...


def atomic(func: Callable[P, Awaitable[R]] | None = None, **transaction_kwargs) -> Awaitable[AF] | Atomic:
    if callable(func):
        return Atomic(**transaction_kwargs)(func)
    else:
        return Atomic(**transaction_kwargs)
