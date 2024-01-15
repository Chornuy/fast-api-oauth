from pathlib import Path

from app.libs.app_loader.middlewares.base import BaseLoaderMiddleware
from app.libs.app_loader.middlewares.exceptions import RuntimeMiddlewareException


class ClickCommandLoader(BaseLoaderMiddleware):
    """Class helper to load all commands that was registered inside apps struct"""

    commands_patter = r"commands/[!__init__]*.py"
    commands_module_name = "commands"

    # Additional commands that not a part of application itself
    additional_cli_modules = ["app.libs.system_app.commands.fast_api_commands"]

    def get_python_files_commands(self, app_folder_path: str) -> list[Path]:
        """Load all files that was registered inside commands module.
        Examples:
            with app struction like:
                apps/user/commands/__init__.py
                apps/user/commands/user_management.py
                apps/user/commands/create_superuser.py

            will produce a list with values:
            [
                "apps/user/commands/user_management.py",
                "apps/user/commands/create_superuser.py"
            ]

        Args:
            app_folder_path:

        Returns:
            list[PosixPath]:
        """
        return list(Path(app_folder_path).glob(self.commands_patter))

    def command_paths_to_module_str(self, base_dir: Path, command_paths: list[Path]) -> list[str]:
        """Convert file path to python module import str
        Examples:
            commands_list = ["apps/user/commands/user_management.py", "apps/user/commands/create_superuser.py"]
            will transform to ["apps.user.commands.user_management", "apps.user.commands.create_superuser"]

        Args:
            base_dir (Path): Base dir of application
            command_paths (list): list of file paths to moduls with commands

        Returns:
            list: python modules with commands
        """

        return [
            self.python_file_path_to_module_path(base_dir=base_dir, app_folder=str(commands_file))
            for commands_file in command_paths
        ]

    def load(self, context: dict, config: dict) -> dict:
        """Method will check all apps for folder with name commands, and will return a list of python modules
        with potential commands for application

        Args:
            config (dict): Base config of bootstrap class
            context (dict): context dict, object that pass to all middleware and register result of middleware


        Returns:
            context: with setup "commands_modules", with list of modules with potential commands for app
        """

        try:
            app_list = context["apps"]
        except KeyError:
            raise RuntimeMiddlewareException(
                "app key missing in result dict, ClickCommandLoader middleware depends"
                " on AutoImportAppLoader middleware, and should run after it"
            )

        commands_file_paths = []

        for app_config in app_list.values():
            commands_files_list = self.get_python_files_commands(app_config["folder_path"])
            commands_file_paths.extend(commands_files_list)

        commands_modules = self.command_paths_to_module_str(
            base_dir=context["bootstrap_config"]["base_dir"], command_paths=commands_file_paths
        )
        commands_modules.extend(self.additional_cli_modules)

        context["commands_modules"] = commands_modules
        return context
