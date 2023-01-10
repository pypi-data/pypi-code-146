from enum import StrEnum, auto


class SioAuth(StrEnum):
    """determines if the channel subs/pub requires the client to be authenticated and what type of auth is it"""

    no_auth = auto()
    jwt = auto()
    token = auto()
