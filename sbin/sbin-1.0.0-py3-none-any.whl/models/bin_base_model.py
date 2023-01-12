from typing import Any, Optional, Type

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, validator


class BinBaseModel(PydanticBaseModel):
    bin_class: Optional[Type[Any]]

    @validator("bin_class", always=True, pre=True)
    def for_equality_purposes(cls, _: Optional[Type[Any]]) -> Optional[Type[Any]]:
        return cls

    class Config:
        allow_mutation = False
        extra = Extra.forbid
        min_anystr_length = 1
        arbitrary_types_allowed = True
