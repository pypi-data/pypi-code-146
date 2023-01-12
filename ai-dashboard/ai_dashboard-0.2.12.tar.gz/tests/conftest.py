import os
import pytest

from ai_dashboard.api.client import Client


TEST_TOKEN = os.getenv("TEST_TOKEN")


@pytest.fixture(scope="session")
def test_token() -> str:
    return TEST_TOKEN


@pytest.fixture(scope="session")
def test_client(test_token: str) -> Client:
    return Client(test_token)
