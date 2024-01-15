from app.apps.oauth.models import JwtToken
from app.apps.user.models import User
from app.libs.jwt_auth.exceptions import TokenException
from app.libs.jwt_auth.manager import RefreshTokenManager
from app.libs.jwt_auth.tokens import AccessToken, RefreshToken, Token
from app.libs.utils.datetime import datetime_from_epoch


class UserTokenManager(RefreshTokenManager):
    async def transform_token(self, token: AccessToken) -> User:
        """

        Args:
            token:

        Returns:

        """
        return await User.repository.ger_user_by_email(token["username"])

    async def is_blacklisted(self, token: Token) -> None:
        """

        Args:
            token:

        Raises:

        Returns:

        """
        is_token_blacklisted = await JwtToken.repository.is_blacklisted(token[RefreshToken.jti_claim])
        if is_token_blacklisted:
            raise TokenException("Token is black listed")

    async def set_token_data(self, user: User, token: RefreshToken) -> RefreshToken:
        """

        Args:
            user:
            token:

        Returns:

        """
        token["username"] = user.email
        await JwtToken.repository.create(
            jti=token[RefreshToken.jti_claim],
            token=str(token),
            created_at=token.current_time,
            expire_at=datetime_from_epoch(token["exp"]),
        )
        return token

    async def token_to_blacklist(self, token: RefreshToken):
        await JwtToken.repository.blacklist(
            token=str(token), jti=token[RefreshToken.jti_claim], expire_at=datetime_from_epoch(token["exp"])
        )
