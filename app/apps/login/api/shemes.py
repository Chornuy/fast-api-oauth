from typing import Annotated

from fastapi import Query
from pydantic import HttpUrl
from typing_extensions import Doc


class CompleteFlowQuery:
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
        code: Annotated[str, Query()],
        state: Annotated[str, Query()] = None,
    ):
        self.redirect_uri = redirect_uri
        self.state = state
        self.code = code
