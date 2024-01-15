from starlette.requests import Request

from app.apps.registration.api.schemas import UserRegistrationScheme
from app.apps.registration.services.email import send_verification_email
from app.apps.user.models import User
from app.apps.user.repository import UserRepository
from app.core.auth.verification_token import create_token, verify_token
from app.core.exceptions.validation import CustomValidationException


async def register_user(user_register_scheme: UserRegistrationScheme, request: Request) -> User:
    """

    Args:
        user_register_scheme:
        request:
    Returns:

    """
    user = await User.repository.ger_user_by_email(user_register_scheme.email)
    if user:
        raise CustomValidationException(
            loc=("email",),
            msg="email already registered"
        )

    user = await User.repository.create_user(**user_register_scheme.model_dump())

    verification_url = str(request.url_for("verify", verification_token=create_token(user.email)))

    await send_verification_email(email=user.email, verification_token_url=verification_url)
    return user


async def verify_user(verification_token: str) -> User:
    """

    Args:
        verification_token:

    Returns:

    """
    email = verify_token(verification_token)
    if not email:
        raise CustomValidationException(
            loc=("verification_token",),
            msg="Invalid verification token"
        )

    user = await User.repository.ger_user_by_email(email)
    if user.verified:
        return user

    user.verified = True
    await user.save()

    return user
