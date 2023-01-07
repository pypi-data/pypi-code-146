from dataclasses import dataclass

from fractal_tokens.services.dummy import DummyJsonTokenService
from fractal_tokens.services.generic import TokenPayload


@dataclass
class TokenPayloadHello(TokenPayload):
    hello: str


if __name__ == "__main__":
    token_service = DummyJsonTokenService(TokenPayloadHello)

    token = token_service.generate(
        {
            "hello": "world",
        }
    )
    print("token:", token)

    payload = token_service.verify(token)
    print("payload:", payload)
