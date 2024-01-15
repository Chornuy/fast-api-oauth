import asyncclick as click
from pymongo.client_session import ClientSession

from app.apps.registration.app import templates_path
from app.apps.registration.services.email import send_verification_email
from app.core.email.conf import get_email_conf
from manage import fast_api_cli


@fast_api_cli.command("show_users")
@click.option('--port', default=8000)
async def show_all_users(port):
    print("hello world")


@fast_api_cli.command("send_email")
async def send_email():
    print(templates_path)
    config = get_email_conf(template_path=templates_path)
    print(config.model_dump())
    #
    await send_verification_email(email="vasya@gmail.com", verification_token_url="aasdasd")

    session = ClientSession()
    with session.start_transaction():
        pass

