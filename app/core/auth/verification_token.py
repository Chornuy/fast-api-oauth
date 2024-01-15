from itsdangerous import BadTimeSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import EmailStr

from app.settings.settings import settings

token_algo = URLSafeTimedSerializer(settings.SECRET_KEY, salt="Email_Verification_&_Forgot_password")


def create_token(email: EmailStr) -> str | bytes:
    """

    Args:
        email:

    Returns:

    """
    _token = token_algo.dumps(email)
    return _token


def verify_token(token: str) -> str | None:
    """

    Args:
        token:

    Returns:

    """
    try:
        email = token_algo.loads(token, max_age=1800)
    except SignatureExpired:
        return None
    except BadTimeSignature:
        return None

    return email
