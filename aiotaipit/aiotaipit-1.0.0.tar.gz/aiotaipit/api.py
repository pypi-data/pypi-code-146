"""Taipit API wrapper."""

from __future__ import annotations

import logging
from typing import cast, List

from aiohttp import hdrs

from .auth import AbstractTaipitAuth
from .const import DEFAULT_API_URL, SECTIONS_ALL, \
    PARAM_ACTION, PARAM_SECTIONS, GET_ENTRIES, PARAM_ID

_LOGGER = logging.getLogger(__name__)


class TaipitApi:
    """Class to communicate with the Taipit API."""
    _api_url: str

    def __init__(self, auth: AbstractTaipitAuth, api_url: str = DEFAULT_API_URL):
        """Initialize the API and store the auth."""
        self._auth = auth
        self._api_url = api_url

    async def async_request(self, method: str, url: str, **kwargs) -> dict:
        """Make async request to api endpoint"""
        _url = f"{self._api_url}/{url}"
        _LOGGER.debug(
            "Request %s with data %s",
            _url,
            kwargs
        )
        resp = await self._auth.request(method, _url, **kwargs)
        if not resp.ok and _LOGGER.isEnabledFor(logging.DEBUG):
            body = await resp.text()
            _LOGGER.debug(
                "Request failed with status=%s, headers=%s, body=%s",
                resp.status,
                resp.headers,
                body,
            )
        resp.raise_for_status()
        data = await resp.json()
        _LOGGER.debug(
            "Request finished with status=%s, headers=%s, data=%s",
            resp.status,
            resp.headers,
            data
        )
        return cast(dict, data)

    async def async_get(self, url: str, **kwargs) -> dict:
        """Make async get request to api endpoint"""
        return await self.async_request(hdrs.METH_GET, url, **kwargs)

    async def async_get_all_readings(self) -> dict:
        """Get all readings."""
        _url = 'meter/list-all'
        return await self.async_get(_url)

    async def async_get_meter_readings(self, meter_id: int) -> dict:
        """Get readings for meter."""
        _url = 'bmd/all'
        params = {PARAM_ID: meter_id}
        return await self.async_get(_url, params=params)

    async def async_get_meters(self) -> dict:
        """Get current user meters."""
        _url = 'meter/list-owner'
        return await self.async_get(_url)

    async def async_get_meter_info(self, meter_id: int) -> dict:
        """Get info for meter."""
        _url = 'meter/get-id'
        params = {PARAM_ID: meter_id}
        return await self.async_get(_url, params=params)

    async def async_get_current_user(self) -> dict:
        """Get current user info."""
        _url = 'user/getuser'
        return await self.async_get(_url)

    async def async_get_user_info(self, user_id: str) -> dict:
        """Get specified user info."""
        _url = f'user/getuserinfo/{user_id}'
        return await self.async_get(_url)

    async def async_get_warnings(self) -> dict:
        """List warnings."""
        _params = {PARAM_ACTION: GET_ENTRIES}
        _url = f'warnings/list'
        return await self.async_get(_url, params=_params)

    async def async_get_settings(self, sections: List[str] = SECTIONS_ALL) -> dict:
        """Get settings"""
        _params = {PARAM_SECTIONS: ','.join(sections)}
        _url = f'config/settings'
        return await self.async_get(_url, params=_params)
