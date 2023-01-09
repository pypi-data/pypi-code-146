import asyncio
import logging
from typing import Dict, List

import httpx
from jose import jwt

from delphai_utils.config import get_config

logger = logging.getLogger(__name__)


public_keys = {}

# endpoint for getting all enabled JWKs
base_url = get_config("keycloak.base_url") or "https://auth.delphai.com"
url = f"{base_url}/auth/realms/delphai/protocol/openid-connect/certs"


async def decode_token(access_token: str) -> str:
    decode_args = {"audience": "delphai-gateway", "options": {"leeway": 10}}
    try:
        result = jwt.decode(access_token, public_keys, **decode_args)
        return result
    except Exception:
        _public_keys = await __async_fetch_keys()
        return jwt.decode(access_token, _public_keys, **decode_args)


class PublicKeyFetchError(Exception):
    pass


async def __async_fetch_keys() -> List[Dict]:
    global public_keys
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print("failed")
            raise PublicKeyFetchError(response.text)
        else:
            result = response.json()
            public_keys = result
            return result


async def update_public_keys(interval: int = 60 * 10):  # updates every 10 minutes
    while True:
        try:
            await __async_fetch_keys()
        except PublicKeyFetchError:
            logger.exception("Error fetching jwk from keycloak")
        await asyncio.sleep(interval)
