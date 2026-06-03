class OAuthFlowError(Exception):
    pass


class AuthCodeNotFoundError(OAuthFlowError):
    pass


class WrongAuthCodeError(OAuthFlowError):
    pass


class UnknownTokenError(OAuthFlowError):
    pass


class WrongTokenTypeError(OAuthFlowError):
    pass


class UnsupportedTokenTypeError(OAuthFlowError):
    pass
