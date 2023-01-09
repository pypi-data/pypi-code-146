import pytest


def test_symmetric_ok(symmetric_jwt_token_service):
    token = symmetric_jwt_token_service.generate({})
    assert symmetric_jwt_token_service.verify(token, typ="access")


def test_symmetric_default_10_mins_valid(symmetric_jwt_token_service):
    from fractal_tokens.settings import ACCESS_TOKEN_EXPIRATION_SECONDS

    token = symmetric_jwt_token_service.generate({}, seconds_valid=0)
    payload = symmetric_jwt_token_service.verify(token)

    assert payload.exp - payload.iat == ACCESS_TOKEN_EXPIRATION_SECONDS


def test_symmetric_default_1_day_valid(symmetric_jwt_token_service):
    from fractal_tokens.settings import REFRESH_TOKEN_EXPIRATION_SECONDS

    token = symmetric_jwt_token_service.generate(
        {}, token_type="refresh", seconds_valid=0
    )
    payload = symmetric_jwt_token_service.verify(token, typ="refresh")

    assert payload.exp - payload.iat == REFRESH_TOKEN_EXPIRATION_SECONDS


def test_symmetric_get_unverified_claims(symmetric_jwt_token_service):
    token = symmetric_jwt_token_service.generate({})
    claims = symmetric_jwt_token_service.get_unverified_claims(token)
    assert set(claims.keys()) == {"iss", "sub", "exp", "nbf", "iat", "jti", "typ"}
    assert claims["typ"] == "access"


def test_symmetric_expired(symmetric_jwt_token_service):
    token = symmetric_jwt_token_service.generate({}, seconds_valid=-1)
    from fractal_tokens.exceptions import TokenExpiredException

    with pytest.raises(TokenExpiredException):
        symmetric_jwt_token_service.verify(token)


def test_symmetric_verify_wrong_typ(symmetric_jwt_token_service):
    token = symmetric_jwt_token_service.generate({})
    from fractal_tokens.exceptions import TokenInvalidException

    with pytest.raises(TokenInvalidException):
        symmetric_jwt_token_service.verify(token, typ="refresh")
