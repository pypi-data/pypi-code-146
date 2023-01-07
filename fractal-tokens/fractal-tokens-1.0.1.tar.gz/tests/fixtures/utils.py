import uuid

import pytest


@pytest.fixture
def secret_key():
    return str(uuid.uuid4())
