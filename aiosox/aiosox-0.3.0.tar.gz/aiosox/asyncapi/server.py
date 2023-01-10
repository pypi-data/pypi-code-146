from typing import Dict, List, Optional

from aiosox.utils import BaseModel

from .enums import ApiServerProtocol
from .security import ApiSecurityRequirement

ApiServerName = str


class ApiServer(BaseModel):
    """model defining a server"""

    url: str
    protocol: ApiServerProtocol
    description: Optional[str] = None
    security: Optional[List[Dict[str, ApiSecurityRequirement]]] = None
