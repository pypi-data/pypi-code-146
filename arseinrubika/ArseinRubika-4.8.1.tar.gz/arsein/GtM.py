import aiohttp
import asyncio
from json import loads
from random import choice

list_servers = []

for server_rubika in range(3):
    async def GETservers(server):
        async with aiohttp.ClientSession() as session:
            async with session.get(server) as response:
                Post =  await response.text()
                return Post
    loop = asyncio.get_event_loop()
    servers =  loads(loop.run_until_complete(GETservers("https://getdcmess.iranlms.ir/"))).get('data').get("default_api")
    servere = "https://messengerg2caddad.iranlms.ir"
    replace = servere.replace("addad",f"{servers}")
    list_servers.append(replace)


class default_api:
    def defaultapi(self):
        return choice(list_servers)
        