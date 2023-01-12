import dataclasses
from decimal import Decimal
from typing import Any, Optional

from pydantic.dataclasses import dataclass


@dataclass
class OrderDescr:
    pair: str
    price: Decimal
    price2: Decimal
    type: str
    ordertype: str


@dataclass
class Order:
    userref: str
    status: str
    opentm: int
    starttm: int
    expiretm: int
    descr: OrderDescr
    vol: Decimal
    vol_exec: Decimal
    cost: Decimal
    price: Decimal
    refid: Optional[str] = ""
    fee: Optional[str] = ""
    stopprice: Optional[str] = ""
    limitprice: Optional[str] = ""
    trigger: Optional[str] = ""
    misc: Optional[str] = ""
    oflags: Optional[str] = ""
    trades: Optional[list[Any]] = dataclasses.field(default_factory=list)
