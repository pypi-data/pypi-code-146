from typing import Any, ClassVar, Mapping

from .models import Summoner
from ..core import BaseLoLEndpoint
from ..enums import Region


class SummonerEndpoint(BaseLoLEndpoint):
    BASE: ClassVar[str] = '/lol/summoner/v4/summoners/'

    async def fetch(self, region: Region, path: str, **params: Any) -> Summoner:
        data = await super().fetch(region, path, **params)
        return self._create_summoner(data)

    def _create_summoner(self, data: Mapping[str, Any]) -> Summoner:
        return Summoner(
            id = data['id'],
            account_id = data['accountId'],
            puuid = data['puuid'],
            name = data['name'],
            icon = data['profileIconId'],
            lvl = data['summonerLevel']
        )

    async def by_id(self, region: Region, _id: str) -> Summoner:
        path = self.BASE + _id
        return await self.fetch(region, path)
    
    async def by_account_id(self, region: Region, account_id: str) -> Summoner:
        path = self.BASE + f'by-account/{account_id}'
        return await self.fetch(region, path)
    
    async def by_puuid(self, region: Region, puuid: str) -> Summoner:
        path = self.BASE + f'by-puuid/{puuid}'
        return await self.fetch(region, path)
    
    async def by_name(self, region: Region, name: str) -> Summoner:
        path = self.BASE + f'by-name/{name}'
        return await self.fetch(region, path)