from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic_core import ErrorDetails


class CustomValidationException(RequestValidationError):
    def __init__(self, loc, msg, type: str = "init", input: Any = None, body: Any = None) -> None:
        errors = [ErrorDetails(loc=loc, msg=msg, type=type, input=input)]
        super().__init__(errors)
        self.body = body


def raise_exception(model_name: str, loc: tuple[int | str, ...], error_type: str, message: str):
    raise RequestValidationError(errors=[ErrorDetails(loc=loc, msg=message, type="init", input="test")])
