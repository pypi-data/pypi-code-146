from typing import Dict, List, TypedDict
from typing_extensions import NotRequired

from .attributes.basketix_team_id import BasketixTeamId
from .attributes.game_id import GameId
from .attributes.nba_team_id import NbaTeamId
from .attributes.player_id import PlayerId
from .attributes.positions import Position
from .attributes.season_id import SeasonId
from .attributes.week_id import WeekId

class PlayerBonus(TypedDict):
    playerId: NotRequired[PlayerId]
    points: int

class BestUniqueEvaluation(PlayerBonus, total=False):
    totalEvaluation: int

class BestTotalEvaluation(PlayerBonus, total=False):
    evaluation: int
    gameId: GameId

class Evaluation(TypedDict):
    playerId: PlayerId
    gameId: GameId
    teamId: NbaTeamId
    gameDate: str
    evaluation: int

class Players(TypedDict):
    playerId: PlayerId
    evaluation: int
    evaluations: List[Evaluation]
    positions: List[Position]

class Bonus(TypedDict):
    bestUniqueEvaluation: BestUniqueEvaluation
    bestTotalEvaluation: BestTotalEvaluation
    points: int

class Points(TypedDict):
    bonus: Bonus
    rank: int
    total: int

class Ranks(TypedDict):
    evaluation: int
    final: int

class BasketixTeamsModel(TypedDict):
    '''Model of the basketix teams table'''
    weekId: WeekId
    teamId: BasketixTeamId
    basketixId: BasketixTeamId
    seasonId: SeasonId
    isValidate: bool
    validateAt: str
    isEditable: bool
    points: Points
    ranks: Ranks
    evaluation: int
    players: Dict[PlayerId, Players]
    starters: List[PlayerId]
    initialStarters: List[PlayerId]
    substitutes: List[PlayerId]
    initialSubstitutes: List[PlayerId]
