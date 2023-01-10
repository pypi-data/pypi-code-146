from typing import Mapping, Optional, Sequence

from pydantic import Extra, Field

from aiosox.utils import BaseModel

from .enums import ApiSecuritySchemeLocation, ApiSecuritySchemesType

ApiSecurityRequirement = Mapping[str, Sequence[str]]


class ApiSecurityScheme(BaseModel):
    """model defining a security protocol"""

    param_type: ApiSecuritySchemesType = Field(None, alias="type")
    description: Optional[str] = None
    name: Optional[str] = None
    param_in: Optional[ApiSecuritySchemeLocation] = Field(None, alias="in")
    scheme: Optional[str] = None
    bearerFormat: Optional[str] = None

    class Config:
        extra = Extra.forbid
