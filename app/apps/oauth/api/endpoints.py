from typing import Annotated

from fastapi import APIRouter, Depends, Form

from app.apps.login.api.endpoints import oauth_manager
from app.apps.oauth.api.shemes import (
    OauthScheme,
    TokenPair,
    TokenRevokeScheme,
    UserResponseScheme,
)
from app.apps.user.models import User
from app.core.dependency.security import get_current_user
from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session

router = APIRouter()


@router.post("/token", response_model=TokenPair, response_model_exclude_unset=True)
@auto_session
@transaction.atomic
async def token(form_data: Annotated[OauthScheme, Form()]):
    """

    Args:
        form_data:

    Returns:

    """
    return await oauth_manager.process_flow(**form_data.model_dump(exclude_none=True, exclude_unset=True))


@router.post("/revoke")
@auto_session
@transaction.atomic
async def revoke(
    user: Annotated[User, Depends(get_current_user)],
    revoke_model: Annotated[TokenRevokeScheme, Form()],
):
    await oauth_manager.revoke_token(user=user, **revoke_model.model_dump(exclude_none=True, exclude_unset=True))
    return {}


@router.post("/me", response_model=UserResponseScheme)
@auto_session
@transaction.atomic
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
