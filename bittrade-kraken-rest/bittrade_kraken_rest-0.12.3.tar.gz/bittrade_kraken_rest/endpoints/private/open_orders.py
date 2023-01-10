import dataclasses
from typing import Literal, Optional

from pydantic.dataclasses import dataclass

from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result
from bittrade_kraken_rest.models.order import Order


@dataclass
class GetOpenOrdersResult:
    open: dict[str, Order]


@dataclasses.dataclass
class GetOpenOrdersOptions:
    trades: bool = False
    userref: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None
    ofs: Optional[int] = None
    closetime: Optional[Literal["open", "close", "both"]] = "both"


def get_open_orders_request(options: Optional[GetOpenOrdersOptions] = None):
    """
    Get open orders
    :return:
    """
    data = {}
    if options:
        data = dataclasses.asdict(options)
    return prepare_private(url="/0/private/OpenOrders", data=data)


def get_open_orders_result():
    return send_and_map_to_result(GetOpenOrdersResult)
