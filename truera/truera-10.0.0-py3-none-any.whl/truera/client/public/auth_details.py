from base64 import b64encode
from enum import IntEnum
from typing import Optional, Sequence, Tuple, Union


def format_headers(func):

    def wrapper(self, use_http: bool = False):
        headers = func(self)
        return dict(headers) if use_http else headers

    return wrapper


# Using an IntEnum instead of Enum to avoid issues like https://stackoverflow.com/a/26636951
# Solution from https://stackoverflow.com/a/28125951.
class AuthDetailsMode(IntEnum):
    UNKNOWN = 0
    ANON_AUTH = 1
    BASIC_AUTH = 2
    TOKEN_AUTH = 3
    IMPERSONATION_AUTH = 4


class AuthDetails(object):

    def __init__(self, *, mode: Optional[AuthDetailsMode] = None, **kwargs):
        self.mode = mode
        # TODO(apoorv) We should probably validate these parameters are set based on mode.
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.token = kwargs.get("token", None)
        # works only within TruEra cluster
        self.impersonation_metadata = kwargs.get("impersonation_metadata", None)

    @format_headers
    def get_auth_headers(
        self, use_http: bool = False
    ) -> Union[dict, Sequence[Tuple]]:
        if self.username and self.password:
            user_pass_bytes = bytes(
                "{}:{}".format(self.username, self.password), 'utf-8'
            )
            user_pass_b64_encoded = b64encode(user_pass_bytes).decode("ascii")
            # Note: For grpc metadata, the keys must be lower case. Http requests perform this conversion automatically.
            return [('authorization', "Basic {}".format(user_pass_b64_encoded))]

        if self.token:
            return [('authorization', f"Bearer {self.token}")]

        return self.impersonation_metadata or []

    def redacted_print(self) -> str:
        if self.mode == AuthDetailsMode.ANON_AUTH:
            return f"Type: Anonymous"
        if self.mode == AuthDetailsMode.BASIC_AUTH:
            return f"Type: Basic Authentication, Username: {self.username}, Password: <Redacted>"
        if self.mode == AuthDetailsMode.TOKEN_AUTH:
            return f"Type: Token, Token: <Redacted>"
        if self.mode == AuthDetailsMode.IMPERSONATION_AUTH:
            return f"Type: Manual Credentials"
        return f"Type: Unknown"
