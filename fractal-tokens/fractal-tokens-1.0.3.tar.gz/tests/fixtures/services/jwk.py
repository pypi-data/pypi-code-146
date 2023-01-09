import pytest

from fractal_tokens.services.jwk import Jwk


@pytest.fixture
def local_jwk_service(rsa_key_pair):
    kid, private_key, public_key = rsa_key_pair

    from cryptography.hazmat.primitives import serialization

    from fractal_tokens.services.jwk import LocalJwkService

    yield LocalJwkService(
        [
            Jwk(
                id=kid,
                public_key=public_key.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf-8"),
            )
        ]
    )


@pytest.fixture
def empty_local_jwk_service():
    from fractal_tokens.services.jwk import LocalJwkService

    yield LocalJwkService([])


@pytest.fixture
def remote_jwk_service():
    from fractal_tokens.services.jwk import RemoteJwkService

    yield RemoteJwkService()


@pytest.fixture
def automatic_jwk_service(rsa_key_pair):
    kid, private_key, public_key = rsa_key_pair

    from cryptography.hazmat.primitives import serialization

    from fractal_tokens.services.jwk import AutomaticJwkService

    yield AutomaticJwkService(
        [
            Jwk(
                id=kid,
                public_key=public_key.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf-8"),
            )
        ]
    )


@pytest.fixture
def mocked_urlopen():
    class HTTPResponse:
        def read(self):
            return "{}"

    return HTTPResponse()
