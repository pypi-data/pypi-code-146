"""Common types."""
# pylint: disable=invalid-name
from enum import Enum
from typing import TypedDict


class IDTokenTyping(TypedDict, total=True):
    """ID token output format."""

    at_hash: str
    sub: str
    displayName: str
    auditTrackingId: str
    roles: list[str]
    iss: str
    tokenName: str
    given_name: str
    locale: str
    nonce: str
    aud: str
    acr: str
    # org.forgerock.openidconnect.ops: str
    s_hash: str
    azp: str
    auth_time: int
    name: str
    realm: str
    exp: int
    tokenType: str
    family_name: str
    iat: int
    email: str


class Rates(Enum):
    """Contract Rates."""

    D: str = "D"
    DT: str = "DT"
    DPC: str = "DPC"
    M: str = "M"
