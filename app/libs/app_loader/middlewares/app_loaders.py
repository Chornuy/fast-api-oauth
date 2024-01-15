import glob
import logging
from pathlib import Path

from app.libs.app_loader.middlewares.base import BaseLoaderMiddleware
from app.libs.app_loader.middlewares.exceptions import AppNameAlreadyRegistered
from app.utils.module_loading import cached_import_class

logger = logging.getLogger(__name__)


class AutoImportAppLoader(BaseLoaderMiddleware):
    """Class helper to load a basic list apps with their

    """

    app_name_attr_name = "app_name"
    app_python_file_name = "app.py"
    application_patter = "*/app.py"

    def get_app_folder_list(self, app_dir: Path) -> list[str]:
        """Method scan all apps, dir that contains app.py file inside module.
        Examples:
            apps/
                user/app.py
                user/commands/
                user/models.py

                authentication/app.py
                authentication/models/__init__.py

                web_client/service.py

            Will return result:
                apps = [
                    "apps/user",
                    "apps/authentication
                ]

        Args:
            app_dir(Path): path to folder with apps

        Returns:
            list: list of apps that contains app.py inside
        """
        return glob.glob(fr"{app_dir}/{self.application_patter}")

    def load_apps(self, base_dir: Path, app_folders: list) -> dict[str, dict]:
        """Register system data for each app, to make easy loading of another pipelines

        Args:
            base_dir (Path):
            app_folders (Path):

        Raises:
            AppNameAlreadyRegistered: Raises when system detect two apps modules with same app_name

        Returns:
            dict:
        """

        apps = {}

        for app_folder in app_folders:
            try:
                app_config = self.build_app_config(base_dir, app_folder)
            except AttributeError:
                logger.debug(
                    f"Module name: {app_folder} found app.py, but has no `app_name` variable."
                    f" Set up `app_name=` for discover auto-loading for app "
                    f" Skipping..."
                )
                continue

            if app_config["name"] in apps.keys():
                raise AppNameAlreadyRegistered()

            apps[app_config["name"]] = app_config

        return apps

    def build_app_config(self, base_dir: Path, app_folder: str) -> dict:
        """Method generate base config for apps, for future processing of autoloader

        Args:
            base_dir (Path): path to the root of project
            app_folder (str): Path to target app module

        Examples:
            Will transform python module with struction like:

            ```
                apps/
                    user/app.py
                    user/commands/
                    user/models.py
            ```
            to config
            ```
                {
                    'user': {
                        'name': 'user',
                        'module_path': 'app.apps.user',
                        'folder_path': PosixPath('/var/app/app/apps/user')
                    }
                }
        Returns:
            dict: with app base config
        """

        app_module = self.python_file_path_to_module_path(base_dir=base_dir, app_folder=app_folder)

        app_name = cached_import_class(app_module, self.app_name_attr_name)

        module_name = self.app_python_file_name.replace(".py", "")
        app_module_path = app_module[:-len(f".{module_name}")]

        return {
            "name": app_name,
            "module_path": app_module_path,
            "folder_path":  Path(app_folder.replace(self.app_python_file_name, ""))
        }

    def load(self, context: dict, config: dict) -> dict:
        """Method will scan base dir of application and get all python modules that got application struction, and
        register config of app to context

        Args:
            config (dict): Base config of bootstrap class
            context (dict): context dict, object that pass to all middleware and register result of middleware

        Returns:
            dict: context with set up list of apps for application
        """

        app_folders = self.get_app_folder_list(context["bootstrap_config"]["app_dir"])
        apps_configs = self.load_apps(app_folders=app_folders, base_dir=context["bootstrap_config"]["base_dir"])
        context["apps"] = apps_configs
        return context
