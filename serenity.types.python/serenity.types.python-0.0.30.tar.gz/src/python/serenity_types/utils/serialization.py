from pydantic import BaseModel
from humps.camel import case
from enum import Enum
from typing import (AbstractSet,
                    Mapping,
                    Any,
                    Callable,
                    Optional,
                    Union,
                    cast)


IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


def serenity_json_format(data):
    for k, v in data.items():
        if isinstance(v, dict):
            data[k] = serenity_json_format(v)
        # Can add further JSON formatting needs here in future
        if issubclass(type(v), Enum):
            data[k] = v.name
    return data


def serenity_json(
    self,
    *,
    include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
    exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    encoder: Optional[Callable[[Any], Any]] = None,
    models_as_dict: bool = True,
    **dumps_kwargs: Any,
) -> str:
    encoder = cast(Callable[[Any], Any], encoder or self.__json_encoder__)
    data = dict(
        self._iter(
            to_dict=models_as_dict,
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
    )
    if self.__custom_root_type__:
        data = data["__root__"]
    data = serenity_json_format(data)
    return self.__config__.json_dumps(data, default=encoder, **dumps_kwargs)


class CamelModel(BaseModel):
    """
    Helper base class that ensures JSON is encoded camel-case and enums are properly encoded.
    """

    class Config:
        alias_generator = case
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    json = serenity_json
