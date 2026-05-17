from pydantic import BaseModel, EmailStr, Field, model_validator

from app.core.pydantic.fields import PasswordSecret


class UserEmailScheme(BaseModel):
    email: EmailStr = Field(title="User email")


class PasswordSchemeMixin(BaseModel):
    password: PasswordSecret = Field(min_length=8, max_length=20, alias="password1")
    password2: PasswordSecret = Field(min_length=8, max_length=20)

    @model_validator(mode="after")
    def validate_two_passwords(self) -> "PasswordSchemeMixin":
        """

        Returns:

        """
        pw1 = self.password.get_secret_value()
        pw2 = self.password2.get_secret_value()

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class UserRegistrationScheme(UserEmailScheme, PasswordSchemeMixin):
    pass


class UserResetPasswordScheme(PasswordSchemeMixin):
    pass
