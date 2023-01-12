# 导入 strategy_api 包里面的策略模版
from strategy_api.strategies.template import StrategyTemplate
# 导入 BINANCE U 本位合约 API包
from strategy_api.tm_api.Okex.futureUsdt import OkexFutureUsdtGateway
from strategy_api.tm_api.Binance.futureUsdt import BinanceFutureUsdtGateway
from strategy_api.tm_api.Binance.futureInverse import BinanceFutureInverseGateway

# 导入 strategy_api 中使用的常量对象
from strategy_api.tm_api.object import Interval, BarData, OrderData, Status, PositionSide, DataType


# 策略类
class StrategyDemo(StrategyTemplate):
    # 属性 作者(标志该策略的开发人员)
    author = "DYX"

    # 初始化方法
    def __init__(self):
        super(StrategyDemo, self).__init__()

    # 初始化策略参数
    def init_parameters(self):
        self.buy_switch = True
        self.long_id = ""
        self.stop_loss_id = ""
        self.stop_profit_id = ""
        self.volume = 1
        self.rate_stop = 0.008

    # k 线数据的回调, 可以在该方法里面记录 k 线数据、分析k线数据
    def on_bar(self, bar: BarData):
        okex_api = self.get_gateway("okex_api")
        # print(bar)
        if self.buy_switch:
            # 开多单
            self.long_id = okex_api.new_order_id()

            okex_api.buy(
                orderid=self.long_id,
                symbol="SOL-USD-SWAP",
                volume=self.volume,
                price=10
            )
            print("--------------做多")
            self.buy_switch = False

    # 获取历史k线，获取最新一根k线的开盘价
    def query_history_kline(self):
        okex_api = self.get_gateway("okex_api")
        try:
            kls = okex_api.query_history(symbol="SOL-USD-SWAP", minutes=5, interval=Interval.MINUTE)
        except Exception as e:
            kls = okex_api.query_history(symbol="SOL-USD-SWAP", minutes=5, interval=Interval.MINUTE)

        open_price = kls[-1].open_price
        return open_price

    # 订单 数据的回调，订单状态的改变都会通过websoket 推送到这里，例如 从提交状态 改为 全成交状态，或者提交状态 改为 撤销状态 都会推送
    # 可以在这里对仓位进行一个记录
    def on_order(self, order: OrderData):
        okex_api = self.get_gateway("okex_api")
        if order.status == Status.ALLTRADED and self.long_id == order.orderid:
            print("做多成交")
            open_price = self.query_history_kline()
            print(f"最新开盘价：{open_price}")
            self.stop_profit_id = okex_api.new_order_id()
            okex_api.sell(
                orderid=self.stop_profit_id,
                symbol="SOL-USD-SWAP",
                volume=self.volume,
                price=round(open_price * (1 + self.rate_stop), 3),
                stop_profit=True
            )

            self.stop_loss_id = okex_api.new_order_id()
            okex_api.sell(
                orderid=self.stop_loss_id,
                symbol="SOL-USD-SWAP",
                volume=self.volume,
                price=round(open_price * (1 - self.rate_stop), 3),
                stop_loss=True
            )

        elif order.status == Status.ALLTRADED and (
                self.stop_profit_id == order.orderid or self.stop_loss_id == order.orderid):
            # okex 不用测小止损止盈单，只要止损了，止盈单自动撤销

            if self.stop_loss_id == order.orderid:
                print("止损")
                pass
                # okex_api.cancel_order(orderid=self.stop_profit_id, symbol="SOL-USD-SWAP")
            elif self.stop_profit_id == order.orderid:
                print("止盈")
                pass
                # okex_api.cancel_order(orderid=self.stop_loss_id, symbol="SOL-USD-SWAP")

            self.buy_switch = True


def start_strategy(api_setting):
    # 初始化策略
    s = StrategyDemo()

    # 添加 BINANCE U本位网关
    okex_gateway = s.add_gateway(BinanceFutureInverseGateway, "okex_api", api_setting)

    # 订阅数据
    okex_gateway.subscribe(symbol="BTC-USD-PERP", data_type=DataType.BAR, interval=Interval.MINUTE)


if __name__ == '__main__':
    print("启动量化系统: 等待策略运行")
    api_setting = {
        "key": "",
        "secret": "",
        "proxy_host": "",
        "proxy_port": 0,
        "Passphrase": "",

        "call_order_switch": False,  # 订单数据回调 开关
        "call_tick_switch": False,  # tick数据回调 开关
        "call_bar_switch": False  # k线数据回调 开关
    }
    start_strategy(api_setting)
