from datetime import datetime

from pydantic import BaseModel


class AvailableTimeSlot(BaseModel):
    datetime: datetime
    callback_url: str
