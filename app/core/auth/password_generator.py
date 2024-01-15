from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def make_password(password: str) -> str:
    """

    Args:
        password:

    Returns:

    """
    return pwd_context.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    """

    Args:
        plain_password (str):
        hashed_password (str):

    Returns:
        bool
    """
    return pwd_context.verify(plain_password, hashed_password)
