from importlib import import_module
from typing import List, Tuple, Type, TypeVar

from beanie import Document, UnionDoc, View

from app.libs.app_loader.middlewares.base import BaseLoaderMiddleware
from app.utils.module_loading import cached_import_module, module_has_submodule, get_module_subclasses

T = TypeVar('T')


class BeanieModelLoader(BaseLoaderMiddleware):
    """Class helper to load from apps models

    """

    models_module_name = "models"

    beanie_models_cls = (Document, UnionDoc, View)

    def check_has_models(self, module_path: str) -> bool:
        """ Method check if python app module has a submodule with models.py inside
        If it has it, this is our target to autoload models from app module

        Args:
            module_path (str): str with python path to module, example: "app.apps.user"

        Returns:
            bool: if module has submodule models.py
        """

        app_config_module = cached_import_module(module_path)
        return module_has_submodule(app_config_module, self.models_module_name)

    def import_module_models(self, module_path: str) -> List[Tuple[str, Type]]:
        """Build from pythonic path like "app.apps.user" to "app.apps.user.modules", and get all
        subclasses of Models ODM that was registered inside

        Returns:
            List[Tuple[str, Type]]: List with tuple where first key is name of class and second class object
        """

        models_module_str = f"{module_path}.{self.models_module_name}"
        models_module = import_module(models_module_str)
        return get_module_subclasses(models_module, self.beanie_models_cls)

    def load(self, context: dict, config: dict) -> dict:
        """ Autoloads Beanie models that stored inside models module, of applications modules

        Args:
            config (dict): Base config of bootstrap class
            context (dict): context dict, object that pass to all middleware and register result of middleware


        Returns:
            dict: Update context dict with set up key, of all models that was found inside the project
        """
        app_list = context["apps"]
        model_list = []
        for app_config in app_list.values():
            if self.check_has_models(app_config["module_path"]):
                models = self.import_module_models(app_config["module_path"])
                model_list.extend(models)

        model_list = [model_cls for _, model_cls in model_list]
        context['beanie_models'] = model_list
        return context
