from enum import Enum
from typing import Union
from urllib.parse import urlencode

from fastapi import APIRouter, Query, Depends, Form
from fastapi.exceptions import ValidationException
from pydantic import HttpUrl
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from typing_extensions import Annotated, Doc  # type: ignore [attr-defined]
from fastapi.responses import RedirectResponse

from app.apps.oauth.app import templates_path
from app.apps.oauth.models import OAuthCode
from app.apps.oauth.services.authentication import authenticate_user
from app.apps.oauth.view.schemes import LoginRequestForm

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
            )
        ],
        state: Annotated[
            str,
            Query()
        ] = None,
        response_type: Annotated[
            Union[str, None],
            Query(enum=["code"])
        ] = "code",
    ):
        self.response_type = response_type
        self.redirect_uri = redirect_uri
        self.state = state


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, login_flow_query: Annotated[LoginFlowQuery, Depends()]):
    return templates.TemplateResponse("login.html", context={"request": request, "login_flow_query": login_flow_query})


class LoginFormRequest:

    def __init__(self, login: Annotated[str, Form()]):
        pass


