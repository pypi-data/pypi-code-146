import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Jwk:
    id: str
    public_key: str


class JwkService(ABC):
    @abstractmethod
    def get_jwks(self, issuer: str = "") -> List[Jwk]:
        raise NotImplementedError


class LocalJwkService(JwkService):
    def __init__(self, jwks: List[Jwk]):
        self.jwks = jwks

    def get_jwks(self, issuer: str = "") -> List[Jwk]:
        return self.jwks


class RemoteJwkService(JwkService):
    def __init__(self, endpoint: str = "/public/keys"):
        self.endpoint = endpoint

    def get_jwks(self, issuer: str = "") -> List[Jwk]:
        from urllib.request import (  # needs to be here to be able to mock in tests
            urlopen,
        )

        jsonurl = urlopen(f"{issuer}{self.endpoint}")
        return [Jwk(**k) for k in json.loads(jsonurl.read())]


class AutomaticJwkService(JwkService):
    def __init__(self, jwks: List[Jwk], endpoint: str = "/public/keys"):
        self.local_jwk_service = LocalJwkService(jwks)
        self.remote_jwk_service = RemoteJwkService(endpoint)

    def get_jwks(self, issuer: str = "") -> List[Jwk]:
        if issuer.startswith("http"):
            return self.remote_jwk_service.get_jwks(issuer)
        else:
            return self.local_jwk_service.get_jwks(issuer)
