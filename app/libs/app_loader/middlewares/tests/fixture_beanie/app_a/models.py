from typing import Optional, List

from beanie import Document, Link, UnionDoc, View
from pydantic import BaseModel, Field


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


class Parent(UnionDoc):  # Union
    class Settings:
        name = "union_doc_collection"  # Collection name
        class_id = "_class_id"  # _class_id is default beanie internal field used to filter children Documents


class One(Document):
    int_field: int = 0
    shared: int = 0

    class Settings:
        name = "One"  # Name used to filer union document 'One', default to class name
        union_doc = Parent


class Two(Document):
    str_field: str = "test"
    shared: int = 0

    class Settings:
        union_doc = Parent


class Bike(Document):
    type: str
    frame_size: int
    is_new: bool


class Metrics(View):
    type: str = Field(alias="_id")
    number: int
    new: int

    class Settings:
        source = Bike
        pipeline = [
            {
                "$group": {
                    "_id": "$type",
                    "number": {"$sum": 1},
                    "new": {"$sum": {"$cond": ["$is_new", 1, 0]}}
                }
            },
        ]
