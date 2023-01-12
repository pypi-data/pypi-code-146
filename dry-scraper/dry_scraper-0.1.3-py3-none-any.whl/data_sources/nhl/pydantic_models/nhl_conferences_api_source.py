from typing import List, Optional

from pydantic import BaseModel, constr, Field

ConferenceLink = constr(regex=r"^/api/v1/conferences/(\d+|null)$")


class Conference(BaseModel):
    id: int
    name: str
    link: ConferenceLink
    abbreviation: str
    short_name: str = Field(alias="shortName")
    active: bool


class ShortConference(BaseModel):
    id: Optional[int]
    name: Optional[str]
    link: ConferenceLink


class Conferences(BaseModel):
    conferences: List[Conference]
