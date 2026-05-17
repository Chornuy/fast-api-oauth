from datetime import datetime

from app.apps.oauth.models import OAuthCode
from app.apps.oauth.services.constants import TokenType
from app.apps.oauth.services.exceptions import (
    AuthCodeNotFound,
    WrongAuthCode,
    WrongTokenType,
    UnsupportedTokenType,
    UnknownToken,
)
from app.apps.oauth.services.token_manager import UserTokenManager
from app.apps.user.models import User
from app.libs.jwt_auth.tokens import RefreshToken
from app.libs.oauth_flow.constants import GrantTypeEnum
from app.libs.oauth_flow.manager import BaseOauthFlowManager


class OauthFlowManager(BaseOauthFlowManager):
    token_manager = UserTokenManager()
    auth_code_manager = OAuthCode.repository

    grant_type_key = "grant_type"

    supported_grant_types = [GrantTypeEnum.authorization_code.value, GrantTypeEnum.refresh_token.value]

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        """

        Args:
            refresh_token:

        Returns:

        """

        refresh_token = self.token_manager.get_refresh_token_from_str(refresh_token)
        await self.token_manager.is_blacklisted(refresh_token)
        return await self.token_manager.refresh_token(refresh_token)

    async def authorization_code(self, code: str, redirect_uri: str, datetime_obj: datetime = datetime.now()):
        """

        Args:
            code:
            redirect_uri:
            datetime_obj:

        Returns:

        """
        code_obj = await self.auth_code_manager.get_code(code)

        if not code_obj:
            raise AuthCodeNotFound("Code was not found")

        is_valid = await code_obj.is_valid(datetime_obj=datetime_obj, redirect_uri=redirect_uri)

        if not is_valid:
            raise WrongAuthCode("Code not pass verification")

        user = await code_obj.get_user()
        return await self.token_manager.create_token_pair(user)

    async def generate_authorization_code(self, redirect_uri: str, user: User) -> OAuthCode:
        """

        Args:
            redirect_uri:
            user:

        Returns:

        """
        return await self.auth_code_manager.create(redirect_uri=redirect_uri, user=user)

    async def revoke_token(
        self, user: User, token: str, token_type_hint: str = TokenType.refresh_token.value
    ) -> RefreshToken:
        if not TokenType.has_value(token_type_hint):
            raise WrongTokenType("Unsupported token type")

        if token_type_hint != TokenType.refresh_token.value:
            raise UnsupportedTokenType("Unsupported token type")

        refresh_token = self.token_manager.get_refresh_token_from_str(token)
        refresh_token = await self.token_manager.revoke_refresh_token(user=user, refresh_token=refresh_token)
        if not refresh_token:
            raise UnknownToken("Unknown token")

        return refresh_token


oauth_manager = OauthFlowManager()
