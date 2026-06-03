class TokenError(Exception):
    pass


class InvalidJwtTokenError(TokenError):
    pass
