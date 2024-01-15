from fastapi import status

from app.core.exceptions.base import ServiceException


class UnauthorizedException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}
