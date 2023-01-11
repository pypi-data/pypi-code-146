from .http import HTTPClient
from .api.lol import (
    SummonerEndpoint,
    LeagueEndpoint,
    ChampionMasteryEndpoint,
    RotationEndpoint,
    StatusEndpoint
)


class LoLApi:
    def __init__(self, token: str) -> None:
        self._http = HTTPClient(token)

    @property
    def summoner(self) -> SummonerEndpoint:
        return SummonerEndpoint(self._http)

    @property
    def ranked(self) -> LeagueEndpoint:
        return LeagueEndpoint(self._http)

    @property
    def mastery(self) -> ChampionMasteryEndpoint:
        return ChampionMasteryEndpoint(self._http)

    @property
    def rotation(self) -> RotationEndpoint:
        return RotationEndpoint(self._http)

    @property
    def status(self) -> StatusEndpoint:
        return StatusEndpoint(self._http)