import json
from typing import Any, Dict

from aiohttp import BasicAuth, ClientConnectionError, ClientSession

from .const import _LOGGER, HTTP_OK, HTTP_UNAUTHORIZED


class BaseAPI:
    """Class to perform CMI API requests."""

    def __init__(
        self, username: str, password: str, session: ClientSession = None
    ) -> None:
        """Initialize."""
        self.auth = BasicAuth(username, password)
        self.session = session

        self._internal_session = False

    async def _make_request(self, url: str) -> Dict[str, Any]:
        """Retrieve data from CMI API."""
        raw_response: str = await self._make_request_no_json(url)
        data = json.loads(raw_response)

        STATUS_CODE = "Status code"

        if data[STATUS_CODE] != 0:
            _LOGGER.debug("Failed response received: %s", raw_response)

        if data[STATUS_CODE] == 0:
            return data
        elif data[STATUS_CODE] == 1:
            raise ApiError("Node not available")
        elif data[STATUS_CODE] == 2:
            raise ApiError(
                "Failure during the CAN-request/parameter not available for this device"
            )
        elif data[STATUS_CODE] == 4:
            raise RateLimitError("Only one request per minute is permitted")
        elif data[STATUS_CODE] == 5:
            raise ApiError("Device not supported")
        elif data[STATUS_CODE] == 7:
            raise ApiError("CAN Bus is busy")
        else:
            raise ApiError("Unknown error")

    async def _make_request_no_json(self, url: str) -> str:
        """Retrieve data from CMI API that is not valid json."""
        if self.session is None:
            self._internal_session = True
            self.session = ClientSession()

        try:
            async with self.session.get(url, auth=self.auth) as res:
                await self._close_session()
                if res.status == HTTP_UNAUTHORIZED:
                    raise InvalidCredentialsError("Invalid API key")
                elif res.status != HTTP_OK:
                    raise ApiError(f"Invalid response from CMI: {res.status}")

                text = await res.text()
                return text
        except ClientConnectionError:
            await self._close_session()
            raise ApiError(f"Could not connect to C.M.I")

    async def _close_session(self) -> None:
        """Close the internal session."""
        if self._internal_session:
            await self.session.close()
            self.session = None


class ApiError(Exception):
    """Raised when API request ended in error."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidCredentialsError(Exception):
    """Triggered when the credentials are invalid."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class RateLimitError(Exception):
    """Triggered when the rate limit is reached."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
