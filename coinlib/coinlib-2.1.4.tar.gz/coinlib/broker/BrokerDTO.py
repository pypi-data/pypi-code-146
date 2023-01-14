from dataclasses import dataclass
from enum import Enum
from typing import Mapping, MutableMapping, Sequence, Iterable, List, Set, TypedDict

from coinlib.helper import Serializable


class BrokerLoginMode(Enum):
    API_KEY = 0

class BrokerContractType(Enum):
    SPOT = 0
    FUTURE = 1
    MARGIN = 2
    OPTION = 3
    INDEX = 4
    CREDIT = 5

class BrokerAssetType(Enum):
    COIN = 0
    FOREX = 1
    STOCK = 2

class BrokerExchangeEntry(TypedDict):
    key: str
    name: str
    icon: str
    description: str
    supportDemo: bool
    supportLive: bool
    loginMode: BrokerLoginMode
    assetTypes: List[BrokerAssetType]
    contractTypes: List[BrokerContractType]



class BrokerEvent(Enum):
    OrderUpdate = "ORDER_UPDATE"
    MarginCall = "MARGIN_CALL"
    SymbolTicker = "SYMBOL_TICKER"

class OrderSide(Enum):
    buy = "buy"
    sell = "sell"

class LeverageInfo(Serializable):
    can_leverage: bool

class OpenOrders(Serializable):
    pass

class Orders(Serializable):
    pass

class ClosedOrders(Serializable):
    pass

class Asset(Serializable):
    def __init__(self):
        self.name: str = ""
        self.free: float = 0
        self.total: float = 0
        self.used: float = 0
    pass

class AssetWithPrice(Asset):
    def __init__(self):
        super().__init__()
        self.price = 0

class Balance(Serializable):
    def __init__(self):
        self.assets: List[AssetWithPrice] = []

    def addAsset(self, assetName: str, free: float, used: float, total: float, price: float):
        asset = Asset()
        asset.name = assetName
        asset.free = free
        asset.price = price
        asset.used = used
        asset.total = total
        self.assets.append(asset)

class OrderTypes(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LIMIT = "STOP_LIMIT"
    OCO = "OCO"
    STOP_LOSS = "STOP_LOSS"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TRAILING_STOP = "TRAILING_STOP"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    STOP_MARKET = "STOP_MARKET"
    STOP = "STOP"

class SelectedSymbolInfo(Serializable):
    leverageMax: int
    canLeverage: bool
    currentLeverage: int


class BrokerDetailedInfo(Serializable):
    canLeverage: bool
    leverageMax: int
    contractType: BrokerContractType
    orderTypes: List[OrderTypes]
    makerFee: float
    takerFee: float

class BrokerSymbol(Serializable):

    def __init__(self, symbol=None):
        if symbol is not None:
            self.symbol = symbol
            if "/" in symbol:
                self.base = symbol.split("/")[0]
                self.quote = symbol.split("/")[1]
            if "-" in symbol:
                self.base = symbol.split("-")[0]
                self.quote = symbol.split("-")[1]

    symbol: str
    quote: str
    base: str
    client_id: str
    price_precision: int
    size_precision: int



class CancelOrder(Serializable):
    pass

class Position(Serializable):
    pass

class BrokerTickerData(Serializable):
    open: float
    high: float
    low: float
    close: float
    volume: float
    date: str
    symbol_id: str

class TakeProfitStopLoss(Serializable):
    take_profit: float
    stop_loss: float
    pass

class Position(Serializable):
    entryPrice: float
    amount: float
    orderId: str
    symbol: BrokerSymbol

class PositionList(Serializable):
    positions: List[Position]

class PositionOrderInfo(Serializable):
    pass

class LeverageUpdateInfo(Serializable):
    setLeverage: int

class OrderCancelInfo(Serializable):
    orderId: str
    clientOrderId: str
    symbol_id: str

class Order(Serializable):
    orderId: str
    clientOrderId: str
    status: str

class OrderUpdateInformation(Order):
    price: float
    fee: float
    cost: float
    timestamp: str
    averagePrice: float
    remaining: float
    filled: float
    tradesCnt: int


class OpenOrderInfo(Order):
    pass

class OrderInformation(Order):
    pass


class CoinlibBrokerLoginParams(Serializable):
    apiKey: str
    secret: str
    username: str
    password: str



class CoinlibBrokerAccount(Serializable):
    exchange_id: str
    sandbox: bool
    assetType: BrokerAssetType
    contractType: BrokerContractType
    loginInfo: CoinlibBrokerLoginParams

class AssetInfoSummary(Serializable):
    assets: List[Asset]