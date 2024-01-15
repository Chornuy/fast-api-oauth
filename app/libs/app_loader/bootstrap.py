import logging
from pathlib import Path

from app.libs.app_loader.middlewares.base import BaseLoaderMiddleware
from app.libs.app_loader.middlewares.exceptions import NotInstanceOfBaseMiddleware, SkipMiddlewareException
from app.utils.module_loading import import_string

logger = logging.getLogger(__name__)


DEFAULT_LOADER_PIPELINE = [
    "app.libs.app_loader.middlewares.app_loaders:AutoImportAppLoader",
    "app.libs.app_loader.middlewares.beanie:BeanieModelLoader",
    "app.libs.app_loader.middlewares.click:ClickCommandLoader",
]


class BootstrapState:
    """Helper class to save state of"""

    loaded = False


class ApplicationBootStrap:
    """"""

    def __init__(
        self,
        base_dir: Path,
        app_dir: Path,
        config: dict = None,
        ensure: bool = True,
        context: dict = None,
        loader_pipeline: list[str] = None,
    ):
        """

        Args:
            app_dir (Path):

        """

        self.app_dir = app_dir
        self.base_dir = base_dir
        self._state = BootstrapState()
        self.config = config or {}
        self._ensure = ensure
        self._context = context or {}
        self.loader_pipeline = loader_pipeline or DEFAULT_LOADER_PIPELINE.copy()
        self._loader_middlewares = []

    def make_context(self, context: dict) -> dict:
        """Create base context dict, for before start middlewares

        Args:
            context (dict): dict with basic settings for starting process a middlewares

        Returns:
            dict: dict with basic configs
        """
        context["bootstrap_config"] = {"app_dir": self.app_dir, "base_dir": self.base_dir}

        return context

    def load_pipelines(self):
        """Import cls objects before start application loading

        Returns:
            None:
        """
        for pipeline_import_str in self.loader_pipeline:
            pipeline_cls = import_string(pipeline_import_str, ":")

            if not issubclass(pipeline_cls, BaseLoaderMiddleware):
                raise NotInstanceOfBaseMiddleware(
                    f"Got class {pipeline_cls.__class__} " f"that is not subclass of {BaseLoaderMiddleware.__class__}"
                )

            self._loader_middlewares.append(pipeline_cls)

    def process_middlewares(self, context: dict):
        """Method run all middlewares that was registered in self._loader_middlewares attrs

        Args:
            context (dict): Context dict

        Returns:
            None

        """
        for middleware_cls in self._loader_middlewares:
            middleware_obj = middleware_cls()
            try:
                self._context = middleware_obj.load(context=context, config=self.config)
            except SkipMiddlewareException as e:
                logger.exception(e)

    def load(self) -> dict:
        """Method start processing of middlewares that helps to load apps struction.

        Returns:
            dict: context with loaded data for apps
        """
        self.load_pipelines()

        self._context = self.make_context(self._context)
        self.process_middlewares(self._context)
        self._state.loaded = True
        return self._context

    def is_loaded(self) -> bool:
        """Helper return current state of loading

        Returns:
            bool: state of loading
        """
        return self._state.loaded

    @property
    def context(self):
        """Descriptor, helper to ensure that data was loaded when accessing the context property

        Returns:
            dict: with data after processing middlewares
        """

        if not self._state.loaded and self._ensure:
            self.load()
        return self._context
