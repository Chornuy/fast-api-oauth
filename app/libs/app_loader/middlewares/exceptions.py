
class LoaderException(Exception):
    """Base Loader exception"""
    pass


class NotInstanceOfBaseMiddleware(Exception):
    """Raised when middleware is not subclass of """


class AppNameAlreadyRegistered(LoaderException):
    """Raised when multiple app registered with the same name
    """

    pass


class SkipMiddlewareException(LoaderException):
    """Called in case need to skip middleware processing
    """
    pass


class RuntimeMiddlewareException(LoaderException):
    """Raised in case internal error
    """
    pass
