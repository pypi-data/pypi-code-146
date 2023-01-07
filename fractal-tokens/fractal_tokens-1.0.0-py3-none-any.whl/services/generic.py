import uuid
from abc import ABC, abstractmethod
from calendar import timegm
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Type

from fractal_tokens.exceptions import InvalidPayloadException
from fractal_tokens.settings import (
    ACCESS_TOKEN_EXPIRATION_SECONDS,
    REFRESH_TOKEN_EXPIRATION_SECONDS,
)


class Service(
    ABC
):  # TODO copied from fractal-toolkit until services are extracted to separate package
    @classmethod
    def install(cls, *args, **kwargs):
        yield cls()

    def is_healthy(self) -> bool:
        return True


@dataclass
class TokenPayload:
    iss: str  # Issuer
    sub: str  # Subject
    exp: int  # Expiration Time
    nbf: int  # Not Before
    iat: int  # Issued At
    jti: str  # JWT ID
    typ: str  # Type of token (custom)


class TokenService(Service):
    def __init__(self, token_payload_cls: Type[TokenPayload] = TokenPayload):
        self.token_payload_cls = token_payload_cls

    @abstractmethod
    def generate(
        self,
        payload: dict,
        token_type: str = "access",
        seconds_valid: int = ACCESS_TOKEN_EXPIRATION_SECONDS,
    ) -> str:
        raise NotImplementedError

    def _prepare(
        self, payload: dict, token_type: str, seconds_valid: int, issuer: str
    ) -> dict:
        payload_contract = not set(payload.keys()) or set(payload.keys()) & set(
            self.token_payload_cls.__dataclass_fields__.keys()
        )
        if not payload_contract:
            raise InvalidPayloadException(
                f"The supplied payload fields ({set(payload.keys())}) are not known to "
                f"'{self.token_payload_cls}' ({set(self.token_payload_cls.__dataclass_fields__.keys())})"
            )
        utcnow = timegm(datetime.utcnow().utctimetuple())
        if not seconds_valid:
            seconds_valid = (
                REFRESH_TOKEN_EXPIRATION_SECONDS
                if token_type == "refresh"
                else ACCESS_TOKEN_EXPIRATION_SECONDS
            )
        payload.update(
            asdict(
                TokenPayload(
                    iat=utcnow,
                    nbf=utcnow,
                    jti=str(uuid.uuid4()),
                    iss=issuer,
                    exp=utcnow + seconds_valid,
                    typ=token_type,
                    sub=payload.get("sub", ""),
                )
            )
        )
        return payload

    @abstractmethod
    def verify(self, token: str, *, typ: str = "access") -> TokenPayload:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_unverified_claims(self, token: str) -> dict:
        raise NotImplementedError
