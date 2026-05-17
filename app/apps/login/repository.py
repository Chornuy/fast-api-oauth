from datetime import datetime
from typing import TYPE_CHECKING

from beanie.odm.operators.find.comparison import Eq

from app.apps.user.models import User
from app.libs.beanie_odm_ext.repository import BaseRepository
from app.libs.jwt_auth.tokens import Token
from app.libs.utils.datetime import datetime_from_epoch

if TYPE_CHECKING:
    from beanie.odm.documents import JwtToken


class JwtTokenRepository(BaseRepository):
    """ """

    async def is_blacklisted(self, jti: str) -> bool:
        """

        Args:
            jti (str):

        Returns:
            bool:
        """
        token = await self.get_document().find_one(
            self.get_document().jti == jti, Eq(self.get_document().is_blacklisted, True)
        )
        return True if token else False

    async def blacklist(self, token: str, jti: str, expire_at: datetime) -> "JwtToken":
        """

        Args:
            expire_at:
            jti:
            token:

        Returns:

        """

        token_obj = await self.get_or_create(
            self.get_document().jti == jti, defaults={"token": token, "jti": jti, "expire_at": expire_at}
        )
        token_obj.is_blacklisted = True
        await token_obj.save()
        return token_obj

    @staticmethod
    async def blacklist_token(token_document: "JwtToken", token: Token) -> "JwtToken":
        token_document.is_blacklisted = True
        token_document.expire_at = datetime_from_epoch(token["exp"])
        await token_document.save()
        return token_document

    async def get_token_by_user(self, user: User, jti: str) -> "JwtToken":
        token = await self.get_document().find_one(
            self.get_document().jti == jti, self.get_document().user.id == user.id
        )
        return token


class OAuthCodeRepository(BaseRepository):

    async def get_code(self, code: str):
        """

        Args:
            code(str):

        Raises:
            DocumentNotFound

        Returns:

        """
        return await self.find_one_or_error(self.get_document().code == code)
