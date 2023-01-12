# tick 数据: 最后的市场交易、订单快照、盘中市场统计
from dataclasses import dataclass
from datetime import datetime

# tick 数据处理
from enum import Enum
from types import TracebackType
from typing import Union, Callable, Type, Any

CALLBACK_TYPE = Callable[[Union[dict, list], "Request"], None]
ON_FAILED_TYPE = Callable[[int, "Request"], None]
ON_ERROR_TYPE = Callable[[Type, Exception, TracebackType, "Request"], None]


# ---------------------------------枚举-----------------------------
class DataType(Enum):
    TICK = "tick"
    BAR = "bar"


class Interval(Enum):
    """
    Interval of bar data.

    """
    MINUTE = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"

    HOUR = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"


# 订单状态类型
class Status(Enum):
    """
    Order status.
    """
    SUBMITTING = "SUBMITTING"  # 提交中 status
    NOTTRADED = "NOTTRADED"  # 没有交易 status
    PARTTRADED = "PARTTRADED"  # 部分交易 status
    ALLTRADED = "ALLTRADED"  # 全部交易 status
    CANCELLED = "CANCELLED"  # 撤单 status
    REJECTED = "REJECTED"  # 拒单 status


ACTIVE_STATUSES = set([Status.SUBMITTING, Status.NOTTRADED, Status.PARTTRADED])


# 订单、交易、仓位等的 方向描述
class Direction(Enum):
    LONG = "Long"  # 多
    SHORT = "Short"  # 空


# 订单类型
class OrderType(Enum):
    """
    Order type.
    """
    LIMIT = "LIMIT"  # 限价单
    MARKET = "MARKET"  # 市价单
    STOP_MARKET = "STOP_MARKET"  # 市价止损
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"  # 世价止盈
    STOP_LOSS_PROFIT = "STOP_LOSS_PROFIT"  # 止盈止损


class PositionSide(Enum):
    ONEWAY = "ONE_WAY"
    TWOWAY = "TWO_WAY"


# 清算：指订单、成交中的描述
class Offset(Enum):
    NONE = ""
    OPEN = "OPEN"  # 开
    CLOSE = "CLOSE"  # 关


# 产品类型
class Product(Enum):
    SPOT = "SPOT"  # 现货
    U_FUTURES = "U_FUTURES"  # 合约
    B_FUTURES = "B_FUTURES"  # 合约


# 交易所名称
class Exchange(Enum):
    BINANCE = "BINANCE"
    OKEX = "OKEX"


# -----------------------------------------------------------

@dataclass
class BarData:
    symbol: str
    datetime: datetime
    endTime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    exchange: Exchange = None  # 交易所
    product: Product = None


@dataclass
class TickData:
    symbol: str
    datetime: datetime

    volume: float = 0
    turnover: float = 0
    last_price: float = 0
    last_volume: float = 0
    limit_up: float = 0
    limit_down: float = 0

    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    pre_close: float = 0
    localtime: datetime = None
    exchange: Exchange = None  # 交易所
    product: Product = None


# order 数据：当前挂单
@dataclass
class OrderData:
    symbol: str
    orderid: str

    type: OrderType = OrderType.LIMIT
    direction: Direction = None
    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    traded: float = 0
    traded_price: float = 0
    status: Status = Status.SUBMITTING
    datetime: datetime = datetime.now()
    update_time: datetime = datetime.now()
    reference: str = ""
    rejected_reason: str = ""  # Order Rejected Reason
    exchange: Exchange = None  # 交易所

    # 检查订单是否有效。
    def is_active(self) -> bool:
        return self.status in ACTIVE_STATUSES

    # 创建 一个测序订单请求数据
    def create_cancel_request(self) -> "CancelRequest":
        return CancelRequest(
            orderid=self.orderid, symbol=self.symbol
        )


# 订单请求数据 发送到特定网关以创建新订单
@dataclass
class OrderRequest:
    """
    Request sending to specific gateway for creating a new order.
    """

    symbol: str
    direction: Direction  # 做多做空方向
    type: OrderType  # 订单类型： 限价、市价、市价止盈、止损
    volume: float  # 交易量
    price: float = 0  # 价格
    offset: Offset = Offset.NONE  # 抵消
    reference: str = ""  # 参考
    positionSide: PositionSide = PositionSide.ONEWAY
    exchange: Exchange = None  # 交易所

    stop_loss_price: float = 0  # 止损触发价格
    stop_profit_price: float = 0  # 止盈触发价

    def create_order_data(self, orderid: str) -> OrderData:
        order: OrderData = OrderData(
            symbol=self.symbol,
            orderid=orderid,
            type=self.type,
            direction=self.direction,
            offset=self.offset,
            price=self.price,
            volume=self.volume,
            reference=self.reference,
            exchange=self.exchange
        )
        return order


@dataclass
class CancelRequest:
    """
    """

    orderid: str
    symbol: str
    exchange: Exchange = None  # 交易所


@dataclass
class TradeData:
    symbol: str
    orderid: str
    tradeid: str = ""
    direction: Direction = None

    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    datetime: datetime = None
    exchange: Exchange = None  # 交易所


@dataclass
class HistoryRequest:
    symbol: str
    start: datetime
    end: datetime = None
    interval: Interval = None
    exchange: Exchange = None  # 交易所


@dataclass
class ContractData:
    symbol: str  # 简称
    exchange: Exchange  # 交易所
    name: str  # 全称
    product: Product  # 类型
    size: float  # 合约乘数
    pricetick: float  # 下单价格精度
    min_volume: float = float(1)  # 最小下单数量
