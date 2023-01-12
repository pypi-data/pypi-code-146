from typing import List, Optional, Literal

from pydantic import BaseModel, Field, constr

from dry_scraper.data_sources.nhl.pydantic_models.nhl_conferences_api_source import (
    ShortConference,
)

DivisionLink = constr(regex=r"^/api/v1/divisions/(\d+|null)$")


class ShortDivision(BaseModel):
    id: int
    name: str
    name_short: Optional[str] = Field(alias="nameShort")
    link: DivisionLink
    abbreviation: Optional[str]


class Division(BaseModel):
    id: int
    name: str
    name_short: Optional[str] = Field(alias="nameShort")
    link: DivisionLink
    abbreviation: Optional[str]
    conference: ShortConference
    active: bool


class NullDivision(BaseModel):
    link: Literal["/api/v1/divisions/null"]

    class Config:
        extra = "forbid"


class Divisions(BaseModel):
    divisions: List[NullDivision | Division]
