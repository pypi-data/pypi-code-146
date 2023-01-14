
from enum import Enum
from pydantic.dataclasses import dataclass
import dataclasses
from typing import Optional


# For sending
class OrderType(str, Enum):
    market = "market"
    limit = "limit"
    stop_loss = "stop-loss"
    take_profit = "take-profit"
    stop_loss_limit = "stop-loss-limit"
    take_profit_limit = "take-profit-limit"
    settle_position = "settle-position"


class OrderSide(str, Enum):
    buy = "BUY"
    sell = "SELL"


class OrderStatus(str, Enum):
    new = "NEW"
    pending = "PENDING"
    rejected = "REJECTED"
    active = "ACTIVE"
    canceled = "CANCELED"
    filled = "FILLED"
    expired = "EXPIRED"


def is_final_state(status: OrderStatus):
    return status in [OrderStatus.canceled, OrderStatus.rejected, OrderStatus.canceled, OrderStatus.expired, OrderStatus.filled]



@dataclass
class Order:
    """
    Sample
    {
            "account_id": "aaa",
            "order_id": "19848525",
            "client_oid": "1613571154900",
            "order_type": "LIMIT",
            "time_in_force": "GOOD_TILL_CANCEL",
            "side": "BUY",
            "exec_inst": [],
            "quantity": "0.0100",
            "limit_price": "50000.0",
            "order_value": "500.000000",
            "maker_fee_rate": "0.000250",
            "taker_fee_rate": "0.000400",
            "avg_price": "0.0",
            "cumulative_quantity": "0.0000",
            "cumulative_value": "0.000000",
            "cumulative_fee": "0.000000",
            "status": "ACTIVE",
            "update_user_id": "fd797356-55db-48c2-a44d-157aabf702e8",
            "order_date": "2021-02-17",
            "instrument_name": "BTCUSD-PERP",
            "fee_instrument_name": "USD",
            "create_time": 1613575617173,
            "create_time_ns": "1613575617173123456",
            "update_time": 1613575617173
        }
    """

    account_id: str
    order_id: str
    create_time: int
    create_time_ns: int
    client_oid: Optional[str] = ""
    order_type: Optional[str] = ""
    time_in_force: Optional[str] = ""
    side: Optional[str] = ""
    exec_inst: Optional[list[str]] = dataclasses.field(default_factory=list)
    quantity: Optional[str] = ""
    limit_price: Optional[str] = ""
    order_value: Optional[str] = ""
    maker_fee_rate: Optional[str] = ""
    taker_fee_rate: Optional[str] = ""
    avg_price: Optional[str] = ""
    cumulative_quantity: Optional[str] = ""
    cumulative_value: Optional[str] = ""
    cumulative_fee: Optional[str] = ""
    status: Optional[str] = ""
    update_user_id: Optional[str] = ""
    order_date: Optional[str] = ""
    instrument_name: Optional[str] = ""
    fee_instrument_name: Optional[str] = ""
    update_time: Optional[int] = 0



__all__ = [
    "OrderStatus",
    "OrderType",
    "OrderSide",
    "Order",
]