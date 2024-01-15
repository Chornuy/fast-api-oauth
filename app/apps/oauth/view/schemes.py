from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.core.pydantic.decorator import as_form
from app.core.pydantic.fields import PasswordSecret


@as_form
class LoginRequestForm(BaseModel):
    email: EmailStr = Field(max_length=320)
    password: PasswordSecret = Field(min_length=8)
    redirect_uri: Optional[str] = None
    state: Optional[str] = None
