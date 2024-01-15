from fastapi import HTTPException, status


class ServiceException(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = ""
    headers: dict[str, str] = {}

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)
