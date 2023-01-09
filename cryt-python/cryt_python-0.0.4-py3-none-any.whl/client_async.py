import aiohttp

from cryt.base import BaseClient


class AsyncClient(BaseClient):
    def __init__(self, base_url=None, public_key=None, private_key=None):
        super().__init__(base_url, public_key, private_key)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        headers = self._get_headers()
        self.session.headers.update(headers)
        return self

    async def __aexit__(self):
        await self.close_connection()

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()

    async def _request(self, method, uri, **kwargs):
        async with self.session.request(method, uri, **kwargs) as response:
            return await self._handle_response(response)

    async def _handle_response(self, response):
        return await response.json()

    async def _request_api(self, method, path, **kwargs):
        uri = self._create_api_uri(path)
        return await self._request(method, uri, **kwargs)

    # MarketAPI

    async def depth(self, pair, limit):
        path = "market/depth"
        params = {
            "symbol": pair,
            "limit": limit,
        }
        return await self._request_api("GET", path, params=params)
