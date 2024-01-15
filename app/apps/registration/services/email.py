from app.apps.registration.app import templates_path
from app.core.email.conf import get_email_conf
from app.core.email.send_email import send_email_async

VERIFICATION_SUBJECT = "Verification email"
RESET_PASSWORD = "Reset password"


async def send_verification_email(email: str, verification_token_url: str) -> None:
    """

    Args:
        email:
        verification_token_url:

    Returns:

    """
    conf = get_email_conf(template_path=templates_path)
    body = {
        "verification_token_url": verification_token_url
    }

    return await send_email_async(
        subject=VERIFICATION_SUBJECT,
        template_name="email.html",
        conf=conf,
        email_to=email,
        body=body
    )


async def send_reset_password_email(email: str, reset_password_token_url: str) -> None:
    """

    Args:
        email:
        reset_password_token_url:

    Returns:

    """
    conf = get_email_conf(template_path=templates_path)
    body = {
        "reset_password_token_url": reset_password_token_url
    }

    return await send_email_async(
        subject=VERIFICATION_SUBJECT,
        template_name="reset_password.html",
        conf=conf,
        email_to=email,
        body=body
    )
