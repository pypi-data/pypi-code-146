from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from fractal_tokens.services.generic import TokenPayload, TokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def rsa_key_pair():
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

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


def get_token_payload(
    *,
    token_service: TokenService,
    typ: str = "access",
):
    def _get_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
        return token_service.verify(token, typ=typ)

    return _get_payload
