from pydantic import BaseModel

from app.core.schemas.constants import ActionStatusCode


class ResourceActionResponse(BaseModel):
    resource_id: str | int
    status_code: ActionStatusCode
    message: str | None = None


class SuccessAction(ResourceActionResponse):
    status_code: ActionStatusCode = ActionStatusCode.success.value
