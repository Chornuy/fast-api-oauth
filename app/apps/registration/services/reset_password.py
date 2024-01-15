from starlette.requests import Request

from app.apps.registration.api.schemas import UserEmailScheme, UserResetPasswordScheme
from app.apps.registration.services.email import send_reset_password_email
from app.apps.user.models import User
from app.core.auth.verification_token import create_token, verify_token
from app.core.exceptions.validation import CustomValidationException
from app.libs.odm_repository.exceptions import ObjectNotFound


async def generate_reset_password_token(user_email_scheme: UserEmailScheme, request: Request) -> User:
    """

    Args:
        user_email_scheme:
        request:

    Returns:

    """
    user = await User.repository.ger_user_by_email(user_email_scheme.email)
    if not user:
        raise CustomValidationException(
            loc=("email",),
            msg="Invalid user email"
        )

    reset_password_token_url = str(
        request.url_for(
            "reset_password",
            reset_password_token=create_token(user.email)
        )
    )

    await send_reset_password_email(user.email, reset_password_token_url)
    return user


async def user_reset_password(reset_password_token: str, reset_password_scheme: UserResetPasswordScheme) -> User:
    """

    Args:
        reset_password_token:
        reset_password_scheme:

    Returns:

    """
    email = verify_token(reset_password_token)
    if not email:
        raise CustomValidationException(
            loc=("reset_password_token",),
            msg="Invalid reset token"
        )

    try:
        user = await User.repository.reset_password_by_email(
            email=email, password=reset_password_scheme.password
        )
    except ObjectNotFound:
        raise CustomValidationException(
            loc=("reset_password_token",),
            msg="Invalid reset token"
        )

    return user
