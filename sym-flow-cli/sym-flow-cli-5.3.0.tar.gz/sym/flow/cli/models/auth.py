from typing import TypedDict

from sym.flow.cli.errors import InvalidTokenError


class AuthToken(TypedDict):
    access_token: str
    token_type: str
    expires_in: int

    def __init__(
        self,
        access_token: str,
        token_type: str,
        expires_in: int,
    ):
        # This is necessary instead of @dataclass due to an
        # incompatibility between dataclass + TypedDict in python3.9
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in


def parse_auth_token(json_response: dict) -> AuthToken:
    try:
        return AuthToken(
            access_token=json_response["access_token"],
            token_type=json_response["token_type"],
            expires_in=json_response["expires_in"],
        )
    except KeyError:
        raise InvalidTokenError(str(json_response))
