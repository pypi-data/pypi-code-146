import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from fractal_tokens.services.jwk import AutomaticJwkService, Jwk
from fractal_tokens.services.jwt.asymmetric import (
    AsymmetricJwtTokenService,
    ExtendedAsymmetricJwtTokenService,
)
from fractal_tokens.services.jwt.automatic import AutomaticJwtTokenService
from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService


def rsa_key_pair():
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=512,  # use at least 4096 in production
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("utf-8")

    return private_key, key.public_key()


if __name__ == "__main__":
    private_key, public_key = rsa_key_pair()
    secret_key = "**SECRET**"
    kid = str(uuid.uuid4())
    jwk_service = AutomaticJwkService(
        jwks=[
            Jwk(
                id=kid,
                public_key=public_key.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo,
                ).decode("utf-8"),
            )
        ]
    )

    asymmetric_token_service = AsymmetricJwtTokenService(
        issuer="example", private_key=private_key, public_key=public_key
    )
    extended_asymmetric_token_service = ExtendedAsymmetricJwtTokenService(
        issuer="example",
        private_key=private_key,
        kid=kid,
    )
    automatic_token_service = AutomaticJwtTokenService(
        issuer="example", secret_key=secret_key, jwk_service=jwk_service
    )
    symmetric_token_service = SymmetricJwtTokenService(
        issuer="example", secret_key=secret_key
    )

    # asymmetric/automatic
    token = asymmetric_token_service.generate({})
    print("asymmetric token:", token)

    payload = automatic_token_service.verify(token)
    print("payload:", payload)

    # extended asymmetric/automatic
    token = extended_asymmetric_token_service.generate({})
    print("extended asymmetric token:", token)

    payload = automatic_token_service.verify(token)
    print("payload:", payload)

    # ssymmetric/automatic
    token = symmetric_token_service.generate({})
    print("symmetric token:", token)

    payload = automatic_token_service.verify(token)
    print("payload:", payload)
