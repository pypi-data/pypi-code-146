"""NBA player performance model"""

from typing import TypedDict

from .nba_game_status import NbaGameStatus

class NbaPlayerPerformanceModel(TypedDict):
    """DynamoDB model for NBA player performance"""
    gameId: str
    weekId: str
    season: str
    gameDate: str
    gameStatus: NbaGameStatus
    playerId: str
    firstName: str
    lastName: str
    fullName: str
    teamId: str
    teamTriCode: str
    teamName: str
    teamCity: str
    teamFullName: str
    points: int
    sec: int
    fgm: int
    fga: int
    fgpct: float
    ftm: int
    fta: int
    ftpct: float
    tpm: int
    tpa: int
    tppct: float
    offReb: int
    defReb: int
    totReb: int
    assists: int
    pFouls: int
    steals: int
    turnovers: int
    blocks: int
    plusMinus: int
    evaluation: int
