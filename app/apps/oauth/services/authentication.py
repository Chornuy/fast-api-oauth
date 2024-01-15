from app.apps.user.models import User


async def authenticate_user(username: str, password: str) -> User | bool:
    """

    Args:
        username:
        password:

    Returns:

    """
    user = await User.repository.ger_user_by_email(username)
    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user
