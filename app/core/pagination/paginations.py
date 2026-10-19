from typing import TypeVar

from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.customization import CustomizedPage, UseExcludedFields, UseFieldsAliases

T = TypeVar("T")

CustomCursorPage = CustomizedPage[
    CursorPage[T],
    UseFieldsAliases(
        items="data",
        current_page_backwards="reverse",
        current_page="current",
        previous_page="previous",
        next_page="next",
    ),
    UseExcludedFields("total"),
]
