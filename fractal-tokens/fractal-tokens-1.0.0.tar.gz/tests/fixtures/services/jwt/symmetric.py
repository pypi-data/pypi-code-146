import pytest


@pytest.fixture
def symmetric_jwt_token_service(secret_key, app_name, app_env, app_domain):
    from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService

    yield next(
        SymmetricJwtTokenService.install(
            issuer=f"{app_name}@{app_env}.{app_domain}",
            secret_key=secret_key,
        )
    )
