from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from fastapi_pagination.ext.beanie import apaginate
from pydantic import Field

from app.apps.oauth.api.shemes import UserResponseScheme
from app.apps.user.models import User
from app.core.pagination.paginations import CustomCursorPage
from app.libs.beanie_filters import Filter

router = APIRouter()


class UserFilter(Filter):
    name: str | None = None
    age__lt: int | None = None
    age__gte: int | None = Field(Query(description="this is a nice description", default=None))
    """Required field with a custom description.

    See: https://github.com/tiangolo/fastapi/issues/4700 for why we need to wrap `Query` in `Field`.
    """
    order_by: list[str] = ["age"]
    search: str | None = None

    class Constants(Filter.Constants):
        model = User
        search_model_fields = ["name"]


@router.get("/", tags=["user-list"], response_model=CustomCursorPage[UserResponseScheme])
async def get_list_users(user_filter: Annotated[UserFilter, FilterDepends(UserFilter)]):
    """

    :param user_filter:
    :return:
    """
    query = user_filter.filter(User.find({}))

    return await apaginate(query.project(UserResponseScheme))
