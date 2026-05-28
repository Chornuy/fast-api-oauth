class LoaderError(Exception):
    """Base Loader exception"""

    pass


class NotInstanceOfBaseMiddlewareError(Exception):
    """Raised when middleware is not subclass of"""


class AppNameAlreadyRegisteredError(LoaderError):
    """Raised when multiple app registered with the same name"""

    pass


class SkipMiddlewareError(LoaderError):
    """Called in case need to skip middleware processing"""

    pass


class RuntimeMiddlewareError(LoaderError):
    """Raised in case internal error"""

    pass
