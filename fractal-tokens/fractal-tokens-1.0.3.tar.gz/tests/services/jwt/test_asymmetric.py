import pytest


def test_asymmetric_ok(asymmetric_jwt_token_service):
    token = asymmetric_jwt_token_service.generate({})
    assert asymmetric_jwt_token_service.verify(token)


def test_extended_asymmetric_ok(extended_asymmetric_jwt_token_service):
    token = extended_asymmetric_jwt_token_service.generate({})
    assert extended_asymmetric_jwt_token_service.verify(token)


def test_dummy_get_unverified_claims(extended_asymmetric_jwt_token_service):
    token = extended_asymmetric_jwt_token_service.generate({})
    claims = extended_asymmetric_jwt_token_service.get_unverified_claims(token)
    assert set(claims.keys()) == {"iss", "sub", "exp", "nbf", "iat", "jti", "typ"}
    assert claims["typ"] == "access"


def test_asymmetric_expired(asymmetric_jwt_token_service):
    token = asymmetric_jwt_token_service.generate({}, seconds_valid=-1)
    from fractal_tokens.exceptions import TokenExpiredException

    with pytest.raises(TokenExpiredException):
        asymmetric_jwt_token_service.verify(token)


def test_asymmetric_verify_wrong_typ(asymmetric_jwt_token_service):
    token = asymmetric_jwt_token_service.generate({})
    from fractal_tokens.exceptions import TokenInvalidException

    with pytest.raises(TokenInvalidException):
        asymmetric_jwt_token_service.verify(token, typ="refresh")


def test_extended_asymmetric_no_kid(
    asymmetric_jwt_token_service, extended_asymmetric_jwt_token_service
):
    token = asymmetric_jwt_token_service.generate({})
    from fractal_tokens.exceptions import NotAllowedException

    with pytest.raises(NotAllowedException):
        extended_asymmetric_jwt_token_service.verify(token)


def test_asymmetric_no_private_key(asymmetric_jwt_token_service_no_private_key):
    from fractal_tokens.exceptions import NoPrivateKeyException

    with pytest.raises(NoPrivateKeyException):
        asymmetric_jwt_token_service_no_private_key.generate({})


def test_asymmetric_no_public_key(asymmetric_jwt_token_service_no_public_key):
    from fractal_tokens.exceptions import NoPublicKeyException

    with pytest.raises(NoPublicKeyException):
        asymmetric_jwt_token_service_no_public_key.verify("")


def test_extended_asymmetric_no_private_key(
    extended_asymmetric_jwt_token_service_no_private_key,
):
    from fractal_tokens.exceptions import NoPrivateKeyException

    with pytest.raises(NoPrivateKeyException):
        extended_asymmetric_jwt_token_service_no_private_key.generate({})


def test_extended_asymmetric_no_jwk_service(
    extended_asymmetric_jwt_token_service_no_jwk_service,
):
    from fractal_tokens.exceptions import NotAllowedException

    with pytest.raises(NotAllowedException):
        extended_asymmetric_jwt_token_service_no_jwk_service.verify("")
