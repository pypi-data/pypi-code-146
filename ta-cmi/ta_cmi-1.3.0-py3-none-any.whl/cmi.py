from typing import List

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .const import ReadOnlyClass
from .device import _LOGGER, Device


class CMI(BaseAPI, metaclass=ReadOnlyClass):
    """Main class to interact with CMI."""

    def __init__(
        self, host: str, username: str, password: str, session: ClientSession = None
    ) -> None:
        """Initialize."""
        super().__init__(username, password, session)
        self.host = host
        self.username = username
        self.password = password

    async def get_devices(self) -> List[Device]:
        """List connected devices."""
        _LOGGER.debug("Receive list of nodes from C.M.I")
        url: str = f"{self.host}/INCLUDE/can_nodes.cgi?_=1"
        data: str = await self._make_request_no_json(url)

        _LOGGER.debug("Received list of nodes from C.M.I: %s", data)

        node_ids: List[str] = data.split(";")

        devices: List[Device] = []

        for node_id in node_ids:
            if len(node_id) == 0:
                continue
            devices.append(
                Device(node_id, self.host, self.username, self.password, self.session)
            )

        return devices
