import aiohttp

class ClientAPI:

    def __init__(
            self,
            type: str,
            value: str,
        ) -> int:

        self.url = 'https://www.thecolorapi.com/id?{}={}'.format(type, value)
    
    async def get(self):

        async with aiohttp.ClientSession() as request:

            async with request.get(self.url) as response:

                res = await response.json(encoding='utf-8')
                return res['hex']['clean']


