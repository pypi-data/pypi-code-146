from __future__ import annotations

from typing import Any, Generic, TypeVar, get_args

from pydantic import ValidationError
from pydantic.generics import GenericModel
from pydantic.typing import get_origin, is_union

from .. import container
from ..pagination import Pagination
from .extra import schema_by_field_name

ListItem = TypeVar("ListItem")


class Schema(container.BaseModel):
    class Config:
        schema_extra = schema_by_field_name()


class TimeStampedSchema(container.TimeStampedModel, Schema):
    ...


class ListSchema(Schema, GenericModel, Generic[ListItem]):
    total: int
    items: list[ListItem]

    @classmethod
    def from_pagination(
        cls,
        pagination: Pagination,
        parser_name: str = "parse_obj",
        **parser_kwargs: Any,
    ) -> ListSchema:
        if not pagination.items:
            return cls(**pagination.dict())

        item_type = cls.__fields__["items"].type_
        item_origin = get_origin(item_type)
        if is_union(item_origin):
            for arg in get_args(item_type):
                try:
                    arg.parse_obj(pagination.items[0])
                    item_type = arg
                except ValidationError:
                    continue

        item_parsable = issubclass(item_type, container.BaseModel)
        if not item_parsable:
            data = pagination.dict(exclude={"extra"}) | pagination.extra
            return cls(**data)

        if (parser := getattr(item_type, parser_name, None)) is None:
            raise AttributeError(f"{item_type.__name__} has no attribute: {parser_name}")

        return cls(
            **pagination.dict(exclude={"items", "extra"}),
            **pagination.extra,
            items=[parser(item, **parser_kwargs) for item in pagination.items],
        )
