from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    description: str
    alert_level: str
