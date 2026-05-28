from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form
from starlette.responses import RedirectResponse

from app.apps.login.api.shemes import CompleteFlowQuery
from app.apps.login.services.authentication import authenticate_user
from app.apps.oauth.api.shemes import TokenPair
from app.apps.oauth.services.oauth_manager import oauth_manager
from app.apps.oauth.view.schemes import LoginRequestForm
from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session

router = APIRouter()


@router.post("", response_class=RedirectResponse, status_code=302)
@auto_session
@transaction.atomic
async def login(login_form: Annotated[LoginRequestForm, Form()]):
    user = await authenticate_user(
        username=str(login_form.email),
        password=str(login_form.password.get_secret_value()),
    )

    code_obj = await oauth_manager.generate_authorization_code(redirect_uri=str(login_form.redirect_uri), user=user)
    query_params = {
        "code": code_obj.code,
        "redirect_uri": str(login_form.redirect_uri),
    }

    if login_form.state:
        query_params["state"] = login_form.state

    query_str = urlencode(query_params)
    redirect_url = f"{login_form.redirect_uri}?{query_str}"

    return redirect_url


@router.get("/complete", response_model=TokenPair, status_code=200)
@auto_session
@transaction.atomic
async def complete(complete_flow_query: Annotated[CompleteFlowQuery, Depends()]):
    token = await oauth_manager.authorization_code(
        redirect_uri=str(complete_flow_query.redirect_uri), code=complete_flow_query.code
    )

    return token
