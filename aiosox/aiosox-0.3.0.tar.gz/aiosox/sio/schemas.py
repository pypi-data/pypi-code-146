from typing import Any, Optional

from ..utils import BaseModel


class SioError(BaseModel):
    code: int
    msg: str
    loc: Optional[Any] = None
    type: Optional[str] = None
