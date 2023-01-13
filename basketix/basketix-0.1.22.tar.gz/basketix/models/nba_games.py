"""NBA game model"""

from typing import List, TypedDict

from .nba_game_status import NbaGameStatus
from .nba_game_extended_status import NbaGameExtendedStatus
from .nba_game_location import NbaGameLocation


class TeamInfo(TypedDict):
    teamId: str
    triCode: str
    teamTriCode: str
    teamName: str
    teamCity: str
    teamFullName: str
    location: NbaGameLocation
    score: int
    linescore: List[int]
    winner: bool

class NbaGameModel(TypedDict):
    """DynamoDB model for NBA game"""
    gameId: str
    gameDate: str
    weekId: str
    season: str
    gameStatus: NbaGameStatus
    extendedGameStatus: NbaGameExtendedStatus
    startTimeUTC: str
    teamIds: List[str]
    teams: List[TeamInfo]
    attendance: int
    gameDuration: int
    nPeriod: int
    hasOverTime: bool
