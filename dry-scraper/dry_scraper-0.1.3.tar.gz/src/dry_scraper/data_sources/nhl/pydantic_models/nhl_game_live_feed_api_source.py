from datetime import datetime
from pydantic import BaseModel, Field, constr
from typing import List, Dict, Optional, Union

from dry_scraper.data_sources.nhl.pydantic_models.nhl_people_api_source import (
    PersonIdString,
    PersonLink,
    Position,
    Player,
    Person,
)
from dry_scraper.data_sources.nhl.pydantic_models.nhl_teams_api_source import (
    Team,
    ShortTeam,
    ShortVenue,
)

LiveFeedLink = constr(regex=r"^/api/v1/game/\d{10}/feed/live$")


class Metadata(BaseModel):
    wait: int
    timestamp: str = Field(alias="timeStamp")


class Game(BaseModel):
    pk: int
    season: str
    type: str


class GameDateTime(BaseModel):
    date_time: datetime = Field(alias="dateTime")
    end_date_time: Optional[datetime] = Field(alias="endDateTime")


class Status(BaseModel):
    abstract_game_state: str = Field(alias="abstractGameState")
    coded_game_state: str = Field(alias="codedGameState")
    detailed_state: str = Field(alias="detailedState")
    status_code: str = Field(alias="statusCode")
    start_time_tbd: bool = Field(alias="startTimeTBD")


class Teams(BaseModel):
    away: Team
    home: Team


class GameData(BaseModel):
    game: Game
    date_time: GameDateTime = Field(alias="datetime")
    status: Status
    teams: Teams
    players: Dict[PersonIdString, Player]
    venue: ShortVenue


class PlaysByPeriod(BaseModel):
    start_index: int = Field(alias="startIndex")
    plays: List[int]
    end_index: int = Field(alias="endIndex")


class Strength(BaseModel):
    code: str
    name: str


class Result(BaseModel):
    event: str
    event_code: str = Field(alias="eventCode")
    event_type_id: str = Field(alias="eventTypeId")
    description: str
    secondary_type: Optional[str] = Field(alias="secondaryType")
    strength: Optional[Strength]
    game_winning_goal: Optional[bool] = Field(alias="gameWinningGoal")
    empty_net: Optional[bool] = Field(alias="emptyNet")


class Goals(BaseModel):
    away: int
    home: int


class About(BaseModel):
    event_idx: int = Field(alias="eventIdx")
    event_id: int = Field(alias="eventId")
    period: int
    period_type: str = Field(alias="periodType")
    ordinal_num: str = Field(alias="ordinalNum")
    period_time: str = Field(alias="periodTime")
    period_time_remaining: str = Field(alias="periodTimeRemaining")
    date_time: datetime = Field(alias="dateTime")
    goals: Goals


class Coordinates(BaseModel):
    x: Optional[int]
    y: Optional[int]


class PlayPlayer(BaseModel):
    player: Person
    player_type: str = Field(alias="playerType")
    season_total: Optional[str] = Field(alias="seasonTotal")


class Play(BaseModel):
    result: Result
    about: About
    coordinates: Coordinates
    players: Optional[List[PlayPlayer]]
    team: Optional[ShortTeam]


class Plays(BaseModel):
    all_plays: List[Play] = Field(alias="allPlays")
    scoring_plays: List[int] = Field(alias="scoringPlays")
    penalty_plays: List[int] = Field(alias="penaltyPlays")
    plays_by_period: List[PlaysByPeriod] = Field(alias="playsByPeriod")
    current_play: Play = Field(alias="currentPlay")


class TeamPeriodLineScore(BaseModel):
    goals: int
    shots_on_goal: int = Field(alias="shotsOnGoal")
    rink_side: Optional[str] = Field(alias="rinkSide")


class Period(BaseModel):
    period_type: str = Field(alias="periodType")
    start_time: datetime = Field(alias="startTime")
    end_time: Optional[datetime] = Field(alias="endTime")
    num: int
    ordinal_num: str = Field(alias="ordinalNum")
    home: TeamPeriodLineScore
    away: TeamPeriodLineScore


class TeamShootoutInfo(BaseModel):
    scores: int
    attempts: int


class ShootoutInfo(BaseModel):
    away: TeamShootoutInfo
    home: TeamShootoutInfo
    start_time: Optional[datetime] = Field(alias="startTime")


class TeamLineScore(BaseModel):
    team: ShortTeam
    goals: int
    shots_on_goal: int = Field(alias="shotsOnGoal")
    goalie_pulled: bool = Field(alias="goaliePulled")
    num_skaters: int = Field(alias="numSkaters")
    power_play: bool = Field(alias="powerPlay")


class TeamsLineScore(BaseModel):
    away: TeamLineScore
    home: TeamLineScore


class IntermissionInfo(BaseModel):
    intermission_time_remaining: int = Field(alias="intermissionTimeRemaining")
    intermission_time_elapsed: int = Field(alias="intermissionTimeElapsed")
    in_intermission: bool = Field(alias="inIntermission")


class PowerPlayInfo(BaseModel):
    situation_time_remaining: int = Field(alias="situationTimeRemaining")
    situation_time_elapsed: int = Field(alias="situationTimeElapsed")
    in_situation: bool = Field(alias="inSituation")


class LineScore(BaseModel):
    current_period: str = Field(alias="currentPeriod")
    current_period_ordinal: str = Field(alias="currentPeriodOrdinal")
    current_period_time_remaining: str = Field(alias="currentPeriodTimeRemaining")
    periods: List[Period]
    shootout_info: ShootoutInfo = Field(alias="shootoutInfo")
    teams: TeamsLineScore
    power_play_strength: str = Field(alias="powerPlayStrength")
    has_shootout: bool = Field(alias="hasShootout")
    intermission_info: IntermissionInfo = Field(alias="intermissionInfo")
    power_play_info: PowerPlayInfo = Field(alias="powerPlayInfo")


class Official(BaseModel):
    official: Person
    official_type: str = Field(alias="officialType")


class TeamSkaterStats(BaseModel):
    goals: int
    pim: int
    shots: int
    power_play_percentage: float = Field(alias="powerPlayPercentage")
    power_play_goals: int = Field(alias="powerPlayGoals")
    power_play_opportunities: int = Field(alias="powerPlayOpportunities")
    face_off_win_percentage: float = Field(alias="faceOffWinPercentage")
    blocked: int
    takeaways: int
    giveaways: int
    hits: int


class TeamStats(BaseModel):
    team_skater_stats: TeamSkaterStats = Field(alias="teamSkaterStats")


class PlayerStatsPerson(BaseModel):
    id: PersonIdString
    full_name: str = Field(alias="fullName")
    link: constr(regex=r"^/api/v1/people/\d+$")
    shoots_catches: str = Field(alias="shootsCatches")
    roster_status: str = Field(alias="rosterStatus")


class GoalieStats(BaseModel):
    time_on_ice: str = Field(alias="timeOnIce")
    assists: int
    goals: int
    pim: int
    shots: int
    saves: int
    power_play_saves: int = Field(alias="powerPlaySaves")
    shorthanded_saves: int = Field(alias="shortHandedSaves")
    even_saves: int = Field(alias="evenSaves")
    shorthanded_shots_against: int = Field(alias="shortHandedShotsAgainst")
    even_shots_against: int = Field(alias="evenShotsAgainst")
    power_play_shots_against: int = Field(alias="powerPlayShotsAgainst")
    decision: str
    save_percentage: float = Field(alias="savePercentage")
    power_play_save_percentage: float = Field(alias="powerPlaySavePercentage")
    even_strength_save_percentage: float = Field(alias="evenStrengthSavePercentage")


class SkaterStats(BaseModel):
    time_on_ice: str = Field(alias="timeOnIce")
    assists: int
    goals: int
    shots: int
    hits: int
    power_play_goals: int = Field(alias="powerPlayGoals")
    power_play_assists: int = Field(alias="powerPlayAssists")
    penalty_minutes: int = Field(alias="penaltyMinutes")
    face_off_wins: int = Field(alias="faceOffWins")
    face_offs_taken: int = Field(alias="faceoffTaken")
    takeaways: int
    giveaways: int
    shorthanded_goals: int = Field(alias="shortHandedGoals")
    shorthanded_assists: int = Field(alias="shortHandedAssists")
    blocked_shots: int = Field(alias="blocked")
    plus_minus: int = Field(alias="plusMinus")
    even_time_on_ice: str = Field(alias="evenTimeOnIce")
    power_play_time_on_ice: str = Field(alias="powerPlayTimeOnIce")
    shorthanded_time_on_ice: str = Field(alias="shortHandedTimeOnIce")


class PlayerStats(BaseModel):
    skater_stats: Optional[SkaterStats] = Field(alias="skaterStats")
    goalie_stats: Optional[GoalieStats] = Field(alias="goalieStats")


class PlayerStatsEntry(BaseModel):
    person: PlayerStatsPerson
    jersey_number: Optional[int] = Field(alias="jerseyNumber")
    position: Position
    stats: Union[PlayerStats, None, Dict]


class ShortPerson(BaseModel):
    full_name: str = Field(alias="fullName")
    link: PersonLink


class Coach(BaseModel):
    person: Person
    position: Position


class OnIcePlusPlayer(BaseModel):
    player_id: PersonIdString = Field(alias="playerId")
    shift_duration: int = Field(alias="shiftDuration")
    stamina: int


class PenaltyBox(BaseModel):
    id: PersonIdString
    time_remaining: str = Field(alias="timeRemaining")
    active: bool


class TeamBoxScore(BaseModel):
    team: ShortTeam
    team_stats: TeamStats = Field(alias="teamStats")
    players: Dict[PersonIdString, PlayerStatsEntry]
    goalies: List[PersonIdString]
    skaters: List[PersonIdString]
    on_ice: List[PersonIdString] = Field(alias="onIce")
    on_ice_plus: List[OnIcePlusPlayer] = Field(alias="onIcePlus")
    scratches: List[PersonIdString]
    penalty_box: List[PenaltyBox] = Field(alias="penaltyBox")
    coaches: List[Coach]


class TeamsBoxScore(BaseModel):
    away: TeamBoxScore
    home: TeamBoxScore


class BoxScore(BaseModel):
    teams: TeamsBoxScore
    officials: List[Official]


class Decisions(BaseModel):
    winner: Optional[Person]
    loser: Optional[Person]
    first_star: Optional[Person] = Field(alias="firstStar")
    second_star: Optional[Person] = Field(alias="secondStar")
    third_star: Optional[Person] = Field(alias="thirdStar")


class LiveData(BaseModel):
    plays: Plays
    line_score: LineScore = Field(alias="linescore")
    box_score: BoxScore = Field(alias="boxscore")
    decisions: Decisions


class LiveFeed(BaseModel):
    game_pk: int = Field(alias="gamePk")
    link: LiveFeedLink
    metadata: Metadata = Field(alias="metaData")
    game_data: GameData = Field(alias="gameData")
    live_data: LiveData = Field(alias="liveData")
