"""Fixture for tests."""
import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():  # type: ignore
    """Clean asyncio loop for each test."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
