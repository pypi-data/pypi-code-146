import logging
from collections.abc import Awaitable
from typing import Optional

from aiohttp import ClientResponse, ClientResponseError
import orjson

from aiopi.exceptions import ResponseError
from aiopi.types import JSONContent



_LOGGER = logging.getLogger(__name__)


async def handle_request(
    coro: Awaitable[ClientResponse],
    raise_for_status: bool = True,
    raise_for_error: bool = True
) -> Optional[JSONContent]:
    """Primary response handling for all HTTP requests to the PI Web API."""
    response = await coro
    
    try:
        response.raise_for_status()
    except ClientResponseError as err:
        await response.release()
        if raise_for_status:
            raise
        _LOGGER.warning("Error in client response (%i)", err.code, exc_info=True)
        return None
    
    async with response as ctx:
        data: JSONContent = await ctx.json(loads=orjson.loads)
    errors = data.get("Errors")
    
    if errors:
        if raise_for_error:
            raise ResponseError(errors)
        else:
            _LOGGER.warning("%i errors returned in response body", len(errors), extra={"errors": ", ".join(errors)})
            return None
    
    return data