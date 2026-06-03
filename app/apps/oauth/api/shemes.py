from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, model_validator

from app.apps.oauth.services.constants import TokenType
from app.core.exceptions.validation import CustomValidationError
from app.libs.oauth_flow.constants import GrantTypeEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class OauthScheme(BaseModel):
    grant_type: GrantTypeEnum
    code: str | None = None
    redirect_uri: str | None = None
    refresh_token: str | None = None

    @staticmethod
    def validate_refresh_token_fields(data: dict) -> dict:
        if not data.get("refresh_token"):
            raise CustomValidationError(loc=("refresh_token",), msg="refresh token field is required")
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
                raise CustomValidationError(loc=(require_field,), msg=f"{require_field} field is required")
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
    refresh_token: str | None = None
    expires_in: int | None = None


class UserResponseScheme(BaseModel):
    email: str
