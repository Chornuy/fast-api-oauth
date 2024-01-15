from datetime import datetime

from app.apps.oauth.models import OAuthCode
from app.apps.oauth.services.exceptions import AuthCodeNotFound, WrongAuthCode
from app.apps.oauth.services.token_manager import UserTokenManager
from app.apps.user.models import User
from app.libs.oauth_flow.constants import GrantTypeEnum
from app.libs.oauth_flow.manager import BaseOauthFlowManager


class OauthFlowManager(BaseOauthFlowManager):
    token_manager = UserTokenManager()
    auth_code_manager = OAuthCode.repository

    grant_type_key = "grant_type"

    supported_grant_types = [GrantTypeEnum.authorization_code.value, GrantTypeEnum.refresh_token.value]

    grant_types_processing = {GrantTypeEnum.authorization_code.value: "", GrantTypeEnum.refresh_token.value: ""}

    async def refresh_token(self, refresh_token: str):
        """

        Args:
            refresh_token:

        Returns:

        """
        await self.token_manager.verify_token(refresh_token)
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

        if not code_obj.is_valid(datetime_obj=datetime_obj, redirect_uri=redirect_uri):
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
