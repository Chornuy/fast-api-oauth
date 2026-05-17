# class Category(DocumentWithSession):
from typing import Optional

from beanie import Document, Indexed, Link


class Category(Document):
    name: str
    name: str
    description: str


class Product(Document):
    name: str
    description: Optional[str] = None
    price: Indexed(typ=float)
    category: Link[Category]
