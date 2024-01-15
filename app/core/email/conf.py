from fastapi_mail import ConnectionConfig

from app.settings.settings import settings


def get_email_conf(template_path: str) -> ConnectionConfig:
    """

    Args:
        template_path:

    Returns:

    """
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.EMAIL_USERNAME,
        MAIL_PASSWORD=settings.EMAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_FROM,
        MAIL_PORT=settings.EMAIL_PORT,
        MAIL_SERVER=settings.EMAIL_HOST,
        MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
        MAIL_SSL_TLS=settings.EMAIL_MAIL_SSL,
        USE_CREDENTIALS=settings.EMAIL_USE_CREDENTIALS,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        TIMEOUT=10,
        MAIL_DEBUG=True,
        TEMPLATE_FOLDER=template_path
    )
    return conf
