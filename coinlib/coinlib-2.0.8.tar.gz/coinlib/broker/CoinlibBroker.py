import abc
import asyncio
import threading
import time
from abc import ABC ,abstractmethod
import simplejson as json
from enum import Enum
from coinlib.broker.BrokerDTO import OrderUpdateInformation, OrderCancelInfo, SelectedSymbolInfo

from typing import List

from coinlib.broker import CoinlibSessionManager
from coinlib.broker.BrokerDTO import CoinlibBrokerLoginParams, LeverageInfo, Balance, AssetInfoSummary, OpenOrders, \
    Orders, ClosedOrders, CancelOrder, Order, OpenOrderInfo, CoinlibBrokerAccount, AssetWithPrice, BrokerSymbol, \
    BrokerEvent, BrokerDetailedInfo, OrderInformation
from coinlib.helper import serializeDTO


class CoinlibBrokerListener(metaclass=abc.ABCMeta):

    def onEventReceived(self, event: BrokerEvent, data: any):
        pass



class BrokerTickerData():
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    date: str
    closeTime: str

class CoinlibBrokerWatcherThread:
    def __init__(self, brokerWorkerInstance, worker, symbol, closedCb):
        self._canceled = False
        self.brokerWorkerInstance = brokerWorkerInstance
        self.worker = worker
        self.symbol = symbol
        self.closedCb = closedCb
        self.current_task = None
        self.thread = None
        self.errorCount = 0
        self.loop = asyncio.new_event_loop()
        pass

    def run_task(self, future_task):
        t = asyncio.create_task(future_task)
        self.current_task = t
        return t

    def get_broker(self):
        return self.brokerWorkerInstance

    def get_loop(self):
        return self.loop

    def sendTicker(self, ticker: BrokerTickerData):
        self.brokerWorkerInstance.cb.onEventReceived(BrokerEvent.SymbolTicker, ticker)
        pass

    def running(self):
        return not self._canceled

    def start(self):
        self.thread = threading.Thread(target=self.runThread, args=(self.symbol,))
        self.thread.start()
        return self

    def onThreadCanceled(self):
        return self.closedCb(self)

    def runThread(self, symbol):
        try:
            while self.running():
                if self.errorCount > 5:
                    break
                processData = self.loop.run_until_complete(self.worker(symbol, self))

        except Exception as e:
            pass
        except asyncio.CancelledError as ce:
            pass

        self.onThreadCanceled()


    def cancel(self):
        self._canceled = True
        if self.current_task is not None:
            self.current_task.cancel()

    def canceled(self):
        return self._canceled


class CoinlibBrokerBasicTask:
    def __init__(self, brokerWorkerInstance, taskname, callback, closedCb):
        self._canceled = False
        self.brokerWorkerInstance = brokerWorkerInstance
        self.callback = callback
        self.taskName = taskname
        self.closedCb = closedCb
        self.current_task = None
        self.thread = None
        self.errorCount = 0
        self.loop = asyncio.new_event_loop()
        pass

    def get_broker(self):
        return self.brokerWorkerInstance

    def get_loop(self):
        return self.loop

    def run_task(self, future_task):
        t = asyncio.create_task(future_task)
        self.current_task = t
        return t

    def running(self):
        return not self._canceled

    def start(self):
        self.thread = threading.Thread(target=self.runThread, args=(self.taskName,))
        self.thread.start()
        return self

    def onThreadCanceled(self):
        return self.closedCb(self)


    def runThread(self, taskname):
        while self.running():
            try:
                if self.errorCount > 5:
                    break
                processData = self.loop.run_until_complete(self.callback(self.brokerWorkerInstance, self))

            except Exception as e2:
                self.errorCount = self.errorCount + 1
                time.sleep(5)
                pass

        self.onThreadCanceled()


    def cancel(self):
        self._canceled = True
        if self.current_task is not None:
            self.current_task.cancel()

    def canceled(self):
        return self._canceled


class CoinlibBroker(ABC):
    def __init__(self):
        self.loop = None
        self.lastSendOrders = {}
        self.price_threads = {}
        self.task_threads = {}
        self.orders : List[OrderInformation] = []
        self.cb : CoinlibBrokerListener = None
        pass

    def get_basic_quote_asset_name(self):
        return "USDT"

    def get_account(self):
        return self.account

    def get_session_id(self):
        return self.session_id

    def get_order_prefix(self):
        return self.short_session_id

    def get_cb(self):
        return self.cb

    def get_session_mng(self):
        return self.sm

    def get_loop(self):
        return self.loop

    def update_order(self, order: OpenOrderInfo):
        orderInformation = None
        for o in self.orders:
            if o.orderId == order.orderId:
                orderInformation = o
        if orderInformation is None:
            orderInformation = OrderInformation()
        orderInformation.orderId = order.orderId
        orderInformation.clientOrderId = order.clientOrderId
        self.orders.append(orderInformation)

        return True

    def sendOrderUpdateInThread(self, order: OrderUpdateInformation):

        if order.orderId in self.lastSendOrders:
            self.registrar.logger.warn("Ignoring order becuase its again: "+order.orderId)
            if order.timestamp in self.lastSendOrders[order.orderId]:
                return

        self.registrar.logger.info(json.dumps(order, default=serializeDTO))

        self.lastSendOrders[order.orderId] = [order.timestamp]
        return self.cb.onEventReceived(BrokerEvent.OrderUpdate, order)

    def sendOrderUpdate(self, order: OrderUpdateInformation):
        self.thread = threading.Thread(target=self.sendOrderUpdateInThread, args=(order,))
        self.thread.start()
        return True

    def is_order_from_session(self, clientOrderId: str):
        if clientOrderId.startswith(self.get_short_id()):
            return True
        return False

    def hasOrder(self, order: Order=None, orderId: str = None):
        if order is not None:
            for o in self.orders:
                if o.orderId == order.orderId:
                    return True
            return False
        if orderId is not None:
            for o in self.orders:
                if o.orderId == orderId:
                    return True
            return False
        return False

    def getOrder(self, order: Order=None, orderId: str = None):
        if order is not None:
            for o in self.orders:
                if o.orderId == order.orderId:
                    return o
            return False
        if orderId is not None:
            for o in self.orders:
                if o.orderId == orderId:
                    return o
            return False
        return False

    async def start_session(self, loop, session: str, short_session_id: str, account: CoinlibBrokerAccount,
                            session_manager: CoinlibSessionManager, is_restart: bool = False, cb: CoinlibBrokerListener = None):
        self.loop = loop
        self.session_id : str = session
        self.short_session_id : str = short_session_id
        self.account : CoinlibBrokerAccount = account
        self.sm : CoinlibSessionManager = session_manager
        if self.cb is None and cb is not None:
            self.cb : CoinlibBrokerListener = cb
        await self.on_start_session(is_restart)
        return await self.login("API_KEY", self.account.loginInfo)

    def get_short_id(self):
        return self.short_session_id

    def register_callback(self, callbackFunction: CoinlibBrokerListener):
        self.cb = callbackFunction
        pass

    async def stop_price_ticker(self, symbol_id: str = None) -> any:
        for key in self.price_threads:
            try:
                self.price_threads[key].cancel()
            except Exception as e:
                pass
        self.price_threads = {}

        return True

    def on_ticker_thread_closed(self, threadTicker: CoinlibBrokerWatcherThread):
        # inform about cancellation

        return True

    def on_task_thread_close(self, threadTicker: CoinlibBrokerBasicTask):
        # inform about cancellation

        return True

    def register_price_ticker(self, worker: any, symbol: str):
        self.price_threads[symbol] = CoinlibBrokerWatcherThread(self, worker, symbol, self.on_ticker_thread_closed)
        self.price_threads[symbol].start()
        return self.price_threads[symbol]

    def register_task(self, taskName: str, callback: any, singleton=True):

        if (singleton and taskName not in self.task_threads) or not singleton:
            self.task_threads[taskName] = CoinlibBrokerBasicTask(self, taskName, callback, self.on_task_thread_close)
            self.task_threads[taskName].start()
        return self.task_threads[taskName]

    def on_order_updates(self, orderUpdate: OrderUpdateInformation):
        return self.cb.onEventReceived(BrokerEvent.OrderUpdate, orderUpdate)

    def stop_all_price_ticker(self):
        for name in self.price_threads:
            try:
                self.price_threads[name].cancel()
            except Exception as e:
                pass
        self.price_threads = {}

    def stop_all_tasks(self):
        for name in self.task_threads:
            try:
                self.task_threads[name].cancel()
            except Exception as e:
                pass
        self.task_threads = {}

    async def stop_session(self):
        try:
            self.stop_all_price_ticker()
        except Exception as e:
            pass
        try:
            self.stop_all_tasks()
        except Exception as e:
            pass
        try:
            await self.shutdown()
        except Exception as e:
            pass

    @abstractmethod
    async def watch_price_ticker(self, symbol_id: str) -> SelectedSymbolInfo:
        pass

    @abstractmethod
    async def get_broker_info(self) -> BrokerDetailedInfo:
        pass

    @abstractmethod
    async def get_symbols(self) -> List[BrokerSymbol]:
        return []

    @abstractmethod
    async def get_price(self, base, quote) -> float:
        pass

    @abstractmethod
    async def on_start_session(self, is_restart: bool):
        pass

    @abstractmethod
    async def login(self, login_mode: str, login_params: CoinlibBrokerLoginParams):
        pass

    @abstractmethod
    async def shutdown(self):
        pass

    @abstractmethod
    async def get_assets(self) -> AssetInfoSummary:
        pass

    @abstractmethod
    async def get_balance(self) -> Balance:
        pass

    @abstractmethod
    async def get_open_orders(self) -> OpenOrders:
        pass

    @abstractmethod
    async def get_orders(self, symbol_id: str) -> Orders:
        pass

    @abstractmethod
    async def get_order_detail(self, order_id: str, clientOrderId: str, symbol_id: str):
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str, clientOrderId: str, symbol_id: str) -> CancelOrder:
        pass


