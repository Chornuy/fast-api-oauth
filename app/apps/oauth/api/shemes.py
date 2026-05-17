from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, model_validator

from app.apps.oauth.services.constants import TokenType
from app.core.exceptions.validation import CustomValidationException
from app.libs.oauth_flow.constants import GrantTypeEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class OauthScheme(BaseModel):
    grant_type: GrantTypeEnum
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    refresh_token: Optional[str] = None

    @staticmethod
    def validate_refresh_token_fields(data: dict) -> dict:
        if not data.get("refresh_token"):
            raise CustomValidationException(loc=("refresh_token",), msg="refresh token field is required")
        try:
            del data["redirect_uri"]
            del data["code"]
        except KeyError:
            pass

        return data

    @staticmethod
    def validate_authorization_code_fields(data: dict) -> dict:
        """Method that validate auth code after redirect

        Examples:
            ```
                data = {
                    "code": "123123,
                    "redirect_uri": ""
                }
                auth_scheme = OauthScheme()
                auth_scheme.validate_authorization_code_fields(data)
                ```
        Args:
            data (dict): Data to validate auth code

        Returns:
            dict:
        """
        require_fields = ["code", "redirect_uri"]
        for require_field in require_fields:
            if not data.get(require_field):
                raise CustomValidationException(loc=(require_field,), msg=f"{require_field} field is required")
        try:
            del data["refresh_token"]
        except KeyError:
            pass

        return data

    @model_validator(mode="before")
    @classmethod
    def validate_based_on_grant_type(cls, data: dict) -> dict:
        grant_type = data.get("grant_type")

        if not grant_type:
            return data

        if grant_type == GrantTypeEnum.refresh_token.value:
            data = cls.validate_refresh_token_fields(data)

        if grant_type == GrantTypeEnum.authorization_code.value:
            data = cls.validate_authorization_code_fields(data)

        return data


class TokenScheme(BaseModel):
    access_token: str
    token_type: str


class TokenDataScheme(BaseModel):
    username: str | None = None


class TokenRevokeScheme(BaseModel):
    token_type_hint: TokenType | None = None
    token: str | None = None


class TokenPair(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


class UserResponseScheme(BaseModel):
    email: str
