from app.app_bootstrap import bootstrap
from app.libs.click_cli.bootstrap_cli import FastApiCliBootStrap

fast_api_cli = FastApiCliBootStrap(bootstrap=bootstrap)
