from typing import Any, ClassVar

from beanie import Document
from pydantic._internal._generics import PydanticGenericMetadata
from pydantic._internal._model_construction import ModelMetaclass

from app.libs.beanie_odm_ext.repository import BaseRepository


class DocumentRepositoryMeta(ModelMetaclass):
    def __new__(
        cls,
        cls_name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
        __pydantic_reset_parent_namespace__: bool = True,
        _create_model_module: str | None = None,
        **kwargs: Any,
    ) -> type:
        new_super = super().__new__

        parents = [b for b in bases if isinstance(b, DocumentRepositoryMeta)]

        if not parents:
            return new_super(
                cls,
                cls_name,
                bases,
                namespace,
                __pydantic_generic_metadata__,
                __pydantic_reset_parent_namespace__,
                _create_model_module,
                **kwargs,
            )

        new_cls = new_super(
            cls,
            cls_name,
            bases,
            namespace,
            __pydantic_generic_metadata__,
            __pydantic_reset_parent_namespace__,
            _create_model_module,
            **kwargs,
        )

        if "repository" in namespace.keys():
            repository = namespace["repository"]
            repository.bind_to_cls(new_cls)

        return new_cls


class DocumentRepository(Document, metaclass=DocumentRepositoryMeta):
    repository: ClassVar[BaseRepository] = BaseRepository()
