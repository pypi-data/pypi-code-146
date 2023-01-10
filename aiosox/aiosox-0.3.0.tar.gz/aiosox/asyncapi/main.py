from typing import Dict, List, Mapping, Optional, Type

import orjson
from fastapi.encoders import jsonable_encoder
from pydantic import AnyUrl, Extra, Field, schema_json_of, schema_of
 
from aiosox.utils import BaseModel

from .channel import ApiChannel, ApiOperation
from .components import ApiComponents
from .message import ApiMessage
from .reference import Reference
from .schema import ApiSchema
from .server import ApiServer, ApiServerName
from .tag import ApiTag

 
ChannelName = str


class License(BaseModel):
    """
    License information for the exposed API.
    """

    name: str
    url: Optional[AnyUrl] = None

    class Config:
        extra = Extra.forbid


class Contact(BaseModel):
    """
    Contact information for the exposed API.
    """

    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[str] = None

    class Config:
        extra = Extra.forbid


class ApiInfo(BaseModel):
    """base data for app api"""

    title: str = Field(..., description="app api title")
    version: str = Field(..., description="app api version")
    description: Optional[str] = Field(None, description="description of app api")
    terms_of_service: Optional[AnyUrl] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None


class AsyncAPI(BaseModel):
    """combines all the parts of the asyncapi schema"""

    """base data for asyncapi spec"""
    id: str | None = None
    info: ApiInfo = Field(description="api base data")
    asyncapi: str = Field(default="2.5.0", description="version of the asyncapi spec")
    servers: Mapping[ApiServerName, ApiServer]
    channels: Mapping[ChannelName, ApiChannel] = {}
    components: ApiComponents
    tags: List[ApiTag]

 
   

 