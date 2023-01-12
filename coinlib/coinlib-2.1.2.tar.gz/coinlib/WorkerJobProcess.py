import asyncio
import inspect

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import time
import pandas as pd
import queue
import grpc
import simplejson as json
import traceback
import zlib
import binascii
import base64
from coinlib.Registrar import Registrar
from coinlib.InfluxDatabase import InfluxDatabase
from chipmunkdb.ChipmunkDb import ChipmunkDb


class Indicator:
    feature: str
    original: any
    subfeature: str
    name: str

class WorkerJobProcess:
    def __init__(self, workerJob, factory):
        if factory is not None:
            self.workerChannel = factory.createChannel()
        self.registrar = Registrar()
        self.chipmunkDb = None
        ##self.chipmunkDb = ChipmunkDb(self.registrar.chipmunkdb)
        if factory is not None:
            self.stub = stats.DataWorkerStub(self.workerChannel)
        self.workerJob = workerJob

        self.stopped = True
        self.currentWorkerJobData = []
        self.factory = factory
        self.dataFrame = pd.DataFrame()
        return None

    def convertIndicatorDictToClass(self, key, func):
        ind = Indicator()
        ksplitted = key.split(".")
        ind.feature = ksplitted[0]
        ind.subfeature = ksplitted[1]
        ind.name = key
        inputs = base64.b64decode(func["inputs"]).decode("gbk")
        ind.inputs = json.loads(inputs, "utf8")
        ind.original = func
        return ind

    def getIndicators(self):
        indicators = []
        registeredFunctions = self.registrar.functionsCallbacks

        for key in registeredFunctions:
            func = registeredFunctions[key]
            ind = self.convertIndicatorDictToClass(key, func)

            indicators.append(ind)

        return indicators

    def getIndicatorMethodByName(self, group, featurename):
        try:
            indicator = Indicator()
            indicator.subfeature = featurename
            indicator.feature = group
            d = self.getIndicatorMethod(indicator)
            if d is not None:
                return self.convertIndicatorDictToClass(group+"."+featurename, d)
        except Exception as e:
            print("Can not find the indicator: "+group+"."+featurename+". You can see all indicators by c.functions()")
            return None

    def getIndicatorMethod(self, indicator):
        found_method = None
        registeredFunctions = self.registrar.functionsCallbacks

        if indicator.feature + "." + indicator.subfeature in registeredFunctions is not None:
            found_method = registeredFunctions[indicator.feature + "." + indicator.subfeature]

        return found_method

    def logger(self):
        return self.registrar.logger

    def fireEventCallback(self, method, routing_key, message):
        pass

    def onEventCallback(self, routing_key: str, message: object):
        block = None
        if routing_key in self.registrar.logicEventCallback:
            block = self.registrar.logicEventCallback[routing_key]
        if routing_key.replace("_dev", "") in self.registrar.logicEventCallback:
            block = self.registrar.logicEventCallback[routing_key.replace("_dev", "")]
        if block is not None:
            for cb in block["callbacks"]:
                self.fireEventCallback(cb, routing_key, message)
    
    def getStub(self) -> stats.DataWorkerStub:
        return self.stub

    def getDataServerForCollection(self, collectionName: str):
        r = statsModel.CollectionNodeRequest()
        r.collectionName = collectionName
        r.stage = self.registrar.environment
        r.worker.CopyFrom(self.workerJob)
        collectionNode = self.stub.GetNodeForCollection(r, metadata=self.registrar.getAuthMetadata())
        return collectionNode.name

    def closeChannel(self):
        self.workerChannel.close()

    def generateRawData(self, result_data):

        result_data_json = str(json.dumps(result_data, ignore_nan=True)).encode('utf8')
        result_data_json_compressed = zlib.compress(bytes(result_data_json))

        return result_data_json_compressed

    def getDataFrameColumn(self, key, column_name, _type="base"):
        try:
            if column_name+":open" in self.dataFrame.columns:
                dfCopy = self.dataFrame[[column_name+":open", column_name+":high",
                                        column_name+":low", column_name+":close", column_name+":volume"]].copy()
                dfCopy["open"] = dfCopy[column_name+":open"]
                dfCopy["high"] = dfCopy[column_name + ":high"]
                dfCopy["low"] = dfCopy[column_name + ":low"]
                dfCopy["close"] = dfCopy[column_name + ":close"]
                dfCopy["volume"] = dfCopy[column_name + ":volume"]

                #self.dataFrame[key + ":open"] = self.dataFrame[column_name + ":open"]
                #self.dataFrame[key + ":open"] = self.dataFrame[column_name + ":high"]
                #self.dataFrame[key + ":low"] = self.dataFrame[column_name + ":low"]
                #self.dataFrame[key + ":close"] = self.dataFrame[column_name + ":close"]
                #self.dataFrame[key + ":volume"] = self.dataFrame[column_name + ":volume"]

                return dfCopy
            elif column_name+":y" in self.dataFrame.columns:
                return self.dataFrame[column_name + ":y"].copy()
            elif column_name+":marker" in self.dataFrame.columns:
                return self.dataFrame[column_name + ":marker"].copy()

        except Exception as e:
            self.logger().error("Assert error")
            pass

        return self.dataFrame[column_name]

    def extractInputsFromDataFrameAndInsertInDataFrame(self, inputs):
        raw_inputs = {}
        for key in inputs:
            try:
                inputVal = inputs[key]
                type = inputVal["type"]
                value = inputVal["value"]
                if type == "symbol":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val, _type="ohlc")
                elif type == "dataInput" or type == "any":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val, _type="ohlc")
                elif type == "feature":
                    val = value
                    if isinstance(val, dict):
                        val = value["id"] if "id" in value else value["value"]
                    raw_inputs[key] = self.getDataFrameColumn(key, val)
                elif type == "any":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "number":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "int":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                elif type == "float":
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
                else:
                    raw_inputs[key] = value
                    self.dataFrame[key] = value
            except Exception as e:
                tb = traceback.format_exc()
                self.logger().error("Problem on extracting data", e)
                pass

        return raw_inputs

    def initialize(self):
        pass
    
    def getDf(self):
        return self.dataFrame
    
    def getChannel(self):
        return self.workerChannel

    def callIndicator(self, targetIndicatorFunction, raw_inputs, chart):
        process = None

        start = time.time()
        if (inspect.iscoroutinefunction(targetIndicatorFunction["process"])):
            async def runandwait():
                try:
                    task = asyncio.ensure_future(targetIndicatorFunction["process"](raw_inputs, chart))
                    result = await task
                except Exception as e2:
                    raise e2

            loop = asyncio.new_event_loop()
            process = loop.run_until_complete(runandwait())
        else:
            process = targetIndicatorFunction["process"](raw_inputs, chart)

        return process
        
    def getWorkerJobDataFrame(self, workerJob):
        df = pd.DataFrame()
        if hasattr(self, 'chartConfigData'):

            configData = self.chartConfigData
            if self.chipmunkDb is None:
                # self.chartConfigData.chipmunkdbHost
                self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host("chipmunkdb1"))
            start = time.time()
            if configData.chart_prefix:
                df = self.chipmunkDb.collection_as_pandas(configData.workspace_id, columns=[],
                                                          domain=configData.chart_prefix)
            else:
                df = self.chipmunkDb.collection_as_pandas(configData.workspace_id, columns=[])
            df = df.sort_index()
            end = time.time()
            self.logger().info("Downloading DataFrame from chipmunk %d ms", end - start)

            if configData.chart_prefix != "" and configData.chart_prefix is not None:
                df.columns = df.columns.str.replace('^'+configData.chart_prefix + ".", "", regex=True)

                if "symbol." not in df.columns:
                    # we need to copy open, high, low, close
                    key = "symbol"
                    df[key + ":open"] = df["main:open"]
                    df[key + ":high"] = df["main:high"]
                    df[key + ":low"] = df["main:low"]
                    df[key + ":close"] = df["main:close"]
                    df[key + ":volume"] = df["main:volume"]

        return df

        # currentWorkerJobData = b''
        #for dataBlock in self.stub.GetWorkerJobData(workerJob):
        #    currentWorkerJobData = currentWorkerJobData + bytes(dataBlock.data)

        #if len(currentWorkerJobData) > 0:
        #    decompressed_data = zlib.decompress(currentWorkerJobData, 15 + 32)
        #    df = pd.DataFrame(json.loads(decompressed_data))
        #    df['Datetime'] = pd.to_datetime(df['datetime'], unit='s')
        #    df = df.set_index(['Datetime'])
        #else:
        #    df = pd.DataFrame()

        #return df
    
    def runProcess(self):
        try:
            self.run()

        except Exception as e:
            self.logger().error(e)
            self.onErrorProcess(e)
            return

        self.logger().info("Finished")
        self.onFinishedProcess()
    
    def run(self):
        pass

    def onErrorProcess(self, e):
        self.stop()
        self.factory.onWorkerJobProcessError(self, e)

    def onFinishedProcess(self):
        self.stop()
        self.factory.onWorkerJobProcessFinished(self)
        
    def stop(self):
        self.stopped = True
        #self.listenThread.join()
        
    def onBeforeDownloadData(self):
        pass

    def reloadDataFrame(self):
        self.dataFrame = self.getWorkerJobDataFrame(self.workerJob)
        return True
    
    def downloadAndRunprocess(self):
        try:
            self.onBeforeDownloadData()

            self.initialize()
            self.dataFrame = self.getWorkerJobDataFrame(self.workerJob)
            if (self.stopped == False):
                self.stop()
                self.stopped = True

            self.listenThread = threading.Thread(target=self.runProcess, daemon=True)
            self.listenThread.start()
        except Exception as e:
            self.onErrorProcess(e)
            return False
            
        return True

    def startProcessWithDataFrame(self, dataFrame):
        try:
            self.onBeforeDownloadData()

            self.initialize()
            self.dataFrame = dataFrame
            if (self.stopped == False):
                self.stop()
                self.stopped = True

            self.listenThread = threading.Thread(target=self.runProcess, daemon=True)
            self.listenThread.start()

        except Exception as e:
            self.onErrorProcess(e)
            return False

        return True

    def startProcess(self):
        
        downloadThread = threading.Thread(target=self.downloadAndRunprocess, daemon=True)
        downloadThread.start()

        pass

    def setConfig(self, configuration):
        pass
    
    