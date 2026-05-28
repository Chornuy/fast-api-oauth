from enum import Enum
from typing import Annotated  # type: ignore [attr-defined]
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, Query
from fastapi.responses import HTMLResponse
from pydantic import HttpUrl
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing_extensions import Doc

from app.apps.login.services.authentication import authenticate_user
from app.apps.login.view.schemes import LoginRequestForm
from app.apps.oauth.app import templates_path
from app.apps.oauth.services.oauth_manager import oauth_manager
from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session

templates = Jinja2Templates(directory=templates_path)

router = APIRouter()


class ResponseTypeEnum(str, Enum):
    code = "code"
    token = "token"


class LoginFlowQuery:
    def __init__(
        self,
        redirect_uri: Annotated[
            HttpUrl,
            Query(),
            Doc(
                """
                Security scheme name.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ],
        state: Annotated[str, Query()] = None,
        response_type: Annotated[str | None, Query(enum=["code"])] = "code",
    ):
        self.response_type = response_type
        self.redirect_uri = redirect_uri
        self.state = state


@router.get("", response_class=HTMLResponse)
async def login(request: Request, login_flow_query: Annotated[LoginFlowQuery, Depends()]):
    return templates.TemplateResponse(
        request,
        "login.html",
        context={"request": request, "login_flow_query": login_flow_query},
    )


@auto_session
@transaction.atomic
@router.post("", response_class=RedirectResponse, status_code=302)
async def login_post(login_form: Annotated[LoginRequestForm, Form()]):
    user = await authenticate_user(
        username=str(login_form.email),
        password=str(login_form.password.get_secret_value()),
    )

    code_obj = await oauth_manager.generate_authorization_code(redirect_uri=str(login_form.redirect_uri), user=user)
    query_params = {"code": code_obj.code}

    if login_form.state:
        query_params["state"] = login_form.state

    query_str = urlencode(query_params)
    redirect_url = f"{login_form.redirect_uri}?{query_str}"

    return redirect_url
