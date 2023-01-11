from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import aiohttp


class ESPHomeDashboard:
    """Class to interact with the ESPHome dashboard."""

    def __init__(self, url: str, session: aiohttp.ClientSession) -> None:
        """Initialize."""
        self._url = url
        self._session = session

    async def request(self, method, path, **kwargs) -> dict:
        """Make a request to the dashboard."""
        resp = await self._session.request(method, f"{self._url}/{path}", **kwargs)
        resp.raise_for_status()
        return await resp.json()

    async def get_config(self, configuration: str) -> dict | None:
        """Get a configuration."""
        try:
            return await self.request(
                "GET", "json-config", params={"configuration": configuration}
            )
        except aiohttp.ClientResponseError as err:
            if err.status == 404:
                return None
            raise

    async def get_encryption_key(self, configuration: str) -> str | None:
        """Get the encryption key for a configuration."""
        config = await self.get_config(configuration)

        if not config:
            return None

        return config.get("api", {}).get("encryption", {}).get("key")
