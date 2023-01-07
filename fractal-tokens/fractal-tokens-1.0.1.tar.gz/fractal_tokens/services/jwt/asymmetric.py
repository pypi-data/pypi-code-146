from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PUBLIC_KEY_TYPES
from jose import jwt

from fractal_tokens.exceptions import (
    NoPrivateKeyException,
    NoPublicKeyException,
    NotAllowedException,
)
from fractal_tokens.services.jwk import JwkService
from fractal_tokens.services.jwt import JwtTokenService
from fractal_tokens.settings import ACCESS_TOKEN_EXPIRATION_SECONDS


class AsymmetricJwtTokenService(JwtTokenService):
    def __init__(
        self,
        issuer: str,
        private_key: str,
        public_key: Optional[PUBLIC_KEY_TYPES] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.issuer = issuer
        self.private_key = private_key
        self.public_key = (
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode("utf-8")
            if public_key
            else ""
        )
        self.algorithm = "RS256"

    def generate(
        self,
        payload: dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        if not self.private_key:
            raise NoPrivateKeyException(
                "Cannot generate asymmetric token since no private key provided!"
            )
        return jwt.encode(
            self._prepare(payload, token_type, seconds_valid, self.issuer),
            self.private_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict:
        if not self.public_key:
            raise NoPublicKeyException(
                "Cannot decode asymmetric token since no public key provided!"
            )
        return jwt.decode(
            token,
            self.public_key,
            algorithms=self.algorithm,
            issuer=self.issuer,
        )

    def get_unverified_claims(self, token: str) -> dict:
        return jwt.get_unverified_claims(token)


class ExtendedAsymmetricJwtTokenService(AsymmetricJwtTokenService):
    def __init__(
        self,
        issuer: str,
        private_key: str,
        kid: str,
        jwk_service: Optional[JwkService] = None,
        *args,
        **kwargs,
    ):
        super(ExtendedAsymmetricJwtTokenService, self).__init__(
            issuer, private_key, *args, **kwargs
        )
        self.kid = kid
        self.jwk_service = jwk_service

    def generate(
        self,
        payload: dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        if not self.private_key:
            raise NoPrivateKeyException(
                "Cannot generate asymmetric token since no private key supplied!"
            )
        return jwt.encode(
            self._prepare(payload, token_type, seconds_valid, self.issuer),
            self.private_key,
            algorithm=self.algorithm,
            headers={"kid": self.kid},
        )

    def decode(self, token: str) -> dict:
        if not self.jwk_service:
            raise NotAllowedException("No permission!")
        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid", None)
        if not kid:
            raise NotAllowedException("No permission!")
        claims = jwt.get_unverified_claims(token)
        for key in filter(
            lambda k: k.id == kid, self.jwk_service.get_jwks(claims["iss"])
        ):
            return jwt.decode(
                token,
                key.public_key,
                algorithms=self.algorithm,
                issuer=self.issuer,
            )
        raise NotAllowedException("No permission!")
