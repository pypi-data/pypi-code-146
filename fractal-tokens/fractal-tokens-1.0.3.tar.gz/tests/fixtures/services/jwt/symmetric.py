import pytest


@pytest.fixture
def symmetric_jwt_token_service(secret_key):
    from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService

    yield SymmetricJwtTokenService(
        issuer="test",
        secret_key=secret_key,
    )
