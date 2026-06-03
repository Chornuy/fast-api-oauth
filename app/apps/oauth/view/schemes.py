from pydantic import BaseModel, EmailStr, Field, HttpUrl

from app.core.pydantic.fields import PasswordSecret


class LoginRequestForm(BaseModel):
    email: EmailStr = Field(max_length=320)
    password: PasswordSecret = Field(min_length=8)
    redirect_uri: HttpUrl
    state: str | None = None
