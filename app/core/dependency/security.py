from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.apps.oauth.app import app_name
from app.apps.oauth.services.token_manager import UserTokenManager
from app.libs.jwt_auth.exceptions import InvalidJwtTokenError
from app.libs.jwt_auth.tokens import AccessToken

oauth2_auth_code_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"/{app_name}/token",
    authorizationUrl=f"/{app_name}/login",
    refreshUrl=f"/{app_name}/token",
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_access_token(token: Annotated[str, Depends(oauth2_auth_code_scheme)]):
    try:
        return AccessToken(token)
    except InvalidJwtTokenError:
        raise credentials_exception from None


async def get_current_user(access_token: Annotated[AccessToken, Depends(get_access_token)]):
    return await UserTokenManager.transform_token(access_token)
