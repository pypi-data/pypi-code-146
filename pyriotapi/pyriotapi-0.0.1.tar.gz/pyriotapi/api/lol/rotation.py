from typing import ClassVar

from .models import Rotation
from ..core import BaseLoLEndpoint
from ..enums import Region


class RotationEndpoint(BaseLoLEndpoint):
    BASE: ClassVar[str] = '/lol/platform/v3/champion-rotations'

    async def get(self, region: Region):
        data = await self.fetch(region, self.BASE)
        return Rotation(
            champions = data['freeChampionIds'],
            champions_for_new = data['freeChampionIdsForNewPlayers'],
            max_lvl_for_new = data['maxNewPlayerLevel']
        )