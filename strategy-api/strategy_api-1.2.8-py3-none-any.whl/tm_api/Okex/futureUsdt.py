"""
1. 只支持单币种保证金模式
2. 只支持全仓模式
3. 只支持单向持仓模式
"""
import base64
import hashlib
import hmac
import json
import time
from copy import copy
from datetime import datetime, timedelta
from threading import Lock
from types import TracebackType
from typing import Any, Dict, List

# 实盘 API地址
from urllib.parse import urlencode

from strategy_api.event.engine import EventEngine
from strategy_api.tm_api.api.rest.rest_client import RestClient, Request, Response
from strategy_api.tm_api.api.websocket.websocket_client import WebsocketClient
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import Status, OrderType, Direction, Interval, TickData, BarData, Product, ContractData, \
    Exchange, DataType, HistoryRequest, PositionSide, OrderRequest, Offset, OrderData, CancelRequest
from strategy_api.tm_api.tools import get_order_type, symbol_deal

REST_HOST: str = "https://www.okx.com"

# 实盘Websocket API地址
PUBLIC_WEBSOCKET_HOST: str = "wss://ws.okx.com:8443/ws/v5/public"
PRIVATE_WEBSOCKET_HOST: str = "wss://ws.okx.com:8443/ws/v5/private"

# 委托状态映射
STATUS_OKEX2VT: Dict[str, Status] = {
    "live": Status.NOTTRADED,
    "effective": Status.ALLTRADED,
    "partially_filled": Status.PARTTRADED,
    "filled": Status.ALLTRADED,
    "canceled": Status.CANCELLED
}

# 委托类型映射
ORDERTYPE_OKEX2VT: Dict[str, OrderType] = {
    "limit": OrderType.LIMIT,
    "market": OrderType.MARKET,
    "conditional": OrderType.MARKET
}
ORDERTYPE_VT2OKEX: Dict[OrderType, str] = {v: k for k, v in ORDERTYPE_OKEX2VT.items()}

# 买卖方向映射
DIRECTION_OKEX2VT: Dict[str, Direction] = {
    "buy": Direction.LONG,
    "sell": Direction.SHORT
}
DIRECTION_VT2OKEX: Dict[Direction, str] = {v: k for k, v in DIRECTION_OKEX2VT.items()}

# 合约数据全局缓存字典
symbol_contract_map: Dict[str, ContractData] = {}

INTERVAL_VT2OKEX: Dict[Interval, str] = {
    Interval.MINUTE: "1m",
    Interval.MINUTE_3: "3m",
    Interval.MINUTE_5: "5m",
    Interval.MINUTE_15: "15m",
    Interval.MINUTE_30: "30m",
    Interval.HOUR: "1H",
    Interval.HOUR_2: "2H",
    Interval.HOUR_4: "4H",
}


class OkexFutureUsdtGateway(BaseGateway):
    """
    vn.py用于对接OKEX统一账户的交易接口。
    """

    default_setting: Dict[str, Any] = {
        "key": "",
        "secret": "",
        "Passphrase": "",
        "proxy_host": "",
        "proxy_port": 0,
    }
    exchange: Exchange = Exchange.OKEX
    product: Product = Product.U_FUTURES
    symbolMap: dict = dict()

    def __init__(self, event_engine: EventEngine, order_switch: bool = False, bar_switch: bool = False,
                 tick_switch: bool = False) -> None:
        """init"""
        super().__init__(event_engine, order_switch, bar_switch, tick_switch)

        self.market_ws_api: "OkexWebsocketPublicApi" = OkexWebsocketPublicApi(self)
        self.trade_ws_api: "OkexWebsocketPrivateApi" = OkexWebsocketPrivateApi(self)
        self.rest_api: "OkexRestApi" = OkexRestApi(self)

        self.fail_send_order: int = 0

    def connect(self, setting: dict) -> None:
        """连接交易接口"""
        key: str = setting["key"]
        secret: str = setting["secret"]
        passphrase: str = setting["Passphrase"]

        if isinstance(setting["proxy_host"], str):
            proxy_host: str = setting["proxy_host"]
        else:
            proxy_host: str = ""

        if isinstance(setting["proxy_port"], int):
            proxy_port: int = setting["proxy_port"]
        else:
            proxy_port: int = 0

        self.rest_api.connect(
            key,
            secret,
            passphrase,
            proxy_host,
            proxy_port,
        )

        self.market_ws_api.connect(
            proxy_host,
            proxy_port
        )

        self.trade_ws_api.connect(
            key,
            secret,
            passphrase,
            proxy_host,
            proxy_port,
        )

    # 订阅数据
    def subscribe(self, symbol: str, data_type: DataType, interval: Interval = None) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        if data_type == DataType.TICK:
            self.market_ws_api.subscribe(new_symbol)
        elif data_type == DataType.BAR:
            if interval:
                self.market_ws_api.subscribe(new_symbol, interval)
            else:
                print(f"订阅失败，k 线数据未定义间隔时间")
        else:
            print(f"订阅失败，未知数据类型: {data_type}")

    # 获取历史K线
    def query_history(self, symbol: str, interval: Interval, hour: int = 0, minutes: int = 0) -> List[BarData]:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        end: datetime = datetime.now()
        if hour:
            start: datetime = end - timedelta(hours=hour + 1)
        elif minutes:
            start: datetime = end - timedelta(minutes=minutes + 1)
        else:
            print("分钟，小时参数都为0, 查询k线失败")
            return []

        req: HistoryRequest = HistoryRequest(
            symbol=new_symbol,
            start=start,
            end=end,
            interval=interval
        )
        return self.rest_api.query_history(req)

    def new_order_id(self) -> str:
        return self.rest_api.get_order_id()

    # 多头买进
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

        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange
        )
        return self.send_order(original_req, orderid)

    # 多头卖出
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
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange
        )
        return self.send_order(original_req, orderid)

    # 空头买进
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
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange
        )
        return self.send_order(original_req, orderid)

    # 空头卖出
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
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange
        )
        return self.send_order(original_req, orderid)

    # 发送订单
    def send_order(self, req: OrderRequest, orderid: str):
        self.fail_send_order = 0
        self.rest_api.send_order(req, orderid)

    # 撤销订单
    def cancel_order(self, orderid: str, symbol: str) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        req: CancelRequest = CancelRequest(
            orderid=orderid,
            symbol=new_symbol,
            exchange=self.exchange
        )
        self.rest_api.cancel_order(req)

    def close(self) -> None:
        """关闭连接"""
        self.rest_api.stop()
        self.trade_ws_api.stop()
        self.market_ws_api.stop()


class OkexRestApi(RestClient):
    """"""

    def __init__(self, gateway: OkexFutureUsdtGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexFutureUsdtGateway = gateway

        self.key: str = ""
        self.secret: str = ""
        self.passphrase: str = ""
        self.simulated: bool = False

        self.order_count: int = 0
        self.connect_time: int = 0

    def sign(self, request: Request) -> Request:
        """生成欧易V5签名"""
        # 签名
        timestamp: str = generate_timestamp()
        request.data = json.dumps(request.data)

        if request.params:
            path: str = request.path + "?" + urlencode(request.params)
        else:
            path: str = request.path

        msg: str = timestamp + request.method + path + request.data
        signature: bytes = generate_signature(msg, self.secret)

        # 添加请求头
        request.headers = {
            "OK-ACCESS-KEY": self.key,
            "OK-ACCESS-SIGN": signature.decode(),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json"
        }

        if self.simulated:
            request.headers["x-simulated-trading"] = "1"

        return request

    def connect(
            self,
            key: str,
            secret: str,
            passphrase: str,
            proxy_host: str,
            proxy_port: int,
    ) -> None:
        """连接REST服务器"""
        self.key = key
        self.secret = secret.encode()
        self.passphrase = passphrase

        self.connect_time = int(datetime.now().strftime("%y%m%d%H%M%S"))

        self.init(REST_HOST, proxy_host, proxy_port)
        self.start()
        print("OKEX REST API启动成功")

        self.query_time()

    def query_time(self) -> None:
        """查询时间"""
        self.add_request(
            "GET",
            "/api/v5/public/time",
            callback=self.on_query_time
        )

    def on_query_time(self, packet: dict, request: Request) -> None:
        """时间查询回报"""
        timestamp: int = int(packet["data"][0]["ts"])
        server_time: datetime = datetime.fromtimestamp(timestamp / 1000)
        local_time: datetime = datetime.now()
        msg: str = f"服务器时间：{server_time}，本机时间：{local_time}"

    def on_error(
            self,
            exception_type: type,
            exception_value: Exception,
            tb: TracebackType,
            request: Request
    ) -> None:
        """触发异常回报"""
        msg: str = f"触发异常，状态码：{exception_type}，信息：{exception_value}"
        print(msg)

    def query_history(self, req: HistoryRequest) -> List[BarData]:
        """
        查询历史数据
        K线数据每个粒度最多可获取最近1440条
        """
        buf: Dict[datetime, BarData] = {}
        start_time: str = str(int(time.mktime(req.start.timetuple()) * 1000))
        end_time: str = str(int(time.mktime(req.end.timetuple()) * 1000))

        limit: int = 300
        path: str = "/api/v5/market/candles"

        while True:
            # 创建查询参数
            params: dict = {
                "instId": req.symbol,
                "bar": INTERVAL_VT2OKEX[req.interval],
                "limit": limit
            }

            if end_time:
                params["after"] = end_time
            if start_time:
                params["before"] = start_time

            # 从服务器获取响应
            resp: Response = self.request(
                "GET",
                path,
                params=params
            )

            # 如果请求失败则终止循环
            if resp.status_code // 100 != 2:
                msg = f"获取历史数据失败，状态码：{resp.status_code}，信息：{resp.text}"
                print(msg)
                break
            else:
                data: dict = resp.json()

                if not data["data"]:
                    m = data["msg"]
                    msg = f"获取历史数据为空，{m}"
                    print(msg)
                    break

                for bar_list in data["data"]:
                    bar: BarData = BarData(
                        symbol=self.gateway.symbolMap[req.symbol],
                        exchange=self.gateway.exchange,
                        volume=float(bar_list[5]),
                        turnover=float(bar_list[7]),
                        open_price=float(bar_list[1]),
                        high_price=float(bar_list[2]),
                        low_price=float(bar_list[3]),
                        close_price=float(bar_list[4]),
                        datetime=generate_datetime(bar_list[0]),
                        endTime=generate_datetime(bar_list[0])
                    )
                    bar.endTime = None
                    buf[bar.datetime] = bar

                begin: str = data["data"][-1][0]
                end: str = data["data"][0][0]
                msg: str = f"获取历史数据成功，{req.symbol} - {req.interval.value}，{generate_datetime(begin)} - {generate_datetime(end)}"
                if len(data) < limit:
                    break
                # # 更新结束时间
                end_time = begin
            time.sleep(0.5)

        index: List[datetime] = list(buf.keys())
        index.sort()

        history: List[BarData] = [buf[i] for i in index]
        return history

    def get_order_id(self) -> str:
        self.order_count += 1
        count_str = str(self.order_count).rjust(6, "0")
        orderid = f"{self.connect_time}{count_str}"
        return orderid

    def send_order(self, req: OrderRequest, orderid: str):

        order: OrderData = req.create_order_data(
            orderid,
        )
        self.gateway.on_order(order)
        if req.positionSide == PositionSide.ONEWAY:
            params: dict = {
                "instId": req.symbol,  # 标的
                "tdMode": "cross",  # 交易模式
                "clOrdId": orderid,  # 用户定义的ID
                "side": DIRECTION_VT2OKEX[req.direction],  # 方向
                "sz": str(req.volume)  # 数量
            }
            if req.offset == Offset.CLOSE:
                params['reduceOnly'] = True
        else:
            if (req.direction == Direction.SHORT and req.offset == Offset.OPEN) or (
                    req.direction == Direction.LONG and req.offset == Offset.CLOSE):
                position_side = "short"
            else:
                position_side = "long"
            params: dict = {
                "instId": req.symbol,  # 标的
                "posSide": position_side,
                "tdMode": "cross",  # 交易模式
                "clOrdId": orderid,  # 用户定义的ID
                "side": DIRECTION_VT2OKEX[req.direction],  # 方向
                "sz": str(req.volume)  # 数量
            }
        if req.type == OrderType.LIMIT:
            params['ordType'] = "limit"
            params['px'] = req.price  # 价格
        else:
            params['ordType'] = "market"

        path: str = "/api/v5/trade/order"

        if req.type == OrderType.STOP_MARKET:
            params['slTriggerPx'] = str(req.price)  # 止损触发价
            params['slOrdPx'] = '-1'  # 止损委托价,当为 -1 时。按市价止损
            params['ordType'] = "conditional"
            path: str = "/api/v5/trade/order-algo"

        elif req.type == OrderType.TAKE_PROFIT_MARKET:
            params['tpTriggerPx'] = str(req.price)  # 止盈触发价
            params['tpOrdPx'] = '-1'  # 止盈委托价, 当为-1 时，按市价止盈
            params['ordType'] = "conditional"
            path: str = "/api/v5/trade/order-algo"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_send_order,
            data=params,
            extra={'order': order, 'req': req, 'orderid': orderid},
            on_error=self.on_send_order_error,
            on_failed=self.on_send_order_failed
        )

    def cancel_order(self, req: CancelRequest) -> None:
        data: dict = {
            "instId": req.symbol,
            "clOrdId": req.orderid,
        }

        path: str = "/api/v5/trade/cancel-order"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_cancel_order,
            data=data,
            on_failed=self.on_cancel_order_failed,
        )

    # 发送订单成功回调
    def on_send_order(self, data: dict, request: Request) -> None:
        if data['code'] != "0":
            print(f"订单被拒绝: {data}")
            if request.extra:
                order: OrderData = copy(request.extra['order'])
                order.status = Status.REJECTED
                self.gateway.on_order(order)
                print(request)

    # 发送订单失败回调
    def on_send_order_failed(self, status_code: int, request: Request) -> None:
        print(f"发送订单 失败：{status_code}, {request}")
        pass

    # 发送订单错误回调
    def on_send_order_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        if self.gateway.fail_send_order < 3:
            req: OrderRequest = copy(request.extra['req'])
            orderid: str = copy(request.extra['orderid'])
            self.send_order(req, orderid)
            self.gateway.fail_send_order += 1
            print(f"发送订单错误,重新发送, {request}")
        print(f"发送订单错误, {request}")

    # 撤销订单成功回调
    def on_cancel_order(self, data: dict, request: Request) -> None:
        print(f"撤销订单成功: {request}")

    # 撤销订单失败
    def on_cancel_order_failed(self, status_code: int, request: Request) -> None:
        print(f"撤销订单失败: {request}")


class OkexWebsocketPublicApi(WebsocketClient):
    """"""

    def __init__(self, gateway: OkexFutureUsdtGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexFutureUsdtGateway = gateway
        self.ticks: Dict[str, TickData] = {}
        self.bars: Dict[str, BarData] = {}

    def connect(
            self,
            proxy_host: str,
            proxy_port: int,
    ) -> None:
        """连接Websocket公共频道"""
        self.init(PUBLIC_WEBSOCKET_HOST, proxy_host, proxy_port, 20)
        self.start()

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        """订阅行情"""
        if interval:
            target = symbol + f"*{interval.value}"
            if target in self.bars:
                return
            bar: BarData = BarData(
                symbol=symbol,
                datetime=datetime.now(),
                endTime=datetime.now(),
                interval=interval,
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.bars[target] = bar
            args = [
                {"channel": f"candle{interval.value}", "instId": symbol}
            ]
        else:
            if symbol in self.ticks:
                return
            tick: TickData = TickData(
                symbol=symbol,
                datetime=datetime.now(),
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.ticks[symbol] = tick
            args = [
                {"channel": "tickers", "instId": symbol}
            ]

        req: dict = {
            "op": "subscribe",
            "args": args
        }
        self.send_packet(req)

    def on_connected(self) -> None:
        """连接成功回报"""
        args = []
        for target in self.bars:
            symbol, interval = target.split("*")
            d = {"channel": f"candle{interval}", "instId": symbol}
            args.append(d)
        for target in self.ticks:
            d = {"channel": "tickers", "instId": target}
            args.append(d)
        if args:
            req: dict = {
                "op": "subscribe",
                "args": args
            }
            self.send_packet(req)
        print("Okex Websocket Public API连接成功")
        pass

    def on_disconnected(self) -> None:
        """连接断开回报"""
        pass
        # print("Okex Websocket Public API连接断开")

    def on_packet(self, packet: dict) -> None:
        """推送数据回报"""
        if "event" in packet:
            event: str = packet["event"]
            if event == "subscribe":
                return
            elif event == "error":
                code: str = packet["code"]
                msg: str = packet["msg"]
                print(f"Okex Websocket Public API请求异常, 状态码：{code}, 信息：{msg}")
        else:
            channel: str = packet["arg"]["channel"]
            symbol: str = packet["arg"].get("instId")
            data: list = packet['data']
            if channel == "tickers":
                for d in data:
                    tick: TickData = self.ticks[symbol]
                    tick.last_price = float(d["last"])
                    tick.open_price = float(d["open24h"])
                    tick.high_price = float(d["high24h"])
                    tick.low_price = float(d["low24h"])
                    tick.volume = float(d["vol24h"])
                    if tick.last_price:
                        self.gateway.on_tick(copy(tick))

            elif channel.startswith("candle"):
                for d in data:
                    if d[8] == "1":
                        bar: BarData = self.bars[symbol + f"*{channel.split('e')[-1]}"]
                        bar.volume = float(d[5])
                        bar.turnover = float(d[7])
                        bar.open_price = float(d[1])
                        bar.high_price = float(d[2])
                        bar.low_price = float(d[3])
                        bar.close_price = float(d[4])
                        bar.datetime = generate_datetime(str(d[0]))
                        bar.endTime = None
                        self.gateway.on_bar(copy(bar))

    def on_error(self, exception_type: type, exception_value: Exception, tb) -> None:
        """触发异常回报"""
        msg: str = f"Okex 公共频道触发异常，类型：{exception_type}，信息：{exception_value}"
        print(msg)


class OkexWebsocketPrivateApi(WebsocketClient):
    """"""

    def __init__(self, gateway: OkexFutureUsdtGateway) -> None:
        """构造函数"""
        super().__init__()

        self.gateway: OkexFutureUsdtGateway = gateway

        self.key: str = ""
        self.secret: str = ""
        self.passphrase: str = ""

        self.reqid: int = 0
        self.order_count: int = 0
        self.connect_time: int = 0

        self.callbacks: Dict[str, callable] = {
            "login": self.on_login,
            "orders": self.on_order,
            "orders-algo": self.on_order,
            "error": self.on_api_error
        }

        self.reqid_order_map: Dict[str, OrderData] = {}

    def connect(
            self,
            key: str,
            secret: str,
            passphrase: str,
            proxy_host: str,
            proxy_port: int
    ) -> None:
        """连接Websocket私有频道"""
        self.key = key
        self.secret = secret.encode()
        self.passphrase = passphrase
        self.connect_time = int(datetime.now().strftime("%y%m%d%H%M%S"))
        self.init(PRIVATE_WEBSOCKET_HOST, proxy_host, proxy_port, 20)
        self.start()

    def on_connected(self) -> None:
        """连接成功回报"""
        self.login()

    def on_disconnected(self) -> None:
        """连接断开回报"""
        pass
        # print("Websocket Private API连接断开")

    def on_packet(self, packet: dict) -> None:
        """推送数据回报"""
        if "event" in packet:
            cb_name: str = packet["event"]
        elif "op" in packet:
            cb_name: str = packet["op"]
        else:
            cb_name: str = packet["arg"]["channel"]

        callback: callable = self.callbacks.get(cb_name, None)
        if callback:
            callback(packet)

    def on_error(self, exception_type: type, exception_value: Exception, tb) -> None:
        """触发异常回报"""
        msg: str = f"私有频道触发异常，类型：{exception_type}，信息：{exception_value}"
        print(msg)

    def on_api_error(self, packet: dict) -> None:
        """用户登录请求回报"""
        code: str = packet["code"]
        msg: str = packet["msg"]
        print(f"Websocket Private API请求失败, 状态码：{code}, 信息：{msg}")

    def on_login(self, packet: dict) -> None:
        """用户登录请求回报"""
        if packet["code"] == '0':
            self.subscribe_topic()
        else:
            print("Websocket Private API登录失败")

    def login(self) -> None:
        """用户登录"""
        timestamp: str = str(time.time())
        msg: str = timestamp + "GET" + "/users/self/verify"
        signature: bytes = generate_signature(msg, self.secret)

        okex_req: dict = {
            "op": "login",
            "args":
                [
                    {
                        "apiKey": self.key,
                        "passphrase": self.passphrase,
                        "timestamp": timestamp,
                        "sign": signature.decode("utf-8")
                    }
                ]
        }
        self.send_packet(okex_req)

    def on_order(self, packet: dict) -> None:
        """委托更新推送"""
        data: list = packet["data"]
        for d in data:
            order: OrderData = parse_order_data(d)
            self.gateway.on_order(order)

    def subscribe_topic(self) -> None:
        """订阅委托推送"""
        okex_req: dict = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "orders",
                    "instType": "ANY"
                },
                {
                    "channel": "orders-algo",
                    "instType": "ANY"
                },
            ]
        }
        self.send_packet(okex_req)


def generate_datetime(timestamp: str) -> datetime:
    """generate time"""
    dt: datetime = datetime.fromtimestamp(int(timestamp) / 1000)
    return dt


def generate_timestamp() -> str:
    """生成时间戳"""
    now: datetime = datetime.utcnow()
    timestamp: str = now.isoformat("T", "milliseconds")
    return timestamp + "Z"


def generate_signature(msg: str, secret_key: str) -> bytes:
    """生成签名"""
    return base64.b64encode(hmac.new(secret_key, msg.encode(), hashlib.sha256).digest())


def parse_order_data(data: dict) -> OrderData:
    """解析委托回报数据"""
    order_id: str = data["clOrdId"]

    order: OrderData = OrderData(
        symbol=data["instId"],
        exchange=Exchange.OKEX,
        type=ORDERTYPE_OKEX2VT[data["ordType"]],
        orderid=order_id,
        direction=DIRECTION_OKEX2VT[data["side"]],
        offset=Offset.NONE,
        traded=0,
        price=0,
        volume=0,
        datetime=generate_datetime(data["cTime"]),
        status=STATUS_OKEX2VT[data["state"]],
    )
    # if data['px'] != "":
    #     order.price = float(data['px'])
    # else:
    #     order.price = None
    return order
