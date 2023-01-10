from typing import Dict, List, Optional, Sequence, Union

from pydantic import Field

from aiosox.utils import BaseModel

from .bindings import ChannelBindings
from .operation import ApiOperation
from .parameter import ApiParameter, ApiParameterName
from .reference import Reference
from .security import ApiSecurityRequirement


class ApiChannel(BaseModel):
    """represents a single topic/channel/namespace(socketio)"""

    ref: Optional[str] = Field(alias="$ref")
    description: Optional[str] = None
    servers: Optional[List[str]] = None

    subscribe: Optional[ApiOperation] = None
    publish: Optional[ApiOperation] = None
    parameters: Optional[Dict[ApiParameterName, Union[ApiParameter, Reference]]] = None

    bindings: Optional[Union[ChannelBindings, Reference]] = None
