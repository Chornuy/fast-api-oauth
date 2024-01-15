from typing import Any, Sequence

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_400_BAD_REQUEST


def transform_errors(errors: Sequence[Any]) -> list:
    errors_response = []

    for error in errors:
        print(error)
        error_dict = {
            "field_name": ".".join(error["loc"]),
            "message": error["msg"]
        }
        errors_response.append(error_dict)

    return errors_response


VALIDATION_STATUS_CODE = 400
VALIDATION_STATUS_MESSAGE = "Request contain errors in data"


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Override default validation exception

    Args:
        request (Request):
        exc (RequestValidationError):

    Returns:

    """
    errors_fields_response = transform_errors(exc.errors())
    error_dict = {
        "status_code": VALIDATION_STATUS_CODE,
        "message": VALIDATION_STATUS_MESSAGE
    }
    if errors_fields_response:
        error_dict["fields"] = errors_fields_response

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(error_dict),
    )


