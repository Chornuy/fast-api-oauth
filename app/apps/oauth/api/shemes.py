from typing import Any, Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, model_validator

from app.core.exceptions.validation import CustomValidationException
from app.core.pydantic.decorator import as_form
from app.libs.oauth_flow.constants import GrantTypeEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@as_form
class OauthScheme(BaseModel):
    grant_type: GrantTypeEnum
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    refresh_token: Optional[str] = None

    @staticmethod
    def validate_refresh_token_fields(data: dict) -> None:
        if not data.get("refresh_token"):
            # raise ValueError("refresh token field is required")
            raise CustomValidationException(loc=("refresh_token",), msg="refresh token field is required")

    @staticmethod
    def validate_authorization_code_fields(data: dict) -> None:
        require_fields = ["code", "redirect_uri"]
        for require_field in require_fields:
            if not data.get(require_field):
                raise CustomValidationException(loc=(require_field,), msg=f"{require_field} field is required")

    @model_validator(mode="before")
    def validate_based_on_grant_type(cls, data: dict) -> Any:
        grant_type = data.get("grant_type")
        if not grant_type:
            return data

        if grant_type == GrantTypeEnum.refresh_token.value:
            cls.validate_refresh_token_fields(data)

        if grant_type == GrantTypeEnum.authorization_code.value:
            cls.validate_authorization_code_fields(data)


class TokenScheme(BaseModel):
    access_token: str
    token_type: str


class TokenDataScheme(BaseModel):
    username: str | None = None


class TokenPair(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    refresh_token: Optional[str]
    expires_in: Optional[int]
