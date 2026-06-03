from beanie import Document, Link
from pydantic import BaseModel


class Vehicle(Document):
    color: str

    class Settings:
        is_root = True


class Fuelled(BaseModel):
    """Just a mixin"""

    fuel: str | None


class Car(Vehicle, Fuelled):
    body: str


class Owner(Document):
    vehicles: list[Link[Vehicle]] | None
