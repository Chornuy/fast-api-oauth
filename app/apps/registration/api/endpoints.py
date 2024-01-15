from typing import Annotated

from fastapi import APIRouter, Path
from starlette.requests import Request

from app.apps.registration.api.schemas import UserEmailScheme, UserRegistrationScheme, UserResetPasswordScheme
from app.apps.registration.services.registration import register_user, verify_user
from app.apps.registration.services.reset_password import generate_reset_password_token, user_reset_password
from app.core.schemas.actions import SuccessAction

router = APIRouter()


@router.post("/register", response_model=SuccessAction)
async def register(user_register_scheme: UserRegistrationScheme, request: Request) -> dict:
    """

    Args:
        user_register_scheme:
        request:

    Returns:

    """
    user = await register_user(user_register_scheme, request)
    return {"resource_id": str(user.id), "message": "Hello world"}


@router.get("/verify/{verification_token}", response_model=SuccessAction)
async def verify(
    verification_token: Annotated[str, Path(title="Verification token for user ", min_length=1, max_length=200)],
) -> dict:
    """

    Args:
        verification_token:

    Returns:

    """

    user = await verify_user(verification_token)

    return {"resource_id": str(user.id), "message": "User successfully validated"}


@router.post("/reset-password", response_model=SuccessAction)
async def reset_password_verify(user_email_scheme: UserEmailScheme, request: Request) -> dict:
    """

    Args:
        request:
        user_email_scheme:

    Returns:

    """
    user = await generate_reset_password_token(user_email_scheme, request)
    return {"resource_id": str(user.id), "message": "Verification of password send to email"}


@router.post("/reset-password/{reset_password_token}", response_model=SuccessAction)
async def reset_password(
    reset_password_token: Annotated[str, Path(title="Reset token for user", min_length=1, max_length=200)],
    user_reset_password_scheme: UserResetPasswordScheme,
) -> dict:
    """

    Args:
        user_reset_password_scheme:
        reset_password_token:

    Returns:

    """

    user = await user_reset_password(reset_password_token, user_reset_password_scheme)

    return {"resource_id": str(user.id), "message": "Password successful reset"}
