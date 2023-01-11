"""Classes / Methods to assist with monitoring continued operation of
tootboot."""
import logging
from typing import Optional
from typing import TypeVar

import aiohttp

from . import __display_name__
from .control import Configuration

HC = TypeVar("HC", bound="HealthChecks")

logger = logging.getLogger(__display_name__)


class HealthChecks:
    """Class to make monitoring the operation of tootboot with Healthchecks
    (healthchecks.io) easier."""

    def __init__(self: HC, config: Configuration) -> None:
        self.base_url = config.health.base_url
        self.uid = config.health.uuid

    async def check(self: HC, data: str = "", check_type: Optional[str] = None) -> None:
        """Check in with a Healthchecks installation.

        Keyword Arguments:
            data (string):
                Data to send along with the check in. Can be used to include a short
                status along with the check in.
            check_type (string):
                - Type of check in. An empty (None) check_type signals an ok check in
                  and also the successful completion of an earlier 'start' check in
                  type.
                - check_type of 'start' signals the start of a process
                - check_type of 'fail' signals the failure. This can include the
                  failure of an earlier start check in
        """
        url = self.base_url + self.uid
        if check_type is not None:
            url = url + "/" + check_type
        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.post(url=url, data=data):
                    pass
            check_type = "OK" if check_type is None else check_type
            logger.debug("Monitoring ping sent of type: %s", check_type)
        except aiohttp.ClientError as check_error:
            logger.error('During Monitoring "OK Ping" we got: %s', check_error)

    async def check_ok(self: HC, data: str = "") -> None:
        """Convenience method to signal an OK completion of a process."""
        await self.check(data=data)

    async def check_start(self: HC, data: str = "") -> None:
        """Convenience method to signal the start of a process."""
        await self.check(data=data, check_type="start")

    async def check_fail(self: HC, data: str = "") -> None:
        """Convenience method to signal the failure of a process."""
        await self.check(data=data, check_type="fail")
