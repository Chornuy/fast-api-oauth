from typing import TYPE_CHECKING


from app.libs.odm_repository.exceptions import ObjectNotFound
from app.libs.odm_repository.repository import BaseRepository

if TYPE_CHECKING:
    from app.apps.user.models import User


class UserRepository(BaseRepository):

    async def ger_user_by_email(self, email: str):
        """

        Args:
            email:

        Returns:

        """
        return await self.get_document().find_one(self.get_document().email == email)

    async def create_user(self, **kwargs) -> "User":
        """

        Args:
            **kwargs:

        Returns:

        """
        if kwargs.get(self.get_document().password):
            kwargs["password"] = self.get_document().make_password(kwargs["password"])

        model_object = self.get_document()(**kwargs)
        await model_object.save()
        return model_object

    async def reset_password_by_email(self, password: str, email: str) -> "User":
        """

        Args:
            password:
            email:

        Returns:

        """
        user = await self.ger_user_by_email(email)
        if not user:
            raise ObjectNotFound()

        user.password = self.get_document().make_password(password)
        await user.save()

        return user
