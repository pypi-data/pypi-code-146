import asyncio

import pandas as pd
from typing import List

from coinlib.broker import CoinlibBroker
from coinlib.broker.BrokerDTO import BrokerDetailedInfo, BrokerSymbol
from coinlib.brokerWorker import BrokerSession, BrokerSessionWorker
from coinlib.data.DataTable import DataTable
from coinlib.logics.broker.LogicBrokerInterface import LogicBrokerInterface
from coinlib.logics.manager.LogicJobBroker import LogicJobBroker, WrongArgumentError
from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import OrderType


class LogicOnlineJobBroker(LogicJobBroker):
    brokerInterface: LogicBrokerInterface

    def __init__(self, manager, interface: LogicBrokerInterface):
        super(LogicOnlineJobBroker, self).__init__(manager)
        self.brokerInterface = interface
        self.loop = asyncio.new_event_loop()
        self.table = DataTable()
        pass

    def getLoop(self):
        return self.loop

    def getBrokerInterface(self) -> LogicBrokerInterface:
        return self.brokerInterface

    def symbols(self) -> List[BrokerSymbol]:
        return self.getBrokerInterface().getCommand("get_symbols")

    def price(self, base, quote):
        return self.getBrokerInterface().getCommand("get_price", {"base": base, "quote": quote})

    def brokerDetails(self) -> BrokerDetailedInfo:
        return self.getBrokerInterface().getCommand("broker_info", {})

    def canLeverage(self):
        details = self.brokerDetails()
        return details["canLeverage"]

    def cancelOrder(self, clientOrderId: str):
        super().cancelOrder(clientOrderId)
        return self.getBrokerInterface().getCommand("cancel_order", {"clientOrderId": clientOrderId})

    def lastOrders(self, symbol: str):
        return self.getBrokerInterface().getCommand("get_orders", {"symbol": symbol})

    def buyAll(self, symbol: BrokerSymbol,  price=None, leverage=None,
               type: OrderType = OrderType.MARKET, group=None):
        super().buyAll(symbol, price=price, leverage=leverage, group=group)
        return self.getBrokerInterface().getCommand("buyAll", {"symbol": symbol, "type": type, "leverage": leverage, "side": "BUY", "price": price, "group": group})

    def sellAll(self, symbol: BrokerSymbol, price=None, leverage=None,
                type: OrderType = OrderType.MARKET, group=None):
        super().sellAll(symbol, price=price, leverage=leverage, group=group)
        return self.getBrokerInterface().getCommand("sellAll", {"symbol": symbol, "type": type, "leverage": leverage, "side": "SELL", "price": price, "group": group})

    def buy(self, symbol: BrokerSymbol,  amount: float = None, amountQuote: float = None,
            price=None, leverage=None, group=None):
        super().buy(symbol, amount, price=price, amountQuote=amountQuote, leverage=leverage, group=group)
        return self.getBrokerInterface().getCommand("buy", {"symbol": symbol, "amountQuote": amountQuote, "leverage": leverage, "amount": amount, "side": "BUY", "price": price, "group": group})

    def sell(self, symbol: BrokerSymbol, amount: float = None, amountQuote: float = None,
             price=None, leverage=None, group=None, type: OrderType = OrderType.MARKET):
        super().sell(symbol, amount, price=price, amountQuote=amountQuote, leverage=leverage, group=group, type=type)
        return self.getBrokerInterface().getCommand("sell", {"symbol": symbol,
                                                             "amountQuote": amountQuote,
                                                             "type": type,
                                                             "leverage": leverage, "amount": amount, "side": "SELL",
                                                             "price": price, "group": group})

    def short(self, symbol: BrokerSymbol, amount: float = None, amountQuote: float = None,
              type: OrderType = OrderType.MARKET,
              price=None, leverage=None, group=None):
        super().short(symbol, amount, price=price, amountQuote=amountQuote, leverage=leverage, group=group)
        return self.getBrokerInterface().getCommand("short", {"symbol": symbol, "type": type, "amountQuote": amountQuote, "leverage": leverage, "amount": amount, "side": "SHORT",  "price": price, "group": group})

    def long(self, symbol: BrokerSymbol,  amount: float = None, amountQuote: float = None,
             type: OrderType = OrderType.MARKET, price=None, leverage=None, group=None):
        super().long(symbol, amount, price=price, amountQuote=amountQuote, leverage=leverage, group=group)
        return self.getBrokerInterface().getCommand("long", {"symbol": symbol, "type": type, "amountQuote": amountQuote, "leverage": leverage, "amount": amount, "price": price, "group": group})

    def openOrders(self):
        return self.getBrokerInterface().getCommand("open_orders", {})

    def positions(self):
        return self.getBrokerInterface().getCommand("positions", {})

    def closeAllPositions(self, group=None):
        super().closeAllPositions()
        return self.getBrokerInterface().getCommand("close_all_positions", {"group": group})

    def closePosition(self, clientOrderId, price=None, type: OrderType = OrderType.MARKET, group=None):
        super().closePosition(clientOrderId, group=group)
        return self.getBrokerInterface().getCommand("close_position", {"clientOrderId": clientOrderId,
                                                                       "type": type,
                                                                       "price": price, "group": group})

    def profitFuture(self):
        return self.getBrokerInterface().getCommand("profitFuture", {})

    def profitSession(self):
        return self.getBrokerInterface().getCommand("profitSession", {})

    def profitGroup(self, group):
        return self.getBrokerInterface().getCommand("profitGroup", {"group": group})

    def session_profit(self):
        return self.getBrokerInterface().getCommand("session_profit", {})

    def complete_profit(self):
        return self.getBrokerInterface().getCommand("complete_profit", {})

    def complete_statistics(self):
        return self.getBrokerInterface().getCommand("complete_statistics", {})

    def session_statistics(self):
        return self.getBrokerInterface().getCommand("session_statistics", {})

    def time_in(self):
        info_data = self.getBrokerInterface().getCommand("time_in", {})
        if info_data is not None and "secondsIn" in info_data:
            return info_data["secondsIn"]
        return False

    def imIn(self):
        return self.getBrokerInterface().getCommand("im_in", {})

    def imOut(self):
        return not self.imIn()