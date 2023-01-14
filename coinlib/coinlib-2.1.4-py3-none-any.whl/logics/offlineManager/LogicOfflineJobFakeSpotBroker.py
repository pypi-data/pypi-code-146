import pandas as pd

from coinlib.broker.BrokerDTO import BrokerSymbol
from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker, FakeOrder, OrderSide, \
    OrderType


class LogicOfflineJobFakeSpotBroker(LogicOfflineJobFakeBroker):

    def __init__(self, manager):
        super(LogicOfflineJobFakeSpotBroker, self).__init__(manager)
        pass

    def long(self, symbol: BrokerSymbol = None,
                price=None, leverage=None, group=None):
        raise NotImplementedError("LONG: This is not available in Spot Broker")

    def short(self, symbol: BrokerSymbol = None,
                 price=None, leverage=None, group=None):
        raise NotImplementedError("SHORT: This is not available in Spot Broker")

    def longAll(self, symbol: BrokerSymbol=None,
             price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        raise NotImplementedError("LONGALL: This is not available in Spot Broker")


    def shortAll(self, symbol: BrokerSymbol=None,
             price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        raise NotImplementedError("SHORTALL: This is not available in Spot Broker")

    def exchangeOrderAndRemoveAssetValue(self, order: FakeOrder):

        #asset = self.manager.getAsset(order.symbol.base)
        #if asset is None:
        #    ## this is an error
        #    self.onErrorHappenedInBroker("You tried to sell a asset which you dont have. ", order)
        #asset.free -= order.quantity
        #asset.total -= order.quantity
        portfolio = self.manager.getPortfolio()
        outprice = self.getPrice(symbol=order.symbol.symbol)
        if order.orderType == OrderType.LIMIT:
            fee = order.quantity * (self.manager.getOptions().makerFee/100)
        else:
            fee = order.quantity * (self.manager.getOptions().takerFee / 100)
        self._fees = self._fees + (fee*outprice)

        quantity_without_fee = order.quantity - fee

        portfolio.getQuoteAsset().free += quantity_without_fee * outprice
        portfolio.getQuoteAsset().total += quantity_without_fee * outprice

        self.manager.updatePortfolio(portfolio)

        return True

    def exchangeOrderAndAddAssetValue(self, order: FakeOrder):
        asset = self.manager.getAsset(order.symbol.base, createIfNotExistant=True)
        if order.orderType == OrderType.LIMIT:
            fee = order.quantity * (self.manager.getOptions().makerFee/100)
        else:
            fee = order.quantity * (self.manager.getOptions().takerFee / 100)
        self._fees = self._fees + (fee*order.executed_price)
        asset.free += order.quantity - fee
        asset.total += order.quantity - fee
        if asset.locked > 0:
            asset.locked -= order.quantity

        portfolio = self.manager.getPortfolio()

        #portfolio.getQuoteAsset().free -= order.quantity * order.executed_price
        #portfolio.getQuoteAsset().total -= order.quantity * order.executed_price

        self.manager.updatePortfolio(portfolio)

        return True

    def onHandleExecutedOrder(self, order: FakeOrder):

        if order.side == OrderSide.SELL:
            self.exchangeOrderAndRemoveAssetValue(order)
        else:
            self.exchangeOrderAndAddAssetValue(order)

