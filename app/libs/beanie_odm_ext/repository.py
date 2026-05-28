from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Optional

from beanie import Document
from beanie.exceptions import DocumentNotFound

if TYPE_CHECKING:
    from beanie.odm.documents import DocType


class BaseRepository:
    __model__: type[Document] = None

    def get_document(self) -> type[Document]:
        return self.__model__

    @classmethod
    def bind_to_cls(cls, document_cls: type[Document]) -> None:
        cls.__model__ = document_cls

    async def create(self, **kwargs) -> Document:
        obj = self.get_document()(**kwargs)
        await obj.save()
        return obj

    async def find_one_or_error(self, *args, **kwargs) -> Document:
        obj = await self.get_document().find_one(*args, **kwargs)
        if not obj:
            raise DocumentNotFound()

        return obj

    async def get(self, *args, **kwargs) -> Optional["DocType"]:
        return await self.get_document().get(*args, **kwargs)

    async def get_or_create(self, *args: Mapping[str, Any] | bool, defaults: dict = None, **kwargs: Any) -> "DocType":
        defaults = defaults or {}

        obj = await self.get_document().find_one(*args, **kwargs).project()
        if obj:
            return obj

        return await self.create(**defaults)
