import dataclasses
import time
from typing import Literal, Optional

from pydantic.dataclasses import dataclass

from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
from bittrade_kraken_rest.models.trade import Trade


@dataclass
class GetTradeHistoryResult:
    trades: dict[str, Trade]
    count: int


@dataclasses.dataclass
class GetTradeHistoryOptions:
    type: Literal[
        "all", "any position", "closed position", "closing position", "no position"
    ] = "all"
    trades: bool = False
    start: int = 0
    end: int = dataclasses.field(default_factory=lambda: int(time.time()))
    ofs: Optional[int] = None


def get_trade_history_request(options: Optional[GetTradeHistoryOptions] = None):
    """
    Get open orders
    :return:
    """
    data = {}
    if options:
        data = dataclasses.asdict(options)
    return prepare_private(url="/0/private/TradesHistory", data=data)


def get_trade_history_result():
    return send_and_map_to_result(GetTradeHistoryResult)
