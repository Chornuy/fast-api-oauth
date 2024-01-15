class OAuthFlowError(Exception):
    pass


class AuthCodeNotFound(OAuthFlowError):
    pass


class WrongAuthCode(OAuthFlowError):
    pass
