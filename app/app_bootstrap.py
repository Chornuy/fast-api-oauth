from app.libs.app_loader.bootstrap import ApplicationBootStrap
from app.settings.settings import settings

bootstrap = ApplicationBootStrap(base_dir=settings.BASE_DIR, app_dir=settings.APPS_DIR)
