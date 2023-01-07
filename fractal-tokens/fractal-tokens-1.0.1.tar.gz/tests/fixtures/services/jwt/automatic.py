import pytest


@pytest.fixture
def automatic_jwt_token_service(secret_key, local_jwk_service):
    from fractal_tokens.services.jwt.automatic import AutomaticJwtTokenService

    yield AutomaticJwtTokenService(
        issuer="test",
        secret_key=secret_key,
        jwk_service=local_jwk_service,
    )


@pytest.fixture
def automatic_jwt_token_service_with_empty_local_jwk_service(
    secret_key, empty_local_jwk_service
):
    from fractal_tokens.services.jwt.automatic import AutomaticJwtTokenService

    yield AutomaticJwtTokenService(
        issuer="test",
        secret_key=secret_key,
        jwk_service=empty_local_jwk_service,
    )
