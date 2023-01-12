# 导入 strategy_api 包里面的策略模版
from strategy_api.strategies.template import StrategyTemplate
# 导入 BINANCE U 本位合约 API包
from strategy_api.tm_api.Okex.futureUsdt import OkexFutureUsdtGateway
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
        self.short_id = ""

        self.stop_loss_id = ""
        self.stop_profit_id = ""
        self.volume = 1
        self.rate_stop = 0.002

        self.open_price_list = []
        self.ma7_list = []
        self.ma30_list = []
        self.init_bar = False

    # 初始化历史k线，用于计算ma值
    def init_history_bar(self):
        okex_api = self.get_gateway("okex_api")  # 从网关插槽中获取 api
        klines = okex_api.query_history(symbol="SOL-USD-SWAP", minutes=1 * 31, interval=Interval.MINUTE)
        klines = klines[0:-1]
        self.open_price_list = [bar.close_price for bar in klines]

    # k 线数据的回调, 可以在该方法里面记录 k 线数据、分析k线数据
    def on_bar(self, bar: BarData):
        okex_api = self.get_gateway("okex_api")  # 从网关插槽中获取 api

        if not self.init_bar:
            self.init_history_bar()
            self.init_bar = True

        # 记录收盘价
        del self.open_price_list[0]
        self.open_price_list.append(bar.close_price)

        # 计算ma30、ma7
        self.calculate_ma7_ma30()

        # 寻找金叉死叉
        res = self.glod_die_fork()

        # 这里开始真正的交易
        if self.buy_switch:
            if res == 0:
                # 如果是死叉, 做空
                self.short_id = okex_api.new_order_id()
                okex_api.short(orderid=self.short_id, symbol="SOL-USD-SWAP", volume=self.volume, price=0, maker=False)
                self.buy_switch = False
            elif res == 1:
                # 如果是金叉, 做多
                self.long_id = okex_api.new_order_id()
                okex_api.buy(orderid=self.long_id, symbol="SOL-USD-SWAP", volume=self.volume, price=0, maker=False)
                self.buy_switch = False

    def glod_die_fork(self):
        # 寻找金叉死叉

        # 如果ma30、ma7 的记录小于2，那么直接返回2, 没有找到金叉死叉
        if len(self.ma7_list) < 2:
            return 2
        if self.ma7_list[-1] < self.ma30_list[-1]:
            # 死叉
            print("die")
            return 0
        elif self.ma7_list[-1] > self.ma30_list[-1]:
            # 金叉
            print("grod")
            return 1
        else:
            return 2

        # if self.ma7_list[-2] > self.ma30_list[-2] and self.ma7_list[-1] < self.ma30_list[-1]:
        #     # 死叉
        #     return 0
        # elif self.ma7_list[-2] < self.ma30_list[-2] and self.ma7_list[-1] > self.ma30_list[-1]:
        #     # 金叉
        #     return 1
        # else:
        #     return 2

    def calculate_ma7_ma30(self):
        # 计算ma7、ma30
        ma30_value = round(sum(self.open_price_list) / 30, 2)
        ma7_value = round(sum(self.open_price_list[-7:]) / 7, 2)
        print(f"ma30: {ma30_value}, ma7: {ma7_value}")

        # 记录ma30，ma7 的结果
        self.ma7_list.append(ma7_value)
        self.ma30_list.append(ma30_value)

        if len(self.ma7_list) > 2:
            del self.ma7_list[0]
            del self.ma30_list[0]

    # 获取历史k线，获取最新一根k线的开盘价
    def query_history_kline(self):
        okex_api = self.get_gateway("okex_api")
        kls = okex_api.query_history(symbol="SOL-USD-SWAP", minutes=5, interval=Interval.MINUTE)
        open_price = kls[-1].open_price
        return open_price

    # 订单 数据的回调，订单状态的改变都会通过websoket 推送到这里，例如 从提交状态 改为 全成交状态，或者提交状态 改为 撤销状态 都会推送
    # 可以在这里对仓位进行一个记录
    def on_order(self, order: OrderData):

        okex_api = self.get_gateway("okex_api")

        print(order)

        if order.status == Status.ALLTRADED and (self.long_id == order.orderid or self.short_id == order.orderid):

            # 如果订单全部成交，并且是 做的订单号，下止盈止损单
            open_price = self.query_history_kline()

            # 如果订单是做多的订单，那么按做多的方式下 止盈止损单
            if self.long_id == order.orderid:

                profit_price = round(open_price * (1 + self.rate_stop), 3)

                loss_price = round(open_price * (1 - self.rate_stop), 3)

                self.stop_profit_id = okex_api.new_order_id()
                okex_api.sell(
                            orderid=self.stop_profit_id,
                            symbol="SOL-USD-SWAP",
                            volume=self.volume,
                            price=profit_price,
                            stop_profit=True
                            )
                self.stop_loss_id = okex_api.new_order_id()

                okex_api.sell(
                              orderid=self.stop_loss_id,
                              symbol="SOL-USD-SWAP",
                              volume=self.volume,
                              price=loss_price,
                              stop_loss=True
                              )
            else:
                profit_price = round(open_price * (1 - self.rate_stop), 3)
                loss_price = round(open_price * (1 + self.rate_stop), 3)
                print(f"做空 成交, 下止盈: 触发价({profit_price})  下止损: 触发价({loss_price})")

                # 按做空的方式下止盈止损单
                self.stop_profit_id = okex_api.new_order_id()
                okex_api.cover(
                            orderid=self.stop_profit_id,
                            symbol="SOL-USD-SWAP",
                            volume=self.volume,
                            price=profit_price,
                            stop_profit=True
                            )

                self.stop_loss_id = okex_api.new_order_id()
                okex_api.cover(
                              orderid=self.stop_loss_id,
                              symbol="SOL-USD-SWAP",
                              volume=self.volume,
                              price=loss_price,
                              stop_loss=True
                              )
            # 将订单号滞空
            self.long_id = ""
            self.short_id = ""

        elif order.status == Status.ALLTRADED and (
                self.stop_profit_id == order.orderid or self.stop_loss_id == order.orderid):
            if self.stop_loss_id == order.orderid:
                print("止损成交")

                # 止损成交撤销止盈单
                # okex_api.cancel_order(orderid=self.stop_profit_id, symbol="SOL-USD-SWAP")
            elif self.stop_profit_id == order.orderid:
                print("止盈成交")

                # 止盈成交撤销止损单
                # okex_api.cancel_order(orderid=self.stop_loss_id, symbol="SOL-USD-SWAP")

            # 将止损止盈订单号滞空
            self.stop_loss_id = ""
            self.stop_profit_id = ""

            # 打开交易开关
            self.buy_switch = True


def start_strategy(api_setting):
    # 初始化策略
    s = StrategyDemo()

    # 添加 BINANCE U本位网关
    okex_gateway = s.add_gateway(OkexFutureUsdtGateway, "okex_api", api_setting)

    # 订阅数据
    okex_gateway.subscribe(symbol="SOL-USD-SWAP", data_type=DataType.BAR, interval=Interval.MINUTE)


if __name__ == '__main__':
    print("启动量化系统: 等待策略运行")
    api_setting = {
        "key": "",
        "secret": "",
        "proxy_host": "",
        "proxy_port": 0,
        "Passphrase": "Test1.123"
    }
    start_strategy(api_setting)
