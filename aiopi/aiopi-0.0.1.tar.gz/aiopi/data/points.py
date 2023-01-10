import asyncio
import logging
from typing import List, Sequence, Union

from pydantic import ValidationError

from aiopi.data.request import handle_request
from aiopi.exceptions import ContentError
from aiopi.http import PIClient
from aiopi.models import PISubscription
from aiopi.types import JSONContent



_LOGGER = logging.getLogger(__name__)


async def search_tags(
    client: PIClient,
    tags: Union[str, Sequence[str]],
    dataserver_web_id: str = None,
    web_id_type: str = "Full"
) -> List[PISubscription]:
    """Get the WebId for a sequence of tags.
    
    If a tag is not found or the query returns multiple results, the result
    for that tag will be `None`. Therefore you cannot use wild card searches
    for this method.
    """
    tags = [tags] if isinstance(tags, str) else list(tags)
    
    if dataserver_web_id is None:
        data = await handle_request(
            client.dataservers.list(selectedFields="Items.Name;Items.WebId")    
        )
        items = data.get("Items")
        if not items or not isinstance(items, list):
            raise ContentError(
                "Could not get dataserver WebId. No items returned in response"
            )
        dataserver_web_id = items[0]["WebId"]
        _LOGGER.debug("No dataserver provided. Defaulting to %s", items[0]["Name"])
    
    dispatch = [
        handle_request(
            client.dataservers.get_points(
                dataserver_web_id,
                nameFilter=tag,
                selectedFields="Items.Name;Items.WebId",
                webIdType=web_id_type
            )
        ) for tag in tags
    ]
    
    results: List[JSONContent] = await asyncio.gather(*dispatch)
    ret: List[PISubscription] = []
    
    for tag, result in zip(tags, results):
        items = result.get("Items")
        if not items or not isinstance(items, list) or len(items) > 1:
            ret[tag] = None
        else:
            try:
                ret.append(PISubscription(web_id=items[0]["WebId"], name=items[0]["Name"], web_id_type=web_id_type))
            except ValidationError:
                _LOGGER.warning("Subscription validation failed", exc_info=True, extra={"raw": items})
    
    return ret