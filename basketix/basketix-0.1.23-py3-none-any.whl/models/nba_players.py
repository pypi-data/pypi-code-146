"""NBA player model"""

from typing import TypedDict, List

from typing_extensions import NotRequired

from .attributes.positions import Position
from .attributes.rotoworld_id import RotoworldId

class NbaPlayerTeamInfo(TypedDict):
    """Sub model for team info for NBA player model"""
    teamId: str
    tricode: str
    city: str
    nickname: str
    fullName: str

NbaPlayerInjuryInfo = TypedDict('NbaPlayerInjuryInfo', {
    'return': str,
    'type': str,
    'date': str,
})

class NbaPlayerEvaluationInfo(TypedDict):
    """Sub model for stat info for NBA player model"""
    gameDate: str
    gameId: str
    weekId: str
    evaluation: int

class NbaPlayerStatInfo(TypedDict):
    """Sub model for stat info for NBA player model"""
    computationDate: int
    n: int
    nPlayed: int
    pctPlayed: int
    evaluationSum: int
    evaluationMean: float
    evaluationStd: int
    evaluationMin: int
    evaluationMax: int
    lastEvaluations: List[NbaPlayerEvaluationInfo]

class NbaPlayerModel(TypedDict):
    """DynamoDB model for NBA player"""
    playerId: str
    fullName: str
    firstName: str
    lastName: str
    teamId: NotRequired[str]
    team: NotRequired[NbaPlayerTeamInfo]
    teamDate: NotRequired[str]
    positions: NotRequired[List[Position]]
    stats: NotRequired[NbaPlayerStatInfo]
    cost: NotRequired[int]
    costComputationDate: NotRequired[str]
    injury: NotRequired[NbaPlayerInjuryInfo]
    rotoworldId: NotRequired[RotoworldId]



