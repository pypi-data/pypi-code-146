from url_normalize import url_normalize
import aiohttp

class ClientUtils():
    def __init__(self, url: str):
        super().__init__()
        self.api_base = url
    headers = {}

    @staticmethod
    def setDefaultHeaders(_headers):
        ClientUtils.headers = _headers
    
    async def get(self, url: str, headers={})-> str:
        async with aiohttp.ClientSession(headers={**ClientUtils.headers, **headers}) as session:
            url=url_normalize(f'{self.api_base}/{url}')
            async with session.get(url) as resp:
                return await resp.text()
    
    async def get_stream(self, url: str, headers={})-> str:
        async with aiohttp.ClientSession(headers={**ClientUtils.headers, **headers}) as session:
            url=url_normalize(f'{self.api_base}/{url}')
            async with session.get(url) as resp:
                return await resp   

    async def post(self, url: str, headers = {}, data=None, config=None) -> str:
        async with aiohttp.ClientSession(headers={**ClientUtils.headers, **headers}) as session:
            url=url_normalize(f'{self.api_base}/{url}')
            async with session.post(url, headers=headers, data=data, params=config) as resp:
                return await resp.text()

    async def put(self, url: str, headers = {}, data=None, config=None) -> str:
        async with aiohttp.ClientSession(headers={**ClientUtils.headers, **headers}) as session:
            url=url_normalize(f'{self.api_base}/{url}')
            async with session.put(url, headers=headers, data=data, params=config) as resp:
                return await resp.text()

    async def delete(self, url: str, headers = {}) -> str:
        async with aiohttp.ClientSession(headers={**ClientUtils.headers, **headers}) as session:
            url=url_normalize(f'{self.api_base}/{url}')
            async with session.delete(url, headers=headers) as resp:
                return await resp.text()  

    async def send_stream(self, url: str, stream: str, options: dict):
        headers = {
            'content-type': options.get('type'),
            'x-end-stream': options.get('end')
        }
        config = { 'parse': options.get('parse_response') }
        return await self.post(url, headers, stream, config)
