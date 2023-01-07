from typing import Dict

from jose import jwt

from fractal_tokens.services.jwt import JwtTokenService
from fractal_tokens.settings import ACCESS_TOKEN_EXPIRATION_SECONDS


class SymmetricJwtTokenService(JwtTokenService):
    def __init__(self, issuer: str, secret_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.issuer = issuer
        self.secret_key = secret_key
        self.algorithm = "HS256"

    def generate(
        self,
        payload: Dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        return jwt.encode(
            self._prepare(payload, token_type, seconds_valid, self.issuer),
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=self.algorithm)

    def get_unverified_claims(self, token: str) -> dict:
        return jwt.get_unverified_claims(token)
