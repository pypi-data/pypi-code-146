"""Asynchronous Python Client for Bepacom EcoPanel BACnet interface"""

import asyncio
import json
import socket
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from time import strftime
from typing import Any, Union

import aiohttp
import async_timeout
from typing_extensions import assert_never
from yarl import URL

from .exceptions import (EcoPanelConnectionClosed, EcoPanelConnectionError,
                         EcoPanelConnectionTimeoutError,
                         EcoPanelEmptyResponseError, EcoPanelError)
from .models import Device, DeviceDict, Object


@dataclass
class Interface:
    """Main class for handling BACnet Add-on"""

    host: str
    timeout: int = 30
    port: int = 80
    session: Union[aiohttp.client.ClientSession, None] = None

    _client: Union[aiohttp.ClientWebSocketResponse, None] = None
    _close_session: bool = False
    _device_dict: Union[DeviceDict, None] = None

    @property
    def connected(self) -> bool:
        """Returns True when the Interface is connected"""

        if self._client is not None and not self._client.closed:
            return True

    async def connect(self) -> None:
        """ "Connect to the websocket of the BACnet Add-on"""

        if self.connected:
            return

        if not self._device_dict:
            # Wait for a devicelist if there's no device list
            await self.update()

        url = URL.build(scheme="ws", host=self.host, port=self.port, path="/ws")
        # For example: ws://host:80/ws

        try:
            self._client = await self.session.ws_connect(url=url, heartbeat=30)
        except (
            aiohttp.WSServerHandshakeError,
            aiohttp.ClientConnectionError,
        ) as exception:
            raise EcoPanelConnectionError(
                "Error occurred while communicating with Ecopanel add-on"
                f" on WebSocket at {self.host}"
            ) from exception

    async def listen(self, callback: Callable[[DeviceDict], None]):
        if not self._client or not self.connected or not self._device_dict:
            raise EcoPanelError("Not connected to a EcoPanel WebSocket")

        while not self._client.closed:
            message = await self._client.receive()

            if message.type == aiohttp.WSMsgType.ERROR:
                raise EcoPanelConnectionError(self._client.exception())

            if message.type == aiohttp.WSMsgType.TEXT:
                message_data = message.json()
                device_dict = self._device_dict.update_from_data(data=message_data)
                callback(device_dict)

            if message.type in (
                aiohttp.WSMsgType.CLOSE,
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.CLOSING,
            ):
                raise EcoPanelConnectionClosed(
                    f"Connection to the EcoPanel WebSocket on {self.host} has been closed"
                )

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket of the EcoPanel."""
        if not self._client or not self.connected:
            return

        await self._client.close()

    async def request(
        self,
        uri: str = "",
        method: str = "GET",
        data: Union[dict[str, Any], None] = None,
    ) -> Any:
        """Handle a request to the EcoPanel."""
        url = URL.build(scheme="http", host=self.host, port=self.port, path=uri)

        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=data,
                    headers=headers,
                )

            content_type = response.headers.get("Content-Type", "")
            if response.status // 100 in [4, 5]:
                contents = await response.read()
                response.close()

                if content_type == "application/json":
                    raise EcoPanelError(
                        response.status, json.loads(contents.decode("utf8"))
                    )
                raise EcoPanelError(
                    response.status, {"message": contents.decode("utf8")}
                )

            if "application/json" in content_type:
                response_data = await response.json()
                if (
                    method == "POST"
                    and uri == "/apiv1/json"
                    and self._device_dict is not None
                    and data is not None
                ):
                    self._device_dict.update_from_data(data)
            else:
                response_data = await response.text()

        except asyncio.TimeoutError as exception:
            raise EcoPanelConnectionTimeoutError(
                f"Timeout occurred while connecting to EcoPanel API at {self.host}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise EcoPanelConnectionError(
                f"Error occurred while communicating with EcoPanel API at {self.host}"
            ) from exception

        return response_data

    async def update(self, full_update: bool = False) -> DeviceDict:
        """Get all information about the device in a single call.
        This method updates all EcoPanel information available with a single API
        call.
        Args:
            full_update: Force a full update from the EcoPanel Device.
        Returns:
            EcoPanel data.
        Raises:
            EcoPanelEmptyResponseError: The EcoPanel API returned an empty response.
        """
        if self._device_dict is None or full_update:
            if not (data := await self.request("/apiv1/json")):
                raise EcoPanelEmptyResponseError(
                    f"EcoPanel API at {self.host} returned an empty API"
                    " response on full update"
                )

            self._device_dict = DeviceDict(data)

            return self._device_dict

    async def write_property(
        self,
        deviceid: str,
        objectid: str,
        presentValue: Union[int, float, str, bool, None] = None,
        outOfService: Union[bool, None] = None,
        covIncrement: Union[int, float, None] = None,
    ) -> None:
        """Method to write values to an object of a device"""

        data_to_send = {"deviceid": deviceid, "objectid": objectid}

        # Check if optional values are present
        if presentValue:
            data_to_send.update({"presentValue": presentValue})
        if outOfService:
            data_to_send.update({"outOfService": outOfService})
        if covIncrement:
            data_to_send.update({"covIncrement": covIncrement})

        await self.request(
            "/apiv1/{}/{}".format(deviceid, objectid), method="POST", data=data_to_send
        )

    async def websocket_write_property(
        self,
        deviceid: str,
        objectid: str,
        presentValue: Union[int, float, str, bool, None] = None,
        outOfService: Union[bool, None] = None,
        covIncrement: Union[int, float, None] = None,
    ) -> None:
        """Method to write values to an object of a device through websocket"""

        if not self._client or not self.connected or not self._device_dict:
            raise EcoPanelError("Not connected to an EcoPanel WebSocket")

        data_to_send = {deviceid: {objectid: dict()}}

        # Check if optional values are present
        if presentValue:
            data_to_send[deviceid][objectid].update({"presentValue": presentValue})
        if outOfService:
            data_to_send[deviceid][objectid].update({"outOfService": outOfService})
        if covIncrement:
            data_to_send[deviceid][objectid].update({"covIncrement": covIncrement})

        await self._client.send_json(data_to_send)

    async def close(self) -> None:
        """Close open client (WebSocket) session."""
        await self.disconnect()
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self):
        """Async enter.
        Returns:
            The EcoPanel object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        await self.close()
