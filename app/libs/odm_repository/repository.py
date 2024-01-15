from typing import Type, Union, Mapping, Any, TYPE_CHECKING
from beanie import Document
from beanie.exceptions import DocumentNotFound

if TYPE_CHECKING:
    from beanie.odm.documents import DocType


class BaseRepository:

    __model__: Type[Document] = None

    def get_document(self) -> Type[Document]:
        return self.__model__

    @classmethod
    def bind_to_cls(cls, document_cls: Type[Document]) -> None:
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

    async def get_or_create(
        self, *args: Union[Mapping[str, Any], bool], defaults: dict = None
    ) -> "DocType":
        defaults = defaults or {}

        obj = await self.get_document().find_one(*args)
        if obj:
            return obj

        return await self.create(**defaults)
