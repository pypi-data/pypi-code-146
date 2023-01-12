from abc import abstractmethod

from coinlib.broker.BrokerDTO import OpenOrderInfo, OrderSide
from coinlib.broker.CoinlibBrokerFuture import CoinlibBroker


class CoinlibBrokerSpot(CoinlibBroker):

    @abstractmethod
    async def create_order_stop_limit(self, asset: str, amount: float, limit_price: float, stop_price: float,
                                      side: OrderSide = OrderSide.buy, clientOrderId: str = None) -> OpenOrderInfo:
        pass

    @abstractmethod
    async def create_order_oco(self, asset: str, amount: float, price: float, stop_price: float, limit_price: float,
                               side: OrderSide = OrderSide.buy, clientOrderId: str = None) -> OpenOrderInfo:
        pass

    @abstractmethod
    async def create_order_market(self, asset: str, amount: float,
                                  side: OrderSide = OrderSide.buy, clientOrderId: str = None) -> OpenOrderInfo:
        pass

    @abstractmethod
    async def create_order_limit(self, asset: str, amount: float, limit_price: float,
                                 side: OrderSide = OrderSide.buy, clientOrderId: str = None) -> OpenOrderInfo:
        pass