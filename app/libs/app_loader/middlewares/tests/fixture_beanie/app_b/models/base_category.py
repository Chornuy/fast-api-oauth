from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel


class Vehicle(Document):
    color: str

    class Settings:
        is_root = True


class Fuelled(BaseModel):
    """Just a mixin"""

    fuel: Optional[str]


class Car(Vehicle, Fuelled):
    body: str


class Owner(Document):
    vehicles: Optional[List[Link[Vehicle]]]
