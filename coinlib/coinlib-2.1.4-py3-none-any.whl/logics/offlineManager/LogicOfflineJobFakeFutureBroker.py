import datetime
import random
import string
from enum import Enum
import pandas as pd
from typing import List

from coinlib.broker.BrokerDTO import BrokerSymbol, Position
from coinlib.logics.manager.PortfolioModel import CurrentMoneyInfo
from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker, FakeOrder, OrderSide, \
    OrderType


class FakeOpenPosition(Position):
    order: FakeOrder

class LogicOfflineJobFakeFutureBroker(LogicOfflineJobFakeBroker):

    _openPositions: List[FakeOpenPosition] = []

    def __init__(self, manager):
        super(LogicOfflineJobFakeFutureBroker, self).__init__(manager)
        self._openPositions = []
        pass

    def closePosition(self, clientOrderId, price: float = None, group=None):
        for pos in self._openPositions:
            if pos.orderId == clientOrderId:
                otherSide = OrderSide.BUY
                if pos.order.side == OrderSide.BUY or pos.order.side == OrderSide.LONG:
                    otherSide = OrderSide.SELL
                else:
                    otherSide = OrderSide.BUY
                type = OrderType.MARKET
                if price is not None:
                    type = OrderType.LIMIT
                super().closePosition(clientOrderId, price=price, amount=pos.amount, symbol=pos.order.symbol, group=group)
                self.createOrder(otherSide, pos.order.symbol, pos.amount, type=type, reduceOnly=True, price=price, clientOrderId=pos.orderId, group=group)
        return False

    def short(self, symbol: BrokerSymbol=None, amount: float = None, amountQuote=None,
             price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().short(symbol, amount=amount, amountQuote=amountQuote, price=price, leverage=leverage, group=group)

        if price is not None:
            return self.createOrder(OrderSide.SHORT, symbol, quantity=amount,
                                    leverage=leverage, type=OrderType.LIMIT, price=price)

        return self.createOrder(OrderSide.SHORT, symbol, quantity=amount,
                                leverage=leverage, type=OrderType.MARKET)

    def long(self, symbol: BrokerSymbol=None, amount: float = None, amountQuote=None,
             price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().long(symbol, amount=amount, amountQuote=amountQuote, price=price,
                     leverage=leverage, group=group)


        if price is not None:
            return self.createOrder(OrderSide.LONG, symbol, quantity=amount,
                                    leverage=leverage, type=OrderType.LIMIT, price=price)

        return self.createOrder(OrderSide.LONG, symbol, quantity=amount,
                                leverage=leverage, type=OrderType.MARKET)
    def unlockQuoteMoney(self, order: FakeOrder):

        if order.reduceOnly:
            # its a close position order
            positionMoney = self.getAllPositionsSummaryForSymbol(order.symbol)
            if order.quantity < positionMoney:
                return False

            return True
        else:
            return super().unlockQuoteMoney(order)

    def lockQuoteMoney(self, order: FakeOrder):

        portfolio = self.manager.getPortfolio()
        if order.reduceOnly:
            # its a close position order
            positionMoney = self.getAllPositionsSummaryForSymbol(order.symbol)
            if order.quantity < positionMoney:
                return False

            return True
        else:
            return super().lockQuoteMoney(order)
    def isOpenOrderForPosition(self, order):
        for position in self._openPositions:
            if position.symbol.base == order.symbol.base:
                return True

        return False


    def imIn(self):
        if len(self._openPositions) > 0:
            foundOpenPositions = len(self._openPositions)
            for order in self._openOrders:
                if self.isOpenOrderForPosition(order):
                    foundOpenPositions = foundOpenPositions - 1
            if foundOpenPositions > 0:
                return True
            else:
                return False

        return False

    def shortAll(self, symbol: BrokerSymbol=None,
             price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)

        asset = self.manager.getAsset(symbol.quote)
        quoteMoney = asset.free * 0.99  ## we remove 1% cause of slippage

        if maximumQuote is not None and quoteMoney > maximumQuote:
            quoteMoney = maximumQuote

        if quoteMoney <= 1:
            raise Exception("Not more than 1 in your portfolio.")

        if price is None:
            current_price = self.getPrice(symbol.symbol)
        else:
            current_price = price

        if current_price is None:
            raise Exception("Price for your symbol can not be found")

        quantity = quoteMoney / current_price
        if maximum is not None and quantity > maximum:
            quantity = maximum

        super().shortAll(symbol, price=price, leverage=leverage, group=group)

        return self.short(symbol, amount=quantity, group=group, price=price, leverage=leverage)


    def longAll(self, symbol: BrokerSymbol=None, price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)

        asset = self.manager.getAsset(symbol.quote)
        quoteMoney = asset.free * 0.99  ## we remove 1% cause of slippage

        if maximumQuote is not None and quoteMoney > maximumQuote:
            quoteMoney = maximumQuote

        if quoteMoney <= 1:
            raise Exception("Not more than 1 in your portfolio.")

        if price is None:
            current_price = self.getPrice(symbol.symbol)
        else:
            current_price = price

        if current_price is None:
            raise Exception("Price for your symbol can not be found")

        quantity = quoteMoney / current_price
        if maximum is not None and quantity > maximum:
            quantity = maximum

        super().longAll(symbol, price=price, leverage=leverage, group=group)

        return self.long(symbol, amount=quantity, group=group, price=price, leverage=leverage)

    def getAllPositionsSummaryForSymbol(self, symbol):
        sumary = 0

        for pos in self._openPositions:
            if pos.symbol.base == symbol.base:
                sumary += pos.amount

        return sumary

    def checkIfOrderIsAllowedInCaseOfMoney(self, order: FakeOrder):
        if order.reduceOnly:
            # its a close position order
            positionMoney = self.getAllPositionsSummaryForSymbol(order.symbol)
            if order.quantity < positionMoney:
                return False
        else:
            quoteMoneyAvailable = self.manager.getFreePortfolioQuoteMoney()
            targetMoney = order.quantity * order.order_price
            if targetMoney > quoteMoneyAvailable:
                return False

        return True

    def closeAllPositions(self, price=None, group=None):
        super().closeAllPositions(group=group)
        for pos in self._openPositions:
            self.closePosition(pos.orderId, price=price, group=group)
        return False

    def positions(self):
        return self._openPositions

    def getCurrentMoneyInMarket(self):
        currentMoney = CurrentMoneyInfo()

        for pos in self._openPositions:
            price = self.getPrice(symbol=pos.symbol.symbol)
            total = pos.amount * price
            currentMoney.summary = currentMoney.summary + total

        return currentMoney

    def recalculateCurrentPortfolioByAssets(self, updatePortfolio=True):
        portfolio = super().recalculateCurrentPortfolioByAssets(updatePortfolio=False)

        for pos in self._openPositions:
            price = self.getPrice(symbol=pos.symbol.symbol)
            total = pos.amount * price
            portfolio.currentMoney.summary = portfolio.currentMoney.summary + total

        self.manager.updatePortfolio(portfolio)

        return portfolio

    def exchangePositionToPortfolio(self, order, position: FakeOpenPosition):
        portfolio = self.manager.getPortfolio()

        outprice = self.getPrice(symbol=position.symbol.symbol)

        if order.orderType == OrderType.LIMIT:
            fee = position.amount * (self.manager.getOptions().makerFee/100)
        else:
            fee = position.amount * (self.manager.getOptions().takerFee / 100)
        self._fees = self._fees + (fee * outprice)

        quantity_without_fee = order.quantity - fee

        if position.order.side == OrderSide.LONG:
            price_change = (outprice / position.entryPrice)
        else:
            price_change = (position.entryPrice / outprice)


        original_money = (quantity_without_fee * position.entryPrice)

        new_money = original_money * price_change


        portfolio.getQuoteAsset().free += new_money
        portfolio.getQuoteAsset().total += new_money

        portfolio = self.recalculateCurrentPortfolioByAssets(updatePortfolio=True)

        return True

    def exchangeOrderToPosition(self, order):
        portfolio = self.manager.getPortfolio()

        if order.orderType == OrderType.LIMIT:
            fee = order.quantity * (self.manager.getOptions().makerFee/100)
        else:
            fee = order.quantity * (self.manager.getOptions().takerFee / 100)
        self._fees = self._fees + (fee * order.executed_price)

        quantity_without_fee = order.quantity - fee

        position = FakeOpenPosition()
        position.entryPrice = order.executed_price
        position.symbol = order.symbol
        position.amount = quantity_without_fee
        position.order = order
        position.orderId = order.orderId

        #portfolio.getQuoteAsset().free -= position.amount * position.entryPrice
        #portfolio.getQuoteAsset().total -= position.amount * position.entryPrice

        portfolio = self.recalculateCurrentPortfolioByAssets(updatePortfolio=True)

        return position

    def onHandleExecutedOrder(self, order: FakeOrder):

        if order.reduceOnly:
            for pos in self._openPositions:
                if pos.orderId == order.orderId:
                    self._openPositions.remove(pos)
                    self.exchangePositionToPortfolio(order, pos)
        else:
            position = self.exchangeOrderToPosition(order)
            self._openPositions.append(position)
