import dataclasses
from decimal import Decimal
from typing import Any, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Order:
    userref: str
    status: str
    opentm: int
    starttm: int
    expiretm: int
    descr: dict[str, Any]
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
