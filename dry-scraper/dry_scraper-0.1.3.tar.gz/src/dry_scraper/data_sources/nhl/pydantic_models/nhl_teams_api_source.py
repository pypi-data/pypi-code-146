from typing import Optional, List

from pydantic import BaseModel, constr, Field, HttpUrl

from dry_scraper.data_sources.nhl.pydantic_models.nhl_conferences_api_source import (
    ShortConference,
)
from dry_scraper.data_sources.nhl.pydantic_models.nhl_divisions_api_source import (
    NullDivision,
    ShortDivision,
)

VenueLink = constr(regex=r"^/api/v1/venues/(\d+|null)$")

FranchiseLink = constr(regex=r"^/api/v1/franchises/(\d+|null)$")
TeamLink = constr(regex=r"^/api/v1/teams/(\d+|null)$")


class ShortTeam(BaseModel):
    id: int
    name: str
    link: TeamLink
    abbreviation: Optional[str]
    tricode: Optional[str] = Field(alias="triCode")


class TimeZone(BaseModel):
    id: str
    offset: int
    tz: str


class Venue(BaseModel):
    id: Optional[int]
    name: Optional[str]
    link: VenueLink
    city: Optional[str]
    time_zone: TimeZone = Field(alias="timeZone")


class ShortVenue(BaseModel):
    id: Optional[int]
    name: str
    link: VenueLink


class Franchise(BaseModel):
    franchise_id: int = Field(alias="franchiseId")
    team_name: str = Field(alias="teamName")
    link: FranchiseLink


class Team(BaseModel):
    id: int
    name: str
    link: Optional[TeamLink]
    venue: Optional[Venue]
    abbreviation: Optional[str]
    tricode: Optional[str] = Field(alias="triCode")
    team_name: str = Field(alias="teamName")
    location_name: str = Field(alias="locationName")
    first_year_of_play: Optional[str] = Field(alias="firstYearOfPlay")
    division: ShortDivision | NullDivision
    conference: ShortConference
    franchise: Franchise
    short_name: str = Field(alias="shortName")
    official_site_url: Optional[HttpUrl] = Field(alias="officialSiteUrl")
    franchise_id: int = Field(alias="franchiseId")
    active: bool


class Teams(BaseModel):
    teams: List[Team]
