from pathlib import Path

app_name = "oauth"

route_prefix = app_name
app_path = Path(__file__).parent
templates_path = app_path.joinpath("templates")
