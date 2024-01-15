from pathlib import Path


class AppLoader:
    def __init__(self, apps_folder: Path):
        self.apps_folder = apps_folder

        self.apps = []

    def load_apps(self):
        pass
