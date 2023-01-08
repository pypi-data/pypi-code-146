from typing import Dict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jose import jwt

from fractal_tokens.exceptions import NotAllowedException, NotImplementedException
from fractal_tokens.services.jwk import JwkService
from fractal_tokens.services.jwt import JwtTokenService
from fractal_tokens.services.jwt.asymmetric import (
    AsymmetricJwtTokenService,
    ExtendedAsymmetricJwtTokenService,
)
from fractal_tokens.services.jwt.symmetric import SymmetricJwtTokenService
from fractal_tokens.settings import ACCESS_TOKEN_EXPIRATION_SECONDS


class AutomaticJwtTokenService(JwtTokenService):
    def __init__(
        self, issuer: str, secret_key: str, jwk_service: JwkService, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.issuer = issuer
        self.symmetric_token_service = SymmetricJwtTokenService(
            issuer=issuer,
            secret_key=secret_key,
        )
        public_key = None
        if jwks := jwk_service.get_jwks(issuer):
            public_key = serialization.load_pem_public_key(
                jwks[0].public_key.encode("utf-8"), backend=default_backend()
            )
        self.asymmetric_token_service = AsymmetricJwtTokenService(
            issuer=issuer,
            private_key="",
            public_key=public_key,
        )
        self.extended_asymmetric_token_service = ExtendedAsymmetricJwtTokenService(
            issuer=issuer,
            private_key="",
            kid="",
            jwk_service=jwk_service,
        )

    def generate(
        self,
        payload: Dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        raise NotImplementedException(
            "Not able to generate tokens with this TokenService"
        )

    def decode(self, token: str) -> dict:
        headers = jwt.get_unverified_headers(token)
        if headers["alg"] == "HS256":
            return self.symmetric_token_service.decode(token)
        if headers["alg"] == "RS256":
            if "kid" in headers:
                return self.extended_asymmetric_token_service.decode(token)
            return self.asymmetric_token_service.decode(token)
        raise NotAllowedException("No permission!")

    def get_unverified_claims(self, token: str) -> dict:
        return jwt.get_unverified_claims(token)
