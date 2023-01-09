import asyncio
import datetime
import threading
import time
from typing import List

from coinlib import helper
from coinlib.BasicJobSessionStorage import BasicJobSessionStorage
from coinlib.broker.BrokerDTO import BrokerSymbol
from coinlib.data.DataTable import DataTable
from coinlib.feature.FeatureDTO import RabbitInfo
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import pandas as pd

import aio_pika
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from coinlib.logics.LogicOptions import LogicOptions
from coinlib.logics.manager.PortfolioModel import PortfolioModel, PriceInterface, CurrentMoneyInfo, AssetInfo


class LogicCommandPortfolioDTO:
    assets: List[AssetInfo]
    currentCalculatedMoney: CurrentMoneyInfo

class LogicCommandParams:
    traderName: str
    portfolio: LogicCommandPortfolioDTO

class LogicManager(BasicJobSessionStorage):
    logicConfig: statsModel.LogicRunnerLogic
    brokerAccount: statsModel.BrokerAccountModel
    _portfolio: PortfolioModel
    _params: LogicCommandParams

    def __init__(self, name, logicConfig: statsModel.LogicRunnerLogic,
                 brokerAccount: statsModel.BrokerAccountModel=statsModel.BrokerAccountModel(),
                 portfolio: PortfolioModel = None, infoStorage = None, options: LogicOptions = None,
                 advancedInfo = None):
        super(LogicManager, self).__init__(infoStorage)
        self.table: DataTable = DataTable()
        self.broker = None
        self.logicOptions = options
        self._lastTimeLogQueueWasRunning = 0
        self._logList = []
        self._sendLogQueueRunning = False
        self.rabbit_info = RabbitInfo()
        self.loop = asyncio.new_event_loop()
        self.appWorkerId = logicConfig.app_worker_id
        self.appWorkerRunnerId = logicConfig.app_worker_runner_id
        self.advancedInfo = advancedInfo
        if portfolio is None:
            portfolio = PortfolioModel()
        self._portfolio = portfolio
        self.brokerAccount = brokerAccount
        self.name = name
        self.logicConfig = logicConfig

        pass

    def getOptions(self):
        return self.logicOptions

    def send_worker_data_to_queue_sync(self, force=False):
        newLoop = asyncio.new_event_loop()
        timeDistanceInSeconds = time.time() - self._lastTimeLogQueueWasRunning
        if force or (not self._sendLogQueueRunning and timeDistanceInSeconds > 5):
            self._lastTimeLogQueueWasRunning = time.time()

            newLoop.run_until_complete(self.send_worker_data_to_queue(loop=newLoop))

        return True

    async def send_worker_data_to_queue(self, loop=None):
        self._sendLogQueueRunning = True
        if loop is None:
            loop = self.loop
        message_log_queue = self._logList.copy()
        self._logList.clear()
        try:
            connection = await aio_pika.connect_robust(
                "amqp://" + self.rabbit_info.user + ":" + self.rabbit_info.pwd + "@" + self.rabbit_info.ip + ":" + self.rabbit_info.port + "/",
                loop=loop
            )

            async with connection:
                # Creating channel
                channel = await connection.channel()

                queue = await channel.declare_queue(
                    "save_logic_log_data",
                    durable=True
                )

                message_body = json.dumps({"data_logs": message_log_queue, "activityId": self.getAppWorkerActivityIdentifier(),
                                           "createdAt": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%fZ"),
                                           "applicationId": self.getAppWorkerIdentifier()},
                                            default=helper.serializeDTO)

                message = Message(
                    str.encode(message_body),
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                # Sending the message
                await channel.default_exchange.publish(
                    message, routing_key="save_logic_log_data"
                )

                await connection.close()

        except Exception as e:
            print(e)
            pass

            self._sendLogQueueRunning = False

    def onLogicStepFinished(self):
        try:
            ## send the last log outputs
            if len(self._logList) > 0:
                self.send_worker_data_to_queue_sync(True)
        except Exception as e:
                pass
        pass

    def runNextLogQueue(self):

        threading.Thread(target=self.send_worker_data_to_queue_sync, args=[], daemon=True).start()

        return True

    def log(self, data: str):

        self._logList.append(data)
        self.runNextLogQueue()

        return True

    def getAppWorkerIdentifier(self):
        return self.appWorkerId

    def getAppWorkerActivityIdentifier(self):
        return self.appWorkerRunnerId

    def setLogicParams(self, params: LogicCommandParams):
        self._params = params
        return True

    def updatePortfolio(self, newPortfolio: PortfolioModel):
        #print("update portfolio with: "+str(self._portfolio.currentMoney.summary))
        self._portfolio = newPortfolio

    def getSymbolForChart(self, chartId=None):

        l = []

        di = self.advancedInfo
        assetmap = di["chartToAssetMap"]

        if chartId is None:
            for chart_key in assetmap.keys():
                chart = assetmap[chart_key]
                symbol = BrokerSymbol(chart["symbol"]["symbol"])
                l.append(symbol)
        else:
            if chartId in assetmap:
                cc = assetmap[chartId]
                symbol = BrokerSymbol(cc["symbol"]["symbol"])
                return symbol

        if len(l) > 0:
            return l[0]
        return l

    def getChartInfo(self):
        return self.advancedInfo["chartToAssetMap"]

    def getAssets(self):
        return self._portfolio.assets

    def getAsset(self, assetName: str, createIfNotExistant: bool = False) -> statsModel.BrokerPortfolioAsset:
        for a in self._portfolio.assets:
            try:
                if a.name.lower() == assetName.lower():
                    return a
            except Exception as e:
                pass
            try:
                if a.base.lower() == assetName.lower():
                    return a
            except Exception as e:
                pass

        if createIfNotExistant:
            asset = AssetInfo()
            asset.name = assetName
            asset.free = 0
            asset.total = 0
            asset.locked = 0
            asset.date = self.getNow()
            self._portfolio.assets.append(asset)
            return self.getAsset(assetName, createIfNotExistant=False)

        return None

    def getNow(self):
        dt = self.table.getLast("datetime")
        date = datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date

    def getMoney(self, assetName: str) -> float:
        a = self.getAsset(assetName)
        if a is not None:
            return a.available
        return None

    def updateCurrentIndexToLast(self):
        self.setCurrentIndex(self.table.index[-1], True)

    def getTable(self):
        return self.table

    def setTable(self, table):
        self.table = table

    def getName(self):
        return self.name

    def getBroker(self):
        return self.broker

    def setBroker(self, broker):
        self.broker = broker

    def isFuture(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.FUTURE

    def isSpot(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.SPOT

    def isOption(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.OPTION

    def isMargin(self):
        return self.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.MARGIN

    def isBacktrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.BACKTRADER

    def isPapertrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.PAPER

    def isLivetrader(self):
        return self.brokerAccount.mode == self.logicConfig.brokerAccount.BrokerMode.LIVE

    def savePortfolio(self):
        self.saveInfo("account", "portfolio", self._portfolio.currentMoney.summary)
        return True

    def getPortfolio(self) -> PortfolioModel:
        return self._portfolio

    def getFreePortfolioQuoteMoney(self):
        return self._portfolio.currentMoney.free

    def getPortfolioQuoteMoney(self):
        return self._portfolio.currentMoney.summary
