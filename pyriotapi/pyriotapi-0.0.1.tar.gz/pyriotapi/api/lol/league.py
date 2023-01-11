from typing import ClassVar

from .models import League, LeagueEnrty, Ranked, MiniSeries
from ..enums import Region, Tier, Division, Queue
from ..core import BaseLoLEndpoint


class LeagueEndpoint(BaseLoLEndpoint):
    BASE: ClassVar[str] = '/lol/league/v4/'

    def _create_league(self, data) -> League:
        return League(
            id = data['leagueId'],
            tier = Tier[data['tier']],
            queue = Queue(data['queue']),
            name = data['name'],
            entries = [
                LeagueEnrty(
                    summoner_id = item['summonerId'],
                    summoner_name = item['summonerName'],
                    lp = item['leaguePoints'],
                    division = Division[item['rank']],
                    wins = item['wins'],
                    losses = item['losses'],
                    veteran = item['veteran'],
                    inactive = item['inactive'],
                    fresh_blood = item['freshBlood'],
                    hot_streak = item['hotStreak'],
                    mini_series = MiniSeries(
                        target = item['miniSeries']['target'],
                        wins = item['miniSeries']['wins'],
                        losses = item['miniSeries']['losses'],
                        progress = item['miniSeries']['progress']
                    ) if 'miniSeries' in item else None
                ) for item in data['entries']
            ]
        )

    def _create_ranked(self, data) -> Ranked:
        return Ranked(
            id = data['leagueId'],
            queue = Queue(data['queueType']),
            tier = Tier[data['tier']],
            division = Division[data['rank']],
            summoner_id = data['summonerId'],
            summoner_name = data['summonerName'],
            lp = data['leaguePoints'],
            wins = data['wins'],
            losses = data['losses'],
            veteran = data['veteran'],
            inactive = data['inactive'],
            fresh_blood = data['freshBlood'],
            hot_streak = data['hotStreak'],
            mini_series = MiniSeries(
                target = data['miniSeries']['target'],
                wins = data['miniSeries']['wins'],
                losses = data['miniSeries']['losses'],
                progress = data['miniSeries']['progress']
            ) if 'miniSeries' in data else None
        )

    async def by_summoner(self, region: Region, _id: str) -> list[Ranked]:
        path = self.BASE + f'entries/by-summoner/{_id}'
        data = await self.fetch(region, path)
        return [self._create_ranked(item) for item in data]

    async def by_league_id(self, region: Region, _id: str) -> League:
        path = self.BASE + f'leagues/{_id}'
        data = await self.fetch(region, path)
        return self._create_league(data)

    async def get(
        self,
        region: Region,
        queue: Queue,
        tier: Tier,
        division: Division,
        *,
        page = 1
    ) -> list[Ranked]:
        path = f'/lol/league-exp/v4/entries/{queue.value}/{tier.name}/{division.name}'
        data = await self.fetch(region, path, page = page)
        return [self._create_ranked(item) for item in data]

    async def get_challenger(self, region: Region, queue: Queue) -> League:
        path = f'challengerleagues/by-queue/{queue.value}'
        data = await self.fetch(region, path)
        return self._create_league(data)

    async def get_grandmaster(self, region: Region, queue: Queue) -> League:
        path = f'grandmasterleagues/by-queue/{queue.value}'
        data = await self.fetch(region, path)
        return self._create_league(data)

    async def get_master(self, region: Region, queue: Queue) -> League:
        path = f'masterleagues/by-queue/{queue.value}'
        data = await self.fetch(region, path)
        return self._create_league(data)