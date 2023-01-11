from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):

    msg: str = Field(...)
    type: Optional[str] = None
    loc: Optional[list] = None
    ctx: Optional[dict] = None
