from abc import ABC
from typing import Dict, Any, List
from strategy_api.event.engine import EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.event.engine import EventEngine, Event
from strategy_api.tm_api.object import OrderData, BarData, TickData, Interval, OrderRequest, HistoryRequest, \
    PositionSide, DataType, Exchange, Product


class BaseGateway(ABC):
    # Default name for the gateway.
    default_setting: Dict[str, Any] = {}
    exchange: Exchange = None
    product: Product = None
    symbolMap: dict = dict()

    def __init__(self,
                 event_engine: EventEngine,
                 order_switch: bool = False,
                 bar_switch: bool = False,
                 tick_switch: bool = False) -> None:

        self.event_engine: EventEngine = event_engine

        self.order_call_switch = order_switch
        self.bar_call_switch = bar_switch
        self.tick_call_switch = tick_switch

    def connect(self, setting: dict) -> None:
        pass

    def buy(self,
            orderid: str,
            symbol: str,
            volume: float,  # 数量
            price: float = 0,  # 价格
            maker: bool = False,  # 限价单
            stop_loss: bool = False,  # 止损
            stop_profit: bool = False,  # 止盈
            position_side: PositionSide = PositionSide.ONEWAY,
            ):
        pass

    def sell(self,
             orderid: str,
             symbol: str,
             volume: float,  # 数量
             price: float = 0,  # 价格
             maker: bool = False,  # 限价单
             stop_loss: bool = False,  # 止损
             stop_profit: bool = False,  # 止盈
             position_side: PositionSide = PositionSide.ONEWAY,
             ):
        pass

    def short(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_profit: bool = False,  # 止盈
              position_side: PositionSide = PositionSide.ONEWAY,
              ):
        pass

    def cover(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_profit: bool = False,  # 止盈
              position_side: PositionSide = PositionSide.ONEWAY,
              ):
        pass

    def new_order_id(self) -> str:
        pass

    def send_order(self, req: OrderRequest, orderid: str):
        pass

    def cancel_order(self, orderid: str, symbol: str) -> None:
        pass

    def query_history(self, symbol: str, interval: Interval, hour: int = 0, minutes: int = 0) -> List[BarData]:
        pass

    def subscribe(self, symbol: str, data_type: DataType, interval: Interval = None) -> None:
        pass

    # 一般事件推送。
    def on_event(self, type: str, data: Any = None) -> None:
        event: Event = Event(type, data)
        self.event_engine.put(event)

    # tick 数据推送
    def on_tick(self, tick: TickData) -> None:
        if self.tick_call_switch:
            tick.symbol = self.symbolMap[tick.symbol]
            self.on_event(EVENT_TICK, tick)

    # K线数据回调
    def on_bar(self, bar: BarData):
        if self.bar_call_switch:
            bar.symbol = self.symbolMap[bar.symbol]
            self.on_event(EVENT_BAR, bar)

    # 定单事件推送
    def on_order(self, order: OrderData) -> None:
        if self.order_call_switch:
            order.symbol = self.symbolMap[order.symbol]
            self.on_event(EVENT_ORDER, order)

    def close(self) -> None:
        pass
