import datetime
import traceback

import pytz

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import pandas as pd
import numpy as np
import pyarrow as pa
import time
from datetime import datetime
from coinlib.data.DataTable import DataTable
from coinlib.logics.LogicBasicWorker import LogicBasicWorker
from coinlib.logics.LogicOptions import LogicOptions
from coinlib.logics.manager.LogicManager import LogicManager
from coinlib.logics.offlineManager.LogicOfflineJobFakeBroker import LogicOfflineJobFakeBroker
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.logics.LogicOfflineJob import LogicOfflineJob
from coinlib.logics.offlineManager.LogicOfflineJobFakeFutureBroker import LogicOfflineJobFakeFutureBroker
from coinlib.logics.offlineManager.LogicOfflineJobFakeSpotBroker import LogicOfflineJobFakeSpotBroker

from coinlib.logics.manager.PortfolioModel import PortfolioModel

class LogicOfflineWorker(LogicBasicWorker):
    _portfolio: PortfolioModel

    def initialize(self):
        super().initialize()
        self.logicInterface = stats.LogicRunnerOfflineServiceStub(self.getChannel())
        logicInfoFullData = self.logicInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
        self.logicConfig = logicInfoFullData.logicInfo
        self.appWorkerId = self.logicConfig.app_worker_id
        self.appWorkerRunnerId = self.logicConfig.app_worker_runner_id
        self.logicMode = self.logicConfig.logicMode
        self._portfolio = PortfolioModel()
        self.logicOptions = {}
        try:
            self.logicOptions = json.loads(self.logicConfig.options_json)
        except:
            pass
        self.makerFee = self.logicOptions["makerFee"]
        self.takerFee = self.logicOptions["takerFee"]
        self.advancedDataInfo = json.loads(logicInfoFullData.advancedDataInfo)
        self.startDate = pd.Timestamp(self.logicConfig.startDate)  # .tz_localize(None)
        self.endDate = pd.Timestamp(self.logicConfig.endDate) #  .tz_localize(None)
        self.chartConfigData = logicInfoFullData.chartData
        return True


    def getLogicMode(self):
        return self.logicMode

    def onLogicRunnerError(self, job, error):

        self.saveLogicStorageToDataFrame()

        statsError = statsModel.LogicRunnerOfflineWorkerError()
        statsError.error.message = str(error)
        statsError.worker.CopyFrom(self.workerJob)

        self.logicInterface.OnRunnerErrorOccured(statsError, metadata=self.registrar.getAuthMetadata())

        return False

    def isOfflineWorker(self):
        return True

    def broadcastCurrentPercentage(self, percentage, manager):
        partiallyData = statsModel.LogicRunnerOfflineWorkerPartiallyData()
        partiallyData.percentage = percentage
        partiallyData.signalData = json.dumps({"keys": manager.getSignalData()}, ensure_ascii=False).encode('gbk')
        partiallyData.worker.CopyFrom(self.workerJob)

        partiallyData.statistic.CopyFrom(self.getStatistics(manager))

        data = self.logicInterface.OnRunnerPartiallyData(partiallyData, metadata=self.registrar.getAuthMetadata())


    def generateLocalJob(self):

        inputs = {}
        logicWithInfo = self.logicComponentsWithInfo[0]
        logic = logicWithInfo.logic
        logicComponentInfo = logicWithInfo.info

        logicJob = self.generateJob(self.currentTable, logicComponentInfo, logic, inputs, self.manager)
        return logicJob

    def runOfflineLogicForTimerange(self):

        try:
            index = 0
            lastPercentage = 0
            startDate = self.startDate
            endDate = self.endDate
            self.parameterTable = self.logicConfig.parameterTable

            # special case lets unset all "old" logic results
            self.dataFrame = self.dataFrame.loc[:,~self.dataFrame.columns.str.contains('^result.', case=False)]

            if self.dataFrame.shape[0] > 0:
                rowIndexZero = self.dataFrame.index[0]
                if rowIndexZero.tzinfo is None:
                    endDate = endDate.tz_localize(None)

            self.generateLogicComponentsInfo()
            self.onBeforeWorkerStarts()

            logicOptions = LogicOptions(self.logicOptions)

            fakeManager = LogicManager("name of trader", self.logicConfig,
                                       self.logicConfig.brokerAccount,
                                       self._portfolio, advancedInfo=self.advancedDataInfo,
                                       options=logicOptions)
            fakeManager.resetLastValue()
            self.manager = fakeManager

            self.onBeforeRunInitialize(fakeManager)

            table = DataTable()
            self.currentTable = table

            minimumPeriod = 200
            index = 0
            columns = self.dataFrame.columns.to_list()
            setdf = []
            infoBlock = {}
            ##for row in self.dataFrame.itertuples(index=True, name='Pandas'):

            ## if we are in "byTime" mode than we iterate other.

            if self.logicOptions and "runnerMode" in self.logicOptions and \
                self.logicOptions["runnerMode"] == "byTime":
                interval = float(self.logicOptions["runnerModeInterval"]) if "runnerModeInterval" in self.logicOptions else 60
                startDate = startDate.tz_localize(None)
                endDate = endDate.tz_localize(None)
                startDateTimestamp = time.mktime(startDate.timetuple())
                endDateTimestamp = time.mktime(endDate.timetuple())

                intervalComplete = endDateTimestamp - startDateTimestamp
                current_time = startDateTimestamp
                while current_time < endDateTimestamp:
                    dta = datetime.fromtimestamp(current_time)

                    if not table.hasIndex(dta):
                        table.addRow({"datetime": dta})

                    current_time = current_time + (interval * 60)
            else:
                table.from_df(self.dataFrame)


            rowLength = table.length()

            for row in table.rows():
                index = index + 1
                self.currentTable = table

                index_date = row[table.col["datetime"]]

                index_date = index_date.replace(tzinfo=None)
                startDate = startDate.replace(tzinfo=None)
                endDate = endDate.replace(tzinfo=None)

                percentage = index / rowLength
                if percentage-0.08 > lastPercentage:

                    lastPercentage = percentage

                    threading.Thread(target=self.broadcastCurrentPercentage, args=[lastPercentage, fakeManager], daemon=True).start()

                if startDate and index_date > startDate and index > minimumPeriod:

                    lastindex = index-minimumPeriod if index-minimumPeriod > 0 else 0
                    subTable = table.subTable(lastindex, minimumPeriod)

                    fakeManager.setTable(subTable)
                    self.onNextSubTableReceived(fakeManager, subTable)
                    fakeManager.updateCurrentIndexToLast()
                    fakeManager.resetChanges()

                    self.onBeforeSingleStepRunng(fakeManager, subTable)

                    self.runLogicComponents(subTable, fakeManager)

                    self.onAfterSingleStepRunning(fakeManager)

                    infoBlock[index-1] = fakeManager.getLastStorageRow()

                else:
                    infoBlock[index - 1] = {}
                    
            fakeManager.onLogicStepFinished()

        except Exception as e:
            tb = traceback.format_exc()
            self.logger().error(tb)
            self.extractLogicInfosFromManagerData(infoBlock)
            self.onLogicRunnerError(None, e)
            return False

        self.extractLogicInfosFromManagerData(infoBlock)

        self.onLogicRunningFinished()

        return True

    def onNextSubTableReceived(self, fakeManager: LogicManager, subTable: DataTable):
        pass


    def onBeforeRunInitialize(self, fakeManager: LogicManager):
        pass

    def onBeforeSingleStepRunng(self, fakeManager: LogicManager, subTable: DataTable):
        pass

    def onBeforeSingleStepRunng(self, fakeManager: LogicManager, subTable: DataTable):
        pass

    def onAfterSingleStepRunning(self, fakeManager: LogicManager):
        pass

    def generateJob(self, table, logicComponentInfo, logic, inputs, fakeManager):
        return LogicOfflineJob(table, logicComponentInfo, logic, inputs, fakeManager, self)

    def run(self):

        t = threading.Thread(target=self.runOfflineLogicForTimerange, args=[], daemon=True)
        t.start()

        try:
            t.join()
        except Exception as e:
            pass

        finishedData = statsModel.LogicRunnerOfflineWorkerFinishedData()
        finishedData.signalData = json.dumps({"keys": self.manager.getSignalData()}, ensure_ascii=False).encode('gbk')
        finishedData.worker.CopyFrom(self.workerJob)

        finishedData.statistic.CopyFrom(self.getStatistics(self.manager))

        self.logicInterface.OnRunnerFinishedComplete(finishedData, metadata=self.registrar.getAuthMetadata())

        return True

    def getStatistics(self, fakeManager: LogicManager) -> statsModel.LogicRunnerStatistics:
        return statsModel.LogicRunnerStatistics()