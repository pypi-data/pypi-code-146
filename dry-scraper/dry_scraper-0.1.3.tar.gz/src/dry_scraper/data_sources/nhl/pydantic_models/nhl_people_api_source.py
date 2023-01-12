from datetime import date
from typing import List, Optional

from pydantic import BaseModel, constr, Field

from dry_scraper.data_sources.nhl.pydantic_models.nhl_teams_api_source import ShortTeam

PersonIdString = constr(regex=r"^(ID)?\d{4,7}$")


PersonLink = constr(regex=r"^/api/v1/people/(\d+|null)$")


class Position(BaseModel):
    code: str
    name: str
    type: str
    abbreviation: str


class Player(BaseModel):
    id: int
    full_name: str = Field(alias="fullName")
    link: PersonLink
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    primary_number: Optional[int] = Field(alias="primaryNumber")
    birth_date: date = Field(alias="birthDate")
    current_age: Optional[int] = Field(alias="currentAge")
    birth_city: Optional[str] = Field(alias="birthCity")
    birth_state_province: Optional[str] = Field(alias="birthStateProvince")
    birth_country: str = Field(alias="birthCountry")
    nationality: str
    height: str
    weight: int
    active: bool
    alternate_captain: Optional[bool] = Field(alias="alternateCaptain")
    captain: Optional[bool]
    rookie: bool
    shoots_catches: str = Field(alias="shootsCatches")
    roster_status: str = Field(alias="rosterStatus")
    current_team: Optional[ShortTeam] = Field(alias="currentTeam")
    primary_position: Position = Field(alias="primaryPosition")


class Person(BaseModel):
    id: Optional[PersonIdString]
    full_name: str = Field(alias="fullName")
    link: PersonLink


class People(BaseModel):
    people: List[Player]
