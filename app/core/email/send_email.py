from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


async def send_email_async(
    subject: str, email_to: str, template_name: str, conf: ConnectionConfig, body: dict | None = None
) -> None:
    """

    Args:
        subject:
        email_to:
        body:
        template_name:
        conf:

    Returns:

    """
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body={"body": body},
        subtype="html",
    )

    fm = FastMail(conf)
    return await fm.send_message(message, template_name=template_name)
