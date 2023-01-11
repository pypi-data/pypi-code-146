import sys
from typing import Any, ClassVar, Mapping

import httpx

from . import __version__


class Route:
    RIOT: ClassVar[str] = 'https://{region}.api.riotgames.com'

    def __init__(self, url: str, **params: Any) -> None:
        self.url = url
        self.params = params

    @classmethod
    def riot(cls, region: str, path: str, **params: Any):
        path = cls.RIOT.format(region = region) + path
        return cls(path, **params)


class HTTPClient:
    def __init__(self, token: str) -> None:
        self.__token = token
        self._session = httpx.AsyncClient()

        user_agent = 'PyRiotApi {0} Python/{1[0]}.{1[1]} httpx/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, httpx.__version__)

        self.headers = {
            'X-Riot-Token': self.__token,
            'User-Agent': self.user_agent
        }

    async def request(self, route: Route) -> Any:        
        response = await self._session.get(
            route.url,
            params = route.params,
            headers = self.headers
        )
        return response.json()