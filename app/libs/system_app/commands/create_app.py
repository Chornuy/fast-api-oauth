#
# app_folder_template = {
#     PythonFile("app.py", template=""),
#     PythonFile("models.py", template=""),
#     PythonModule("api", struction={
#         PythonFile("schemes.py"),
#         PythonFile("endpoints.py")
#     }),
#     FolderStruction("events", struction={
#         PythonFile("schemes.py"),
#         PythonFile("events.py")
#     }),
#     PythonFile("router.py", template=""),
#     PythonFile("tasks.py"),
#     FolderStruction("commands")
# }
import os
from pathlib import Path

from app.libs.utils.managment import get_fast_api_cli
from app.settings.settings import settings


fast_api_cli = get_fast_api_cli()


class AppFactoryMeta(type):

    pass


class LocalFileManger:

    pass


class FileSystemFactory:

    python_module_filename = "__init__.py"

    def __init__(self, folder_path: Path, module_name: str):
        self.folder_path = folder_path
        self.module_name = module_name
        self.module_path = folder_path.joinpath(module_name)

    @staticmethod
    def exists(path: Path):
        return os.path.lexists(path)

    @staticmethod
    def create_folder(folder_name: Path):
        os.mkdir(folder_name)

    def create_file(self, path: Path, file_name: str):
        fh = open(path.joinpath(file_name))
        fh.close()

    def create_module(self):
        self.create_folder(self.module_path)
        self.create_file(self.module_path, self.python_module_filename)

    def verify(self):
        if not self.exists(self.folder_path):
            raise Exception("Path do not exist")

        if self.exists(self.module_path):
            raise Exception("Module already exists")

    def create(self):
        self.verify()
        self.create_module()


class PythonModuleFactory:
    pass


class AppFactory(metaclass=AppFactoryMeta):

    def __init__(self, app_name: str, folder_path: Path) -> None:
        self.app_name = app_name
        self.folder_path = folder_path

    def create_python_module(self):
        pass

    def create(self):
        pass

    class Meta:
        factories = []


#
# class AppFactory:
#     pass
#
#     class Settings:
#         presets = {
#             "simple": {
#
#             }
#         }
#
#
@fast_api_cli.command()
def create_app():

    fs_factory = FileSystemFactory(folder_path=settings.APPS_DIR, module_name="sandbox")
    fs_factory.create()
#     AppFactory(app_name=, app_folder_dir=)
