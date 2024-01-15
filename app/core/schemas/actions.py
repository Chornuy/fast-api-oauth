from typing import Optional

from pydantic import BaseModel

from app.core.schemas.constants import ActionStatusCode


class ResourceActionResponse(BaseModel):
    resource_id: str | int
    status_code: ActionStatusCode
    message: Optional[str] = None


class SuccessAction(ResourceActionResponse):
    status_code: ActionStatusCode = ActionStatusCode.success.value
