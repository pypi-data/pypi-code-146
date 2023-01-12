import asyncio

import aiohttp
import pytest
import pytest_asyncio

from aiotaipit import SimpleTaipitAuth, TaipitApi
from .common import (
    TEST_USERNAME,
    TEST_PASSWORD,
    TEST_CLIENT_ID,
    TEST_CLIENT_SECRET
)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="class")
@pytest.mark.asyncio
async def auth() -> SimpleTaipitAuth:
    async with aiohttp.ClientSession() as _session:
        _auth = SimpleTaipitAuth(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            session=_session,
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET
        )
        yield _auth
        # some finalization


@pytest_asyncio.fixture(scope="class")
@pytest.mark.asyncio
async def api(auth: SimpleTaipitAuth) -> TaipitApi:
    _api = TaipitApi(auth)
    yield _api
    # some finalization
