from __future__ import annotations

from typing import Any, Optional, Union

import bson
from pydantic import BaseModel as PydanticBaseModel

from . import field, types


class BaseModel(PydanticBaseModel):
    def copy(
        self,
        *,
        include: Optional[Union[set[str], dict[str, Any]]] = None,
        exclude: Optional[Union[set[str], dict[str, Any]]] = None,
        update: Optional[dict[str, Any]] = None,
        deep: bool = False,
        strict: bool = True,
    ) -> BaseModel:
        if strict and (diff := set((update or {}).keys()) - self.__fields_set__):
            raise AttributeError(f"{self.__class__.__name__} has no attributes: {', '.join(diff)}")

        return super().copy(
            include=include,
            exclude=exclude,
            update=update,
            deep=deep,
        )

    class Config:
        json_encoders = {bson.ObjectId: str}
        allow_population_by_field_name = True
        validate_assignment = True


class TimeStampedModel(BaseModel):
    created_at: types.DateTime = field.DateTimeField()
    updated_at: types.DateTime = field.DateTimeField()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        created_at_field = cls.__fields__.pop("created_at")
        updated_at_field = cls.__fields__.pop("updated_at")
        cls.__fields__ |= dict(created_at=created_at_field, updated_at=updated_at_field)
