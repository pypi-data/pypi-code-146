import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from dry_scraper.data_sources.nhl.pydantic_models.nhl_game_live_feed_api_source import (
    LiveFeedLink,
    Status,
)
from dry_scraper.data_sources.nhl.pydantic_models.nhl_teams_api_source import ShortTeam


class LeagueRecord(BaseModel):
    wins: int
    losses: int
    ot: Optional[int]
    type: str


class Team(BaseModel):
    league_record: LeagueRecord = Field(alias="leagueRecord")
    score: int
    team: ShortTeam


class Teams(BaseModel):
    away: Team
    home: Team


class Game(BaseModel):
    gamePk: int
    link: LiveFeedLink
    game_type: str = Field(alias="gameType")
    season: str = Field(alias="gameType")
    game_date: datetime.datetime = Field(alias="gameDate")
    status: Status
    teams: Teams


class Date(BaseModel):
    date: datetime.date
    total_items: int = Field(alias="totalItems")
    total_games: int = Field(alias="totalGames")
    games: List[Game]


class Schedule(BaseModel):
    total_items: int = Field(alias="totalItems")
    total_games: int = Field(alias="totalGames")
    dates: List[Date]
