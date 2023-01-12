"""
General constant enums used in the trading platform.
"""

from enum import Enum
from dataclasses import dataclass

class SymbolType():
    Options="OPT"
    Futures="FUT"
    Stocks="STK"

class BarType():
    MINUTE = 4
    DK = 5
    TICK = 2
class GreeksType():
    DOGSS=800
    DOGSK=820
    GREEKS1K=9
    GREEKSTICK=10
    GREEKSDK=19

class OrderSide():
    Buy=1
    Sell=2
    
class TimeInForce():
    ROD=1
    IOC=2
    FAK=2
    FOK=3
class OrderType():
    Market=1
    Limit=2
    Stop=3
    Stoplimit=4
    TrailingStop=5
    TrailingStopLimit=6
    MarketifTouched=7
    LimitifTouched=8
    TrailingLimit=9
    # 对方价=10
    # 本方价=11
    # 中间价=15

    # 最优价=20
    # 最优价转限价=21
    # 五档市价=22
    # 五档市价转限价=23
    # 市价转限价=24
    # 一定范围市价=25

class PositionEffect():
    Open=0
    Close=1
    平今=2
    平昨=3
    Auto=4
    备兑开仓=10
    备兑平仓=11

@dataclass
class OrderStruct:
    Account:str
    BrokerID:str
    Symbol:str
    Side:OrderSide
    OrderQty:int
    OrderType:OrderType
    TimeInForce:TimeInForce
    PositionEffect:PositionEffect
    SymbolA:str=""
    SymbolB:str=""
    Price:float=0
    StopPrice:float=0
    Side1:int=0
    Side2:int=0
    ContingentSymbol:str=""
    TrailingAmount:int=0
    TrailingField:int=0
    TrailingType:int=0
    TouchCondition:int=0
    TouchField:int=0
    TouchPrice:str=""
    Synthetic:int=0
    GroupID:str=""
    GroupType:int=0
    GrpAcctOrdType:int=0
    ChasePrice:str=""
    Strategy:str=""
    UserKey1:str=""
    UserKey2:str=""
    UserKey3:str=""
    SlicedPriceField:int=0
    SlicedTicks:int=0
    SlicedType:int=0
    DiscloseQty:int=0
    Variance:int=0
    Interval:int=0
    LeftoverAction:int=0
    SelfTradePrevention:int=0
    ExtCommands:str=""
    ExCode:str=""
    Exchange:str=""
    TradeType:int=0
