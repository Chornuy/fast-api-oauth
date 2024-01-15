from pathlib import Path


class BaseLoaderMiddleware:
    @staticmethod
    def python_file_path_to_module_path(base_dir: Path, app_folder: str) -> str:
        """Method convert system path to python module to import module str.

        Examples:
            Usage example
            ```
                app_folder = "apps/user/app.py"
                base_dir = Path('/var/app/')
                python_module_path =AutoImportAppLoader.python_file_path_to_module_path(base_dir, app_folder)
                print(python_module_path)
                module = import_module(python_module_path)
            ```

        Args:
            base_dir (Path): dir of application
            app_folder (str): path to app module that need to import

        Returns:
            str: Import module str, like 'app.apps.user'
        """
        return app_folder.replace(str(base_dir), "").replace("/", ".").replace(".py", "")[1:]

    def load(self, context: dict, config: dict):
        raise NotImplementedError("Method Load should be implemented")
