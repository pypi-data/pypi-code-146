import datetime
import time
from abc import ABC
from typing import List, Dict, Type
from strategy_api.event.engine import EventEngine, Event, EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import TickData, BarData, OrderData, Interval


class StrategyTemplate(ABC):
    author: str = ""

    def __init__(self) -> None:
        self.event_engine: EventEngine = EventEngine()
        self.gateways: Dict[str, BaseGateway] = {}
        self.register_handler(self.process_tick_event, self.process_bar_event, self.process_order_event)

        self.init_strategy()    # 初始化引擎

    def get_gateway(self, gateway_name) -> BaseGateway:
        gateway: BaseGateway = self.gateways.get(gateway_name)
        if not gateway:
            print(f"没有该网关: {gateway_name}")
        return gateway

    def init_strategy(self):
        # 启动事件引擎
        self.event_engine.start()
        # 初始化参数
        self.init_parameters()

    # 添加网关
    def add_gateway(self,
                    gateway_class: Type[BaseGateway],
                    gateway_name,
                    api_setting: dict
                    ) -> BaseGateway:
        order_call_switch = api_setting.get("call_order_switch", False)
        bar_call_switch = api_setting.get("call_bar_switch", False)
        tick_call_switch = api_setting.get("call_tick_switch", False)

        gateway: BaseGateway = gateway_class(self.event_engine, order_call_switch, bar_call_switch, tick_call_switch)
        self.gateways[gateway_name] = gateway
        gateway.connect(api_setting)
        print(f"添加网关:{gateway_name}, 等待网关链接")
        time.sleep(10)
        return gateway

    # 事件注册
    def register_handler(self, tick_handler: callable, bar_handler: callable, order_handler: callable):
        self.event_engine.register(EVENT_TICK, tick_handler)
        self.event_engine.register(EVENT_BAR, bar_handler)
        self.event_engine.register(EVENT_ORDER, order_handler)

    # tick 数据事件推送
    def process_tick_event(self, event: Event):
        tick: TickData = event.data
        self.on_tick(tick)

    # k线 数据推送
    def process_bar_event(self, event: Event):
        bar: BarData = event.data
        self.on_bar(bar)

    # 订单 数据推送
    def process_order_event(self, event: Event):
        order: OrderData = event.data
        self.on_order(order)

    # 策略参数设置
    def init_parameters(self):
        pass

    # 策略启动时的回调。
    def on_start(self) -> None:
        pass

    # 新的tick数据更新回调。
    def on_tick(self, tick: TickData) -> None:
        pass

    # 新的bar数据更新回调。
    def on_bar(self, bar: BarData) -> None:
        pass

    # 新订单数据更新回调。
    def on_order(self, order: OrderData) -> None:
        pass

    # 记录数据
    def record_bar(self, bar: BarData):
        pass

    # 数据分析
    def deal_data(self, bar: BarData):
        pass
