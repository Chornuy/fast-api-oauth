from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, ClassVar

from beanie import Indexed, before_event, Insert, Update
from pydantic import Field, EmailStr

from app.apps.user.repository import UserRepository
from app.core.auth.password_generator import verify_password, make_password
from app.libs.odm_repository.metadata import DocumentRepository


class UserRoles(str, Enum):
    super_user = "superuser"
    user = "user"


class User(DocumentRepository):

    name: Optional[str | None] = Field(max_length=200, default=None)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(max_length=200)
    password: str = Field(max_length=200)
    verified: bool = False
    roles: UserRoles = UserRoles.user.value
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)

    repository: ClassVar = UserRepository()

    @staticmethod
    def make_password(password: str) -> str:
        """

        Args:
            password:

        Returns:

        """
        return make_password(password)

    def verify_password(self, password: str) -> bool:
        """

        Args:
            password:

        Returns:

        """
        return verify_password(self.password, password)

    @before_event(Insert, Update)
    def updated_datetime(self):
        """

        Returns:

        """
        self.updated = datetime.now()

    class Settings:
        name = "user"
