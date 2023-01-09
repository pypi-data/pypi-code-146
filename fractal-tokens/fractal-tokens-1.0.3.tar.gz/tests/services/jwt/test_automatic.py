import pytest


def test_symmetric_automatic(symmetric_jwt_token_service, automatic_jwt_token_service):
    token = symmetric_jwt_token_service.generate({})
    assert automatic_jwt_token_service.verify(token)


def test_extended_asymmetric_automatic(
    extended_asymmetric_jwt_token_service, automatic_jwt_token_service
):
    token = extended_asymmetric_jwt_token_service.generate({})
    assert automatic_jwt_token_service.verify(token)


def test_extended_asymmetric_automatic_no_kid(
    asymmetric_jwt_token_service, automatic_jwt_token_service
):
    token = asymmetric_jwt_token_service.generate({})
    assert automatic_jwt_token_service.verify(token)


def test_automatic_get_unverified_claims(
    symmetric_jwt_token_service, automatic_jwt_token_service
):
    token = symmetric_jwt_token_service.generate({})
    claims = automatic_jwt_token_service.get_unverified_claims(token)
    assert set(claims.keys()) == {"iss", "sub", "exp", "nbf", "iat", "jti", "typ"}
    assert claims["typ"] == "access"


def test_automatic_error(automatic_jwt_token_service):
    from fractal_tokens.exceptions import TokenInvalidException

    with pytest.raises(TokenInvalidException):
        automatic_jwt_token_service.verify("token")


def test_automatic_no_public_key_error(
    extended_asymmetric_jwt_token_service,
    automatic_jwt_token_service_with_empty_local_jwk_service,
):
    from fractal_tokens.exceptions import NotAllowedException

    token = extended_asymmetric_jwt_token_service.generate({})
    with pytest.raises(NotAllowedException):
        automatic_jwt_token_service_with_empty_local_jwk_service.verify(token)


def test_automatic_wrong_algorithm(
    symmetric_jwt_token_service, automatic_jwt_token_service
):
    symmetric_jwt_token_service.algorithm = "HS512"
    from fractal_tokens.exceptions import NotAllowedException

    token = symmetric_jwt_token_service.generate({})
    with pytest.raises(NotAllowedException):
        automatic_jwt_token_service.verify(token)


def test_automatic_generate(automatic_jwt_token_service):
    from fractal_tokens.exceptions import NotImplementedException

    with pytest.raises(NotImplementedException):
        automatic_jwt_token_service.generate({})
