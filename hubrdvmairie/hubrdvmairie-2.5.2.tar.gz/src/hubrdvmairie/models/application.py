from datetime import datetime

from pydantic import BaseModel


class Application(BaseModel):
    meeting_point: str
    datetime: datetime
    management_url: str
    cancel_url: str
