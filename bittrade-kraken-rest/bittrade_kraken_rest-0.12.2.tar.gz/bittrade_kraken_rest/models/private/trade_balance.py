import dataclasses
from typing import TypedDict

from ..message import KrakenMessage


class GetTradeBalanceResult(TypedDict):
    eb: str
    tb: str
    m: str
    n: str
    c: str
    v: str
    e: str
    mf: str
    ml: str
    uv: str


@dataclasses.dataclass
class GetTradeBalanceResponse(KrakenMessage):
    result: GetTradeBalanceResult
