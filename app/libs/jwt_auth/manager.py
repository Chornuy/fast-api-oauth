from typing import Any

from app.libs.jwt_auth.tokens import AccessToken, RefreshToken, Token, UntypedToken


class BaseTokenManager:
    async def transform_token(self, token: Token) -> Any:
        raise NotImplementedError("Black list should be implemented") from None

    async def set_token_data(self, data: Any, token: RefreshToken) -> RefreshToken:
        raise NotImplementedError("Set token data should be implemented") from None


class RefreshTokenManager(BaseTokenManager):
    refresh_token_class = RefreshToken
    access_token_class = AccessToken
    untyped_token_class = UntypedToken

    def get_refresh_token_from_str(self, refresh_token: str) -> RefreshToken:
        return self.refresh_token_class(refresh_token)

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

    @staticmethod
    async def refresh_token(refresh_token: RefreshToken) -> dict[str, str]:
        """

        Args:
            refresh_token:

        Returns:

        """

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

    async def verify_token(self, token: str) -> UntypedToken:
        """

        Args:
            token:

        Returns:

        """
        return self.untyped_token_class(token)
