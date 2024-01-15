from app.libs.app_loader.middlewares.base import BaseLoaderMiddleware
from app.libs.app_loader.middlewares.exceptions import SkipMiddlewareException


class FixtureTestMiddleware(BaseLoaderMiddleware):

    def load(self, context: dict, config: dict):
        context["testing_result"] = "ok"
        return context


class FixtureTestResultAfterTestMiddleware(BaseLoaderMiddleware):
    def load(self, context: dict, config: dict):
        testing_result = context["testing_result"]
        context["testing_result_another"] = f"{testing_result}.ok"
        return context


class AnotherClass:
    pass


class FixtureWrongSubclassMiddleware(AnotherClass):

    def load(self, context: dict, config: dict):
        pass


class NotImplementLoadMethodMiddleware(BaseLoaderMiddleware):
    def some_method(self):
        pass


class SkippableLoaderMethodMiddleware(BaseLoaderMiddleware):

    def load(self, context: dict, config: dict):
        raise SkipMiddlewareException("skip")
