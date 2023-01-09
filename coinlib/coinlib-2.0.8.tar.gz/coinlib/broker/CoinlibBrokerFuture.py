from abc import ABC ,abstractmethod

from coinlib.broker.BrokerDTO import OpenOrderInfo, PositionList, Position, PositionOrderInfo, TakeProfitStopLoss, \
   OrderSide, LeverageInfo, LeverageUpdateInfo
from coinlib.broker.CoinlibBroker import CoinlibBroker


class CoinlibBrokerFuture(CoinlibBroker):

   @abstractmethod
   async def get_positions(self) -> PositionList:
      pass

   @abstractmethod
   async def create_order_stop_limit(self, asset: str, amount: float, limit_price: float, stop_price: float,
                               leverage: float = 1, clientOrderId: str = None) -> OpenOrderInfo:
      pass

   @abstractmethod
   async def create_order_trailing_stop(self, asset: str, amount: float, activation_price: float, callback_rate: float = 0.01,
                                  leverage: float = 1, clientOrderId: str = None) -> OpenOrderInfo:
      pass

   @abstractmethod
   async def create_order_market(self, asset: str, amount: float, side: OrderSide = OrderSide.buy,
                           take_profit_stop_los: TakeProfitStopLoss = None,
                           leverage: float = 1, clientOrderId: str = None) -> OpenOrderInfo:
      pass

   @abstractmethod
   async def create_order_limit(self, asset: str, amount: float, limit_price: float,
                          side: OrderSide = OrderSide.buy, take_profit_stop_los: TakeProfitStopLoss = None,
                          leverage: float = 1, clientOrderId: str = None) -> OpenOrderInfo:
      pass

   @abstractmethod
   async def close_position_market(self, asset:str, position_order_id: str, amount: float, side: str, clientOrderId=None) -> PositionOrderInfo:
      pass

   @abstractmethod
   async def close_position_limit(self, asset: str, position_order_id: str,  amount: float, limit_price: float,
                                 side: OrderSide = OrderSide.buy, take_profit_stop_los: TakeProfitStopLoss = None,
                                 clientOrderId: str = None) -> PositionOrderInfo:
      pass

   @abstractmethod
   async def set_leverage(self, symbol: str, leverage: float) -> LeverageUpdateInfo:
      pass