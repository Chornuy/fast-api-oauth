from pydantic import Field

from beanie import Document, View


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
