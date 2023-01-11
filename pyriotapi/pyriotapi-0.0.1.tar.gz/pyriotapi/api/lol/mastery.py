from typing import ClassVar

from .models import ChampionMastery
from ..core import BaseLoLEndpoint
from ..enums import Region


class ChampionMasteryEndpoint(BaseLoLEndpoint):
    BASE: ClassVar[str] = '/lol/champion-mastery/v4/champion-masteries/by-summoner/'
    SCORES: ClassVar[str] = '/lol/champion-mastery/v4/scores/by-summoner/'

    def _create_champion_mastery(self, data) -> ChampionMastery:
        return ChampionMastery(
            id = data['championId'],
            lvl = data['championLevel'],
            points = data['championPoints'],
            last_play = data['lastPlayTime'],
            points_since_last_level = data['championPointsSinceLastLevel'],
            points_until_next_level = data['championPointsUntilNextLevel'],
            chest = data['chestGranted'],
            tokens = data['tokensEarned']
        )

    async def get(self, region: Region, _id: str, *, champion: int = None, page: int = None) -> ChampionMastery:
        path = self.BASE + _id
        if champion is not None:
            path += f'/by-champion/{champion}'
        elif page is not None:
            path += '/top'
        
        data = await self.fetch(region, path, page = page if champion is None else None)
        if isinstance(data, list):
            return [self._create_champion_mastery(item) for item in data]
        return self._create_champion_mastery(data)

    async def get_scores(self, region: Region, _id: str) -> int:
        path = self.SCORES + _id
        return await self.fetch(region, path)