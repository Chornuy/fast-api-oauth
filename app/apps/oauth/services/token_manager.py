from app.apps.oauth.models import JwtToken
from app.apps.user.models import User
from app.libs.jwt_auth.exceptions import TokenError
from app.libs.jwt_auth.manager import RefreshTokenManager
from app.libs.jwt_auth.tokens import AccessToken, RefreshToken, Token
from app.libs.utils.datetime import datetime_from_epoch


class UserTokenManager(RefreshTokenManager):
    @staticmethod
    async def transform_token(token: AccessToken) -> User:
        """

        Args:
            token:

        Returns:

        """
        return await User.repository.ger_user_by_email(token["username"])

    @staticmethod
    async def is_blacklisted(token: Token) -> None:
        """

        Args:
            token:

        Raises:

        Returns:

        """
        is_token_blacklisted = await JwtToken.repository.is_blacklisted(token[Token.jti_claim])
        if is_token_blacklisted:
            raise TokenError("Token is black listed")

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
            user=user,
        )
        return token

    @staticmethod
    async def revoke_refresh_token(user: User, refresh_token: RefreshToken):
        jwt_token = await JwtToken.repository.get_token_by_user(user, refresh_token)
        if not jwt_token:
            return jwt_token

        if jwt_token.is_blacklisted:
            return jwt_token

        return await JwtToken.repository.blacklist_token(jwt_token, refresh_token)
