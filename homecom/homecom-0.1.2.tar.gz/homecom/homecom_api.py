import asyncio
from asyncio import run
from typing import List
from .abstract_auth import AbstractAuth

from .air_conditioner import AirConditioner


class HomecomApi:
    """Class to communicate with the HomeCom API."""

    def __init__(self, auth: AbstractAuth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_acs(self) -> List[AirConditioner]:
        resp = await self.auth.request("get", "pointt-api/api/v1/gateways")
        print(await resp.text())
        resp.raise_for_status()
        acs = filter(lambda x: x["deviceType"] == "rac", await resp.json())
        return await asyncio.gather(*[self.async_get_ac(ac['deviceId']) for ac in acs])

    async def async_get_ac(self, device_id: int) -> AirConditioner:
        resp = await self.auth.request("get", f"pointt-api/api/v1/gateways/{device_id}/resource/airConditioning"
                                              "/standardFunctions")
        print(await resp.text())
        resp.raise_for_status()
        return AirConditioner(device_id, await resp.json(), self.auth)
