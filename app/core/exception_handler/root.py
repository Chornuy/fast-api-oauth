from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError

from app.core.exception_handler.validations import request_validation_exception_handler


def root_exception_handlers() -> (
    dict[
        int | type[Exception],
        Callable[[Request, Any], Coroutine[Any, Any, Response]],
    ]
):
    """

    Returns:

    """
    return {RequestValidationError: request_validation_exception_handler}
