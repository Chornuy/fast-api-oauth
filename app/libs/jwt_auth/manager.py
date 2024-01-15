from typing import Any

from app.libs.jwt_auth.tokens import AccessToken, RefreshToken, Token, UntypedToken


class BaseTokenManager:
    async def transform_token(self, token: Token) -> Any:
        raise NotImplementedError("Black list should be implemented")

    async def is_blacklisted(self, token: Token):
        raise NotImplementedError("Black list should be implemented")

    async def set_token_data(self, data: Any, token: RefreshToken) -> RefreshToken:
        raise NotImplementedError("Set token data should be implemented")

    async def token_to_blacklist(self, token: RefreshToken):
        raise NotImplementedError("blacklist data should be implemented")


class RefreshTokenManager(BaseTokenManager):
    refresh_token_class = RefreshToken
    access_token_class = AccessToken

    async def create_token_pair(self, data: Any) -> dict[str, str]:
        """

        Args:
            data:

        Returns:

        """
        refresh_token = self.refresh_token_class()
        refresh_token = await self.set_token_data(data, refresh_token)
        access_token = refresh_token.access_token
        return {
            "refresh_token": str(refresh_token),
            "access_token": str(access_token),
            "expires_in": access_token["exp"],
        }

    async def refresh_token(self, token: str) -> dict[str, str]:
        """

        Args:
            token:

        Returns:

        """

        refresh_token = self.refresh_token_class(token)
        access_token = refresh_token.access_token
        return {"access_token": str(access_token), "expires_in": access_token["exp"]}

    async def decode_token(self, token: str) -> Any:
        """

        Args:
            token:

        Returns:

        """
        token = self.access_token_class(token)
        return await self.transform_token(token)

    async def verify_token(self, token: str) -> dict:
        """

        Args:
            token:

        Returns:

        """
        token = UntypedToken(token)
        await self.is_blacklisted(token)
        return {}

    async def blacklist(self, token: str) -> Token:
        refresh_token = self.refresh_token_class(token)
        await self.token_to_blacklist(refresh_token)
        return refresh_token
