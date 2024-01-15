from datetime import datetime, timedelta
from typing import Annotated, ClassVar

from beanie import Indexed, Link
from pydantic import HttpUrl

from app.apps.oauth.repository import JwtTokenRepository, OAuthCodeRepository
from app.apps.user.models import User
from app.libs.odm_repository.metadata import DocumentRepository
from app.libs.token_generator.generator import generate_token

DEFAULT_CODE_TIMEOUT = timedelta(hours=1)


class JwtToken(DocumentRepository):

    # Unique id of Jwt token
    jti: Annotated[str, Indexed(unique=True)]

    # Jwt token str
    token: str

    # Date of creation of token
    created_at: datetime = datetime.now()

    # Date of expire
    expire_at: datetime

    # Is token was blacklisted
    is_blacklisted: bool = False

    # Date of blacklisting
    blacklisted_at: datetime | None = None

    repository: ClassVar = JwtTokenRepository()


class OAuthCode(DocumentRepository):

    # Unique code for obtaining access token
    code: Annotated[str, Indexed(unique=True)] = generate_token()

    # redirect uri from original request
    redirect_uri: HttpUrl

    # Date of creation of code
    created_at: datetime = datetime.now()
    # Date when code will be expired
    expire_at: datetime = datetime.now() + DEFAULT_CODE_TIMEOUT

    # If code was checked but not pass other validation
    already_checked: bool = False

    # User that initialize code verification
    user: Link[User]

    repository: ClassVar = OAuthCodeRepository()

    async def get_user(self):
        if isinstance(self.user, Link):
            await self.fetch_link(OAuthCode.user)

        return self.user

    def is_expire(self, datetime_obj: datetime = datetime.now()) -> bool:
        """ Check if auth code is expired

        Args:
            datetime_obj (datetime): datetime object based on which will be checked token

        Returns:
            bool: is code already expired
        """
        return self.expire_at > datetime_obj

    async def is_valid(self, redirect_uri: str, datetime_obj: datetime = datetime.now()) -> bool:
        """General code check.
        Checks if code was expired, and if it was not successfully checked

        Args:
            redirect_uri (str): redirect_uri form client
            datetime_obj (datetime): datetime object to check if expired

        Returns:
            bool: Is token is valid
        """
        if not self.is_expire(datetime_obj) and not self.already_checked and self.redirect_uri == redirect_uri:
            self.already_checked = True
            await self.save()
            return False

        return True

