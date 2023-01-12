""" Example showing usage of this library """

import asyncio
from pprint import pprint

import aiohttp

from aiotaipit import SimpleTaipitAuth, TaipitApi


async def main(username: str, password: str) -> None:
    """Create the aiohttp session and run the example."""
    async with aiohttp.ClientSession() as session:
        auth = SimpleTaipitAuth(username, password, session)
        api = TaipitApi(auth)

        all_readings = await api.async_get_all_readings()

        pprint(all_readings)


if __name__ == "__main__":
    _username = "guest@taipit.ru"
    _password = "guest"
    asyncio.run(main(_username, _password))
