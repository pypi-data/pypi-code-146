from typing import Any
from typing import Dict

import aiohttp


async def request(
    hub, ctx, method: str, path: str, query_params: Dict[str, str], data: Dict[str, Any]
):
    url = "/".join((ctx.acct.endpoint_url, path))
    async with aiohttp.ClientSession(
        loop=hub.pop.Loop, raise_for_status=True, auth=ctx.acct.auth
    ) as session:
        async with session.request(
            url=url,
            method=method.lower(),
            allow_redirects=True,
            params=query_params,
            data=data,
        ) as response:
            return await response.json()
