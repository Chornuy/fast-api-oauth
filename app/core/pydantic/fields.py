from typing import Any, Dict

from pydantic import SecretStr
from pydantic._internal._utils import update_not_none


class PasswordSecret(SecretStr):
    """Pydantic type for password"""

    special_chars = {
        "$",
        "@",
        "#",
        "%",
        "!",
        "^",
        "&",
        "*",
        "(",
        ")",
        "-",
        "_",
        "+",
        "=",
        "{",
        "}",
        "[",
        "]",
    }

    min_length = 8
    includes_special_chars = False
    includes_numbers = False
    includes_lowercase = False
    includes_uppercase = False

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: Dict[str, Any]) -> None:
        update_not_none(
            field_schema,
            minLength=cls.min_length,
            includesNumbers=cls.includes_numbers,
            includesLowercase=cls.includes_lowercase,
            includesUppercase=cls.includes_uppercase,
            includesSpecialChars=cls.includes_special_chars,
            specialChars=cls.special_chars,
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        if len(v) < cls.min_length:
            raise ValueError(f"length should be at least {cls.min_length}")

        if cls.includes_numbers and not any(char.isdigit() for char in v):
            raise ValueError("Password should have at least one numeral")

        if cls.includes_uppercase and not any(char.isupper() for char in v):
            raise ValueError("Password should have at least one uppercase letter")

        if cls.includes_lowercase and not any(char.islower() for char in v):
            raise ValueError("Password should have at least one lowercase letter")

        if cls.includes_special_chars and not any(char in cls.special_chars for char in v):
            raise ValueError(f"Password should have at least one of the symbols {cls.special_chars}")

        return cls(v)
