from enum import Enum


class GrantTypeEnum(str, Enum):
    refresh_token = "refresh_token"
    authorization_code = "authorization_code"
