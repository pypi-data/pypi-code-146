import datetime
import queue
import time

import pytz
from chipmunkdb.ChipmunkDb import ChipmunkDb

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import inspect
import pandas as pd
import asyncio
import simplejson as json

from coinlib import logger
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.helper import createTimerWithTimestamp
from coinlib.statistics.StatisticMethodJob import StatisticMethodJob

class SymbolWorker(WorkerJobProcess):


    def __init__(self, workerJob, factory):
        self.symbolWorkerConfig = None
        self.waitingQueue = None
        self.symbolWorkerProcessInfo = None
        self.symbolWorkerRegistrationInfo = None
        super(SymbolWorker, self).__init__(workerJob, factory)

    def initialize(self):
        self.registrar = Registrar()
        self.log = self.logger()
        self.symbolWorkerInterface = stats.SymbolBrokerWorkerStub(self.getChannel())
        if self.symbolWorkerConfig is None:
            symbolWorkerConfigGlobal = self.symbolWorkerInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
            if symbolWorkerConfigGlobal.HasField("infoConfig"):
                self.symbolWorkerConfig = symbolWorkerConfigGlobal.infoConfig
            if symbolWorkerConfigGlobal.HasField("consumeConfig"):
                self.symbolWorkerConfig = symbolWorkerConfigGlobal.consumeConfig
            if symbolWorkerConfigGlobal.HasField("historicalConfig"):
                self.symbolWorkerConfig = symbolWorkerConfigGlobal.historicalConfig
            if symbolWorkerConfigGlobal.HasField("consumeOrderbookConfig"):
                self.symbolWorkerConfig = symbolWorkerConfigGlobal.consumeOrderbookConfig

            self.symbolWorkerRegistrationInfo = self.registrar.symbolBrokerCallbacks["method_"+self.symbolWorkerConfig.symbolBrokerIdentifier]
            self.symbolWorkerProcessInfo = self.symbolWorkerRegistrationInfo["process"]
        pass

    def onErrorHappened(self, message):

        indicatorError = statsModel.SymbolBrokerError()
        indicatorError.error.message = str(message)
        indicatorError.worker.CopyFrom(self.workerJob)

        self.logger().error("Error in symbol broker - "+str(message))

        self.symbolWorkerInterface.OnSymbolBrokerErrorOccured(indicatorError, metadata=self.registrar.getAuthMetadata())

    def error(self, message):
        self.onErrorHappened(message)
        return False

    def setConfig(self, configuration):
        self.symbolWorkerConfig = configuration
        pass

    def runSymbolWorker(self):
        pass

    def getOptions(self):
        return json.loads(self.symbolWorkerConfig.options)

    def run(self):

        t = threading.Thread(target=self.runSymbolWorker, args=[], daemon=True)

        t.start()

        try:
           t.join()
        except Exception as e:
           self.onErrorHappened(str(e))
           pass

        return True

class SymbolBrokerTickerSymbolData:
    open = None
    close = None
    datetime : str = None # format: "%Y-%m-%dT%H:%M:%S.%fZ"
    high = None
    low = None
    volume = None
    trades = None
    timeframe = None
    symbol = None
    closeTime = None  # format: "%Y-%m-%dT%H:%M:%S.%fZ"
    symbol_id = None
    isFinal = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class ExchangeInfoRequest:
    options = {}

class HistoricalSymbolRequest:
    options = {}
    start = None
    end = None
    quoteAsset = None
    baseAsset = None
    symbol_id = None
    exchange_id = None
    timeframe = None
    contractType = None
    assetType = None

class OrderBookConsumer:
    options = {}
    quoteAsset = None
    baseAsset = None
    symbol_id = None
    exchange_id = None
    timeframe = None
    contractType = None
    assetType = None

class MarketDataConsumer:
    options = {}
    quoteAsset = None
    baseAsset = None
    symbol_id = None
    exchange_id = None
    timeframe = None
    contractType = None
    assetType = None

class SymbolWorkerFetchHistoricalData(SymbolWorker):

    def getRunnerProcess(self):
        return self.symbolWorkerProcessInfo["downloadHistorical"]

    def sendDataFrame(self, df: pd.DataFrame):
        """Saving the Dataframe.
           Keyword arguments:
                index: should be your "close" datetime
                open: Open price
                high:  High Price
                low: Low Price
                close: Close Price
                volume: Volumes
                (trades: Optional: Trades count)

        """
        domain = None
        if self.symbolWorkerConfig.chartData.chart_prefix is not None and self.symbolWorkerConfig.chartData.chart_prefix != "":
            domain = self.symbolWorkerConfig.chartData.chart_prefix

        if self.chipmunkDb is None:
            host = self.registrar.get_chipmunkdb_host(self.symbolWorkerConfig.chartData.chipmunkdbHost);
            self.chipmunkDb = ChipmunkDb(host)

        if self.symbolWorkerConfig.returnData:

            brokerSymbolData = statsModel.SymbolBrokerFetchData()
            brokerSymbolData.worker.CopyFrom(self.workerJob)

            list = df.to_records()
            for e in list:
                d = statsModel.SymbolBrokerMarketData()
                d.open = e[1]
                d.close = e[4]
                d.high = e[2]
                d.low = e[3]
                ts = pd.to_datetime(str(e[0]))
                d.closeTime = datetime.datetime.strftime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
                d.volume = e[5]
                brokerSymbolData.data.append(d)

            self.symbolWorkerInterface.onBrokerFetchSymbolDataReceived(brokerSymbolData, metadata=self.registrar.getAuthMetadata())

        else:

            df.rename(columns={'open': 'main:open', 'close': 'main:close', 'high': 'main:high', 'low': 'main:low', 'trades':'main:trades', 'volume':'main:volume'}, inplace=True)

            df = df.sort_index()
            self.chipmunkDb.save_as_pandas(df, self.symbolWorkerConfig.chartData.workspace_id, mode="dropbefore", domain=domain)

        return True

    def runSymbolWorker(self):
        try:
            process = self.getRunnerProcess()

            req = HistoricalSymbolRequest()
            req.options = self.getOptions()
            req.start = self.symbolWorkerConfig.start
            req.end = self.symbolWorkerConfig.end
            req.quoteAsset = self.symbolWorkerConfig.quoteAsset
            req.baseAsset = self.symbolWorkerConfig.baseAsset
            req.symbol_id = self.symbolWorkerConfig.client_symbol_id
            req.exchange_id = self.symbolWorkerConfig.exchange_id
            req.timeframe = self.symbolWorkerConfig.timeframe
            req.contractType = self.symbolWorkerConfig.contractType
            req.assetType = self.symbolWorkerConfig.assetType


            if (inspect.iscoroutinefunction(process)):
                async def runandwait():
                    try:
                        task = asyncio.ensure_future(process(req, self))
                        await task
                    except Exception as e2:
                        raise e2

                loop = asyncio.new_event_loop()
                ret = loop.run_until_complete(runandwait())
            else:
                ret = process(req, self)

        except Exception as e:

            self.onErrorHappened(str(e))

class SymbolWorkerConsumeMarketData(SymbolWorker):
    consumerStopped = False

    def getFetchCandleProcess(self):
        return self.symbolWorkerProcessInfo["fetchCandles"]

    def getRunnerProcess(self):
        return self.symbolWorkerProcessInfo["consumeLive"]

    def canceled(self):
        return self.consumerStopped

    def sendSymbolTicker(self, ticker: SymbolBrokerTickerSymbolData):

        d = statsModel.SymbolBrokerMarketData()
        d.worker.CopyFrom(self.workerJob)
        d.open = ticker.open
        d.close = ticker.close
        d.high = ticker.high
        d.low = ticker.low
        d.volume = ticker.volume
        d.trade = ticker.trades
        d.datetime = datetime.datetime.strftime(datetime.datetime.strptime(ticker.datetime, "%Y-%m-%dT%H:%M:%S.%f%Z")
                                               .replace(tzinfo=pytz.utc), "%Y-%m-%dT%H:%M:%S.%fZ")
        d.closeTime = datetime.datetime.strftime(datetime.datetime.strptime(ticker.closeTime, "%Y-%m-%dT%H:%M:%S.%f%Z")
                                               .replace(tzinfo=pytz.utc), "%Y-%m-%dT%H:%M:%S.%fZ")
        d.symbol = ticker.symbol
        d.isfinal = ticker.isFinal
        d.symbol_id = ticker.symbol_id

        self.symbolWorkerInterface.onMarketDataReceived(d, metadata=self.registrar.getAuthMetadata())

        return True

    # This method is used to "fetch" the live candle when the "timestamp"
    # in the current selected timeframe gets fired
    async def tickerTimeFrameTimer(self, c, timeframe, currentTickTime, params):
        reqData = params["reqData"]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        ticker = None
        for i in range(10):
            print("Fetching Current Timestamp for final " + reqData.symbol_id + " and " + str(reqData.timeframe))
            process = self.getFetchCandleProcess()
            allticker = await process(reqData, self, 2)
            current_ticker = allticker[-1]
            tickerTimestamp = datetime.datetime.strptime(current_ticker.closeTime, "%Y-%m-%dT%H:%M:%S.%f%Z")

            print("Search for ticktime: " + str(currentTickTime))
            print("Got a ticktime: " + str(tickerTimestamp))

            if tickerTimestamp.replace(second=0, microsecond=0, tzinfo=None) == \
                    currentTickTime.replace(second=0, microsecond=0, tzinfo=None):
                ticker = allticker[0]
                print("Found correct candle on second clear... " + str(reqData.symbol_id) + " and " + str(
                    reqData.timeframe))
                break
            else:
                ## wait for a second until the ticker swaps
                print("Waiting one sec")
                await asyncio.sleep(2)
        loop.close()
        if ticker is not None:
            ticker.trades = -1
            # lets fake the close time and be sure it works
            ticker.timeframe = reqData.timeframe
            ticker.symbol_id = reqData.exchange_id + "_" + reqData.symbol_id
            ticker.symbol = reqData.symbol_id
            ticker.isFinal = True

            self.lastTimestamp = ticker

            self.sendSymbolTicker(ticker)
        else:
            self.log.error("Error we hav enot found a correct ticker for: " + str(reqData.symbol_id) + " and " + str(
                reqData.timeframe))

    def wait_for_stop_thread(self):

        s = statsModel.SymbolBrokerStopConsumerListener()
        s.worker.CopyFrom(self.workerJob)

        try:
            if (self.waitingQueue != None):
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()
            self.commandStream = self.symbolWorkerInterface.waitForCommands(iter(self.waitingQueue.get, None))
            self.waitingQueue.put(s)
            for d in self.commandStream:
                if d.stopped:
                    self.consumerStopped = True
        except Exception as e:
            self.logger().info(str(e))
            self.consumerStopped = True

    def run_process_in_thread(self, process, req):
        t = threading.Thread(target=self.wait_for_stop_thread, args=())
        t.start()
        errorMessage = None

        print("Consuming for: ["+self.symbolWorkerConfig.exchange_id+"]  " + req.symbol_id + "@" + req.timeframe)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            timer = createTimerWithTimestamp(self.tickerTimeFrameTimer, req.timeframe, self, {"reqData": req})
        except Exception as e:
            pass
        try:
            loop.run_until_complete(process(req, self))
        except Exception as e:
            self.logger().error("This is a problem cause process crashes")
            errorMessage = str(e)
            pass
        if not self.canceled():
            self.logger().warn("We should not be here when its not canceled")
            d = statsModel.SymbolBrokerConsumerError()
            d.worker.CopyFrom(self.workerJob)
            d.errorMessage = errorMessage if errorMessage is not None else "The consumer exited unexpectedly"
            self.symbolWorkerInterface.onBrokerSymbolTickerCrashed(d, metadata=self.registrar.getAuthMetadata())
        loop.close()
        try:
            timer.cancel()
        except Exception as e:
            pass
        return True

    def runSymbolWorker(self):
        process = self.getRunnerProcess()

        req = MarketDataConsumer()
        req.options = self.getOptions()
        req.quoteAsset = self.symbolWorkerConfig.quoteAsset
        req.baseAsset = self.symbolWorkerConfig.baseAsset
        req.symbol_id = self.symbolWorkerConfig.client_symbol_id
        req.exchange_id = self.symbolWorkerConfig.exchange_id
        req.timeframe = self.symbolWorkerConfig.timeframe
        req.exchange_id = self.symbolWorkerConfig.exchange_id
        req.contractType = self.symbolWorkerConfig.contractType
        req.assetType = self.symbolWorkerConfig.assetType

        t = threading.Thread(target=self.run_process_in_thread, args=(process, req))
        t.start()

        pass

class SymbolWorkerBrokerInfo(SymbolWorker):

    def saveBrokerInfo(self, exchanges, symbols):
        brokerSymbolInfo = statsModel.SymbolBrokerInfo()
        for e in exchanges:
            brokerSymbolInfo.exchanges.append(e)

        for s in symbols:
            brokerSymbolInfo.symbols.append(s)
        brokerSymbolInfo.worker.CopyFrom(self.workerJob)
        return self.symbolWorkerInterface.onBrokerSymbolInfoReceived(brokerSymbolInfo, metadata=self.registrar.getAuthMetadata())

    def getRunnerProcess(self):
        return self.symbolWorkerProcessInfo["brokerInfoProcess"]

    def runSymbolWorker(self):
        process = self.getRunnerProcess()

        try:

            req = ExchangeInfoRequest()
            req.options = self.getOptions()

            if (inspect.iscoroutinefunction(process)):
                async def runandwait():
                    try:
                        task = asyncio.ensure_future(process(req, self))
                        result = await task
                    except Exception as e2:
                        raise e2

                loop = asyncio.new_event_loop()
                ret = loop.run_until_complete(runandwait())
            else:
                ret = process(req, self)


        except Exception as e:
            self.onErrorHappened(str(e))

