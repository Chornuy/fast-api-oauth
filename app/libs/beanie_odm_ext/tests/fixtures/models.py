# class Category(DocumentWithSession):

from beanie import Document, Indexed, Link


class Category(Document):
    name: str
    name: str
    description: str


class Product(Document):
    name: str
    description: str | None = None
    price: Indexed(typ=float)
    category: Link[Category]
