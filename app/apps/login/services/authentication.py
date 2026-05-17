from app.apps.user.models import User
from app.core.exceptions.validation import CustomValidationException


async def authenticate_user(username: str, password: str) -> User:
    """

    Args:
        username:
        password:

    Returns:

    """
    user = await User.repository.ger_user_by_email(username)
    if not user:
        raise CustomValidationException(loc=("email",), msg="Password of email wrong")

    if not user.verified:
        raise CustomValidationException(loc=("email",), msg="User not verified")

    if not user.verify_password(password):
        raise CustomValidationException(loc=("email",), msg="Password of email wrong")

    return user
