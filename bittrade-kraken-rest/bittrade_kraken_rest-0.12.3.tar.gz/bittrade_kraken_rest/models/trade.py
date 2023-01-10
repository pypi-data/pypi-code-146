import dataclasses
from decimal import Decimal
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Trade:
    ordertxid: str
    pair: str
    time: int
    type: str
    ordertype: str
    price: Decimal
    cost: Decimal
    fee: str
    vol: Decimal
    margin: str
    misc: Optional[str] = ""
    posstatus: Optional[str] = ""
    cprice: Optional[str] = ""
    ccost: Optional[str] = ""
    cfee: Optional[str] = ""
    cvol: Optional[str] = ""
    cmargin: Optional[str] = ""
    net: Optional[str] = ""
    trades: Optional[list[str]] = dataclasses.field(default_factory=list)
