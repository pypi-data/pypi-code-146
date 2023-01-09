import pytest


def test_dummy_ok(dummy_token_service):
    token = dummy_token_service.generate({})
    assert dummy_token_service.verify(token)


def test_dummy_error(dummy_token_service):
    from fractal_tokens.exceptions import TokenInvalidException

    with pytest.raises(TokenInvalidException):
        dummy_token_service.verify("token")


def test_dummy_get_unverified_claims(dummy_token_service):
    token = dummy_token_service.generate({})
    assert dummy_token_service.get_unverified_claims(token)


def test_dummy_payload_error(dummy_token_service):
    from fractal_tokens.exceptions import InvalidPayloadException

    with pytest.raises(InvalidPayloadException):
        dummy_token_service.generate({"claim": "error"})
