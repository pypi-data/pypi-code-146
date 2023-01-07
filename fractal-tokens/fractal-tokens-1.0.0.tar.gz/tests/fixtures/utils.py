import uuid

import pytest


@pytest.fixture
def secret_key():
    return str(uuid.uuid4())


@pytest.fixture
def app_name():
    return "fractal-roles"


@pytest.fixture
def app_env():
    return "test"


@pytest.fixture
def app_domain():
    return "karibu.online"
