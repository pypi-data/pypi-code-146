import pytest


@pytest.fixture
def dummy_token_service():
    from fractal_tokens.services.dummy import DummyJsonTokenService

    yield DummyJsonTokenService()
