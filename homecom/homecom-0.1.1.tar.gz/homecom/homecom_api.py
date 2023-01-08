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
        return list(map(lambda x: AirConditioner(x, self.auth), acs))

    async def async_get_ac(self, device_id: str) -> AirConditioner:
        resp = await self.auth.request("get", f"pointt-api/api/v1/gateways/{device_id}")
        print(await resp.text())
        resp.raise_for_status()
        return AirConditioner(await resp.json(), self.auth)
