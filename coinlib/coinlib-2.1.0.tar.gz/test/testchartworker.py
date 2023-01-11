import json
import threading
from munch import munchify
import pandas as pd
import pyarrow as pa
import time
import pyarrow.parquet as pq
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import chipmunkdb
from chipmunkdb.ChipmunkDb import ChipmunkDb

from coinlib import log
from coinlib.ChartsFactory import ChartsFactory
from coinlib.ChartsWorker import ChartsWorker

class TestChartWorker(ChartsWorker):

    def initialize(self):
        super().initialize()
        self.chartConfigData = statsModel.ChartDataInfo()
        self.chartConfigData.chart_prefix = "chart1"
        data = json.loads("""{"elements": [{"indicator": {"id_output": null, "chartType": "line","type": "function","feature": "Talib","subfeature": "sma","short": "Simple Moving Average","stage": "live","id": "nQ2t7aMiva1P","elementId": "5ebec9d6c351cd00a9f2443a","name": "sma_1"},"indicatorConfig": "{'symbol':{'type':'dataInput','value':{'label':'main','value':'main'}},'period':{'type':'int','value':30},'color':{'type':'string','value':'#1F41AB'}}"}],
"children": {
  "elements": [{
    "indicator": {
    "id_output": null, 
      "chartType": "line",
      "type": "function",
      "feature": "Talib",
      "subfeature": "wma",
      "short": "Weighted Moving Average",
      "stage": "live",
      "id": "qbG8izwhvM7Y",
      "elementId": "5ebec9d6c351cd00a9f24445",
      "name": "wma_1"
    },
    "indicatorConfig": "{'symbol':{'type':'dataInput','value':{'label':'sma_1','value':'sma_1'}},'period':{'type':'int','value':15},'color':{'type':'string','value':'#b7e03a'}}"
  }],
  "children": {
  }
}}""")
        chartConfig = munchify(data)
        self.chartConfig = chartConfig

        return True

    def getWorkerJobDataFrame(self, workerJob):
        df = pd.DataFrame()
        if hasattr(self, 'chartConfigData'):

            configData = self.chartConfigData
            start = time.time()
            if configData.chart_prefix:
                df = self.chipmunkDb.collection_as_pandas("live_60f434f170dcb7707b729233_610e6420a85ca69ade34d7cb", columns=[],
                                                          domain=configData.chart_prefix)
            else:
                df = self.chipmunkDb.collection_as_pandas("live_60f434f170dcb7707b729233_610e6420a85ca69ade34d7cb", columns=[])
            end = time.time()
            log.info("Downloading DataFrame from chipmunk ", end - start)

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

    def onFinishedProcess(self):
        self.stop()
        print("MUH")

    def getIndicatorConfiguration(self, element):
        return json.loads(element.indicatorConfig.replace("'", "\""))

    def downloadAndRunprocess(self):
        try:

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

factory = ChartsFactory()
factory.loadPlugins()

workerJob = statsModel.WorkerJob()

workerJobProcess = TestChartWorker(workerJob, None)


workerJobProcess.downloadAndRunprocess()
time.sleep(0.5)

while True:

    workerJobProcess.downloadAndRunprocess()

    time.sleep(0.5)






