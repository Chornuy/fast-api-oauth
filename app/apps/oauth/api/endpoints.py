from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter
from fastapi.exceptions import ValidationException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from fastapi import Depends
from starlette.responses import RedirectResponse

from app.apps.oauth.api.shemes import TokenScheme, TokenPair, OauthScheme
from app.apps.oauth.app import app_name
from app.apps.oauth.services.authentication import authenticate_user
from app.apps.oauth.services.oauth_manager import OauthFlowManager
from app.apps.oauth.view.schemes import LoginRequestForm
from starlette.requests import Request

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{app_name}/token")
oauth2_auth_code_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"/{app_name}/token",
    authorizationUrl=f"/{app_name}/login",
    refreshUrl=f"/{app_name}/token"
)


oauth_manager = OauthFlowManager()


@router.post("/token", response_model=TokenPair)
async def token(
    form_data: OauthScheme = Depends(OauthScheme)
):
    """

    Args:
        form_data:

    Returns:

    """
    return await oauth_manager.process_flow(**form_data.model_dump())


@router.post("/revoke", response_model=TokenScheme)
async def revoke(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return {"access_token": form_data, "token_type": "bearer"}


@router.post("/me")
async def me(
    token: Annotated[str, Depends(oauth2_auth_code_scheme)]
):
    return {"status": "ok"}


def check_redirect_uri(redirect_uri: str):
    return True


@router.post("/login", response_class=RedirectResponse, status_code=302)
async def post_login(request: Request):
    try:
        login_form = LoginRequestForm(
            **await request.form()
        )
    except ValidationException as ex:
        print(ex)
        return {"status": "error"}

    user = await authenticate_user(username=login_form.email, password=str(login_form.password))

    check_redirect_uri(login_form.redirect_uri)

    code_obj = await oauth_manager.generate_authorization_code(redirect_uri=login_form.redirect_uri, user=user)
    query_params = {"code": code_obj.code}

    if login_form.state:
        query_params["state"] = login_form.state

    query_str = urlencode(query_params)
    redirect_url = f"{login_form.redirect_uri}?{query_str}"

    return redirect_url
