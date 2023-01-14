from datetime import datetime
from typing import List
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from abc import ABC, abstractmethod

class PriceInterface(ABC):

    @abstractmethod
    def getPrice(self, symbol=None, base: str = None, quote: str = None) -> float:
        raise NotImplemented()

class AssetInfo:
    name: str
    total: float
    free: float
    locked: float
    lastPrice: float
    date: datetime.date

class CurrentMoneyInfo:
    summary: float
    free: float
    locked: float
    date: datetime.date

    def __init__(self):
        self.summary = 0
        self.free = 0
        self.locked = 0


class PortfolioModel:

    def __init__(self):
        self.currentMoney = CurrentMoneyInfo()
        self.currentMoney.free = 0
        self.currentMoney.locked = 0
        self.currentMoney.name = "USDT"
        self.assets = []

    currentMoney: CurrentMoneyInfo
    assets: List[AssetInfo]

    def unlockQuoteMoney(self, base: str, quote: str, quantity: float,
                         executed_price: float = None):

        quanittyPrice = quantity
        if executed_price is not None:
            quanittyPrice = executed_price * quantity
        for asset in self.assets:
            if asset.name == quote:
                asset.locked -= quanittyPrice
                asset.total = asset.locked + asset.free

        return

    def getQuoteAsset(self):
        for asset in self.assets:
            if asset.name == self.currentMoney.name:
                return asset

        return None

    def lockQuoteMoney(self, base: str, quote: str, quantity: float, executed_price: float= None):

        targetQuantity = quantity
        if executed_price is not None:
            targetQuantity = executed_price * quantity
        for asset in self.assets:

            if asset.name == quote:
                if asset.free >= targetQuantity:
                    asset.locked += targetQuantity
                    asset.free -= targetQuantity
                else:
                    raise Exception("You have not enough money in your portfolio")

        return

    def exchangeQuoteToAsset(self, assetName: str, quantity: float, price: float):
        """This method exchanges an qupte to a asset in quantity"""



        return False

    def exchangeAssetToQuote(self, assetName: str, quantity: float, price: float):
        """This method exchanges an asset to a quantity"""

        return False

    def hasEnoughAsset(self, asset, quantity):
        return False

    def hasEnoughQuoteMoney(self, quantity):
        return False

    @staticmethod
    def from_stats_model(p: statsModel.PortfolioModel):
        pm = PortfolioModel()
        for asset in p.assets:
            ass = AssetInfo()
            ass.name = asset.name
            ass.total = asset.value
            ass.free = asset.free
            ass.locked = asset.locked
            ass.date = asset.date
            pm.assets.append(ass)

        pm.currentMoney = CurrentMoneyInfo()
        pm.currentMoney.name = p.currentCalculatedBaseMoney.name
        pm.currentMoney.free = p.currentCalculatedBaseMoney.free
        pm.currentMoney.summary = p.currentCalculatedBaseMoney.total
        pm.currentMoney.date = p.currentCalculatedBaseMoney.date
        pm.currentMoney.locked = p.currentCalculatedBaseMoney.locked

        return pm

    @staticmethod
    def from_live_logics_model(p: statsModel.PortfolioModel):
        pm = PortfolioModel()
        for asset in p.assets:
            ass = AssetInfo()
            ass.name = asset.name
            if "value" in asset:
                ass.total = asset.value
            if "total" in asset:
                ass.total = asset.total
            ass.free = asset.free
            ass.locked = asset.locked
            if "date" in asset:
                ass.date = asset.date
            pm.assets.append(ass)

        pm.currentMoney = CurrentMoneyInfo()
        if "name" in p.currentCalculatedBaseMoney:
            pm.currentMoney.name = p.currentCalculatedBaseMoney.name
        pm.currentMoney.free = p.currentCalculatedBaseMoney.free
        pm.currentMoney.summary = p.currentCalculatedBaseMoney.total
        pm.currentMoney.date = p.currentCalculatedBaseMoney.date
        pm.currentMoney.locked = p.currentCalculatedBaseMoney.locked

        return pm