from dataclasses import dataclass
from typing import Optional

from ..enums import Queue, Division, Tier, Locale


@dataclass
class Summoner:
    id: str
    account_id: str
    puuid: str
    name: str
    icon: int
    lvl: int

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} {0.name}>'.format(self)


@dataclass
class MiniSeries:
    target: int
    wins: int
    losses: int
    progress: str

    def __str__(self) -> str:
        return self.progress

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} {0.progress}>'.format(self)


@dataclass
class LeagueEnrty:
    summoner_id: str
    summoner_name: str
    division: Division
    lp: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool
    mini_series: Optional[MiniSeries]

    def __str__(self) -> str:
        return '{0.summoner_name} {0.division.name} division'.format(self)

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} {0.summoner_name} {0.division.name} division>'.format(self)


@dataclass
class League:
    id: str
    tier: Tier
    queue: Queue
    name: str
    entries: list[LeagueEnrty]

    def __str__(self) -> str:
        return '{0.tier} league {0.name}'.format(self)

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} entries={1}>'.format(self, len(self.entries))


@dataclass
class Ranked(LeagueEnrty):
    id: str
    queue: Queue
    tier: Tier

    def __str__(self) -> str:
        return '{0.queue.name} {0.tier} {0.division.name}'.format(self)

    def __repr__(self) -> str:
        return '<{0.__class__.__name__} {0.tier} {0.division.name}>'.format(self)


@dataclass
class ChampionMastery:
    id: int
    lvl: int
    points: int
    last_play: int
    points_since_last_level: int
    points_until_next_level: int
    chest: bool
    tokens: int


@dataclass
class Rotation:
    champions: list[int]
    champions_for_new: list[int]
    max_lvl_for_new: int


@dataclass
class ContentDto:
    content: str
    locale: Locale


@dataclass
class UpdateDto:
    id: int
    created_at: str
    updated_at: str
    translations: list[ContentDto]


@dataclass
class StatusDto:
    id: int
    status: str
    severity: str
    created_at: str
    archive_at: str
    updated_at: str
    titles: list[ContentDto]
    updates: list[UpdateDto]
    platforms: list[str]


@dataclass
class Status:
    id: str
    name: str
    locales: list[Locale]
    maintenances: list[StatusDto]
    incidents: list[StatusDto]