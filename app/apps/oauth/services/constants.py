from enum import Enum


class TokenType(str, Enum):
    refresh_token: str = "refresh_token"
    access_token: str = "access_token"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
