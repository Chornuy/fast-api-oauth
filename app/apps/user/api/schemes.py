from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class UserResponseScheme(BaseModel):
    _id: PydanticObjectId = Field(alias="id")
    email: str
