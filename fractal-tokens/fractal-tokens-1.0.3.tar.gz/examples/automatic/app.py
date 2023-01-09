import uuid

from automatic.utils import rsa_key_pair
from cryptography.hazmat.primitives import serialization

from fractal_tokens.services.jwk import AutomaticJwkService, Jwk
from fractal_tokens.services.jwt.asymmetric import (
    AsymmetricJwtTokenService,
    ExtendedAsymmetricJwtTokenService,
)
from fractal_tokens.services.jwt.automatic import AutomaticJwtTokenService
from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService

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
