import os

import uvicorn
from fastapi import FastAPI, APIRouter
import asyncclick as click
from app.libs.click_cli.bootstrap_cli import pass_fast_api
from app.libs.utils.managment import get_fast_api_cli, FAST_API_APP_ENV_NAME


fast_api_cli = get_fast_api_cli()


@fast_api_cli.command()
@pass_fast_api
async def show_urls(fast_api: FastAPI):
    for route in fast_api.routes:

        methods = ",".join(route.methods)
        tags_str = ""
        if isinstance(route, APIRouter):
            router_tags = ",".join(route.tags)
            tags_str = f", Tags: {router_tags}"

        click.echo(f"Path: {route.path}, Name: {route.name}, Method: {methods}{tags_str}")


@fast_api_cli.command()
@pass_fast_api
async def run_server(fast_api: FastAPI):
    uvicorn.run(os.environ.get(FAST_API_APP_ENV_NAME), host="0.0.0.0", port=8001, reload=True)
