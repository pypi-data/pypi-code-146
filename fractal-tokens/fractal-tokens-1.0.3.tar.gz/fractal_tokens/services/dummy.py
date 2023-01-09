import json

from fractal_tokens.exceptions import TokenInvalidException
from fractal_tokens.services.generic import TokenPayload, TokenService
from fractal_tokens.settings import ACCESS_TOKEN_EXPIRATION_SECONDS


class DummyJsonTokenService(TokenService):
    def generate(
        self,
        payload: dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        return json.dumps(self._prepare(payload, token_type, seconds_valid, "dummy"))

    def verify(self, token: str, *, typ: str = "access") -> TokenPayload:
        try:
            return self.token_payload_cls(**self.decode(token))
        except Exception:
            raise TokenInvalidException()

    def decode(self, token: str) -> dict:
        return json.loads(token)

    def get_unverified_claims(self, token: str) -> dict:
        return self.decode(token)
