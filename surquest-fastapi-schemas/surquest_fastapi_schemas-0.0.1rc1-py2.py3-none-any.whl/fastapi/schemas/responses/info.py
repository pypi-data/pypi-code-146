from pydantic import BaseModel
from typing import List
from .status import Status
from .message import Message


class InfoSuccess(BaseModel):
    status: str = Status.success


class InfoWarning(BaseModel):
    status: str = Status.warning
    warnings: List[Message] = []


class InfoError(BaseModel):
    status: str = Status.error
    warnings: List[Message] = []
    errors: List[Message] = []
