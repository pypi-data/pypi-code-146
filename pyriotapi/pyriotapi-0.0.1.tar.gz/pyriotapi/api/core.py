from .enums import Region
from ..http import HTTPClient, Route


class BaseEndpoint:
    def __init__(self, http: HTTPClient):
        self._http = http

    async def fetch(self, route: Route):
        return await self._http.request(route)

class BaseLoLEndpoint(BaseEndpoint):
    
    async def fetch(self, region: Region, path: str, **params):
        if not isinstance(region, Region):
            raise TypeError(
                'Argument region must be `{0.__name__}` not `{1.__name__}`'
                .format(Region, type(region))
            )
        route = Route.riot(region.value, path, **params)
        return await super().fetch(route)