import asyncclick as click
from manage import fast_api_cli


@fast_api_cli.command("send_email")
@click.option('--user_id')
async def hello_world():
    print("hello world")
