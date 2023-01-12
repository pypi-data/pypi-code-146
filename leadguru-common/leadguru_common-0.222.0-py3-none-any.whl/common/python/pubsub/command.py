import enum
from typing import Optional
from pydantic import BaseModel, Extra


class TelegramCommandType(enum.Enum):
    AUTH_VERIFICATION_CODE = 1
    HARD_RESET = 1


class TelegramCommand(BaseModel, extra=Extra.ignore):
    bot_id: str
    type: int
    data: Optional[str]
