import time

from strategy_api.event.engine import Event, EventEngine, EVENT_TICK, EVENT_BAR, EVENT_ORDER
from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.Binance.futureInverse import BinanceFutureInverseGateway
from strategy_api.tm_api.Okex.futureUsdt import OkexFutureUsdtGateway

from strategy_api.tm_api.object import Interval, TickData, BarData, OrderData, DataType, PositionSide

api_setting = {
    "key": "",
    "secret": "",
    "proxy_host": "",
    "proxy_port": 0,
    "Passphrase": ""
}


def process_tick_event(event: Event):
    tick: TickData = event.data
    print("tick 数据：")
    print(tick)


def process_bar_event(event: Event):
    bar: BarData = event.data
    print("k 线 数据：")
    print(bar)


def process_order_event(event: Event):
    order: OrderData = event.data
    print("订单 数据：")
    print(order)

# # ---------------------------币安api---------------------------


# event_engine = EventEngine()
# event_engine.start()
# event_engine.register(EVENT_TICK, process_tick_event)
# event_engine.register(EVENT_BAR, process_bar_event)
# event_engine.register(EVENT_ORDER, process_order_event)
#
# # api = BinanceFutureUsdtGateway(event_engine)
# api = BinanceFutureInverseGateway(event_engine)
# # # 链接api
# api.connect(api_setting)
# time.sleep(5)
# history_kline = api.query_history(symbol="BTCUSD_PERP", interval=Interval.MINUTE, minutes=20)
# print(len(history_kline))
# #
# # 订阅 1 分钟 K 线 行情
# api.subscribe(symbol="BTCUSD_PERP", data_type=DataType.BAR, interval=Interval.MINUTE)

# 订阅 tick 行情
# api.subscribe(symbol="BTCUSDT", data_type=DataType.TICK)

# 下单
# api.buy(symbol="BTCUSDT", volume=0.01, price=9999, maker=True, stop_loss=False, stop_profit=False)
#
# # 撤销订单
# api.cancel_order(orderid="xl_1111111", symbol="BTCUSDT")
# # -------------------------------------------------------------
# ---------------------------Okex api---------------------------


# 订阅 1 分钟 K 线 行情
# api.subscribe(symbol="BTC-USDT", interval=Interval.MINUTE)

# # 订阅 tick 行情



event_engine = EventEngine()
event_engine.start()
event_engine.register(EVENT_TICK, process_tick_event)
event_engine.register(EVENT_BAR, process_bar_event)
event_engine.register(EVENT_ORDER, process_order_event)

api = OkexFutureUsdtGateway(event_engine)

# 链接api
api.connect(api_setting)
time.sleep(5)
# 查询历史K线数据
# history_kline = api.query_history(symbol="BTC-USDT-SWAP", interval=Interval.MINUTE, minutes=20)
# for l in history_kline:
#     print(l)
# api.subscribe(symbol="BTC-USDT-SWAP", data_type=DataType.BAR, interval=Interval.MINUTE)

# api.subscribe(symbol="BTC-USDT-SWAP", data_type=DataType.TICK)
# 市价单下单
# api.short(symbol="SOL-USDT-SWAP", volume=1, price=9999, maker=False, stop_loss=False, stop_profit=False, position_side=PositionSide.TWOWAY)
# 限价单下单
api.buy(symbol="SOL-USD-SWAP", volume=1, price=10, maker=False, stop_loss=False, stop_profit=False)
# print(orderid)
# # 撤销订单
# api.cancel_order(orderid="230104211950000001", symbol="SOL-USDT-SWAP")
# -------------------------------------------------------------

