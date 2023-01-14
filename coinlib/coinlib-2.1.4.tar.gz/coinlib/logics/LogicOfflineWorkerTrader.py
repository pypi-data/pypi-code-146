from coinlib.data.DataTable import DataTable
from coinlib.logics.LogicOfflineWorker import LogicOfflineWorker
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib.logics.manager.LogicManager import LogicManager
from coinlib.logics.manager.PortfolioModel import PortfolioModel
from coinlib.logics.offlineManager.LogicOfflineJobFakeFutureBroker import LogicOfflineJobFakeFutureBroker
from coinlib.logics.offlineManager.LogicOfflineJobFakeSpotBroker import LogicOfflineJobFakeSpotBroker


class LogicOfflineWorkerTrader(LogicOfflineWorker):

    def initialize(self):
        super().initialize()

        self._portfolio = PortfolioModel.from_stats_model(self.logicConfig.portfolio)

    def onNextSubTableReceived(self, fakeManager: LogicManager, subTable: DataTable):
        fakeManager.broker.setTable(subTable)

    def onBeforeSingleStepRunng(self, fakeManager: LogicManager, subTable: DataTable):
        # first we run this and then the next one
        fakeManager.broker.runOrderCalculation()

    def onAfterSingleStepRunning(self, fakeManager: LogicManager):
        fakeManager.broker.calculateStatistics()
        if fakeManager.hasChanged():
            fakeManager.savePortfolio()

    def onBeforeRunInitialize(self, fakeManager: LogicManager):
        if self.logicConfig.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.FUTURE:
            fakeManager.setBroker(LogicOfflineJobFakeFutureBroker(fakeManager))
        elif self.logicConfig.brokerAccount.brokerType == self.logicConfig.brokerAccount.BrokerType.SPOT:
            fakeManager.setBroker(LogicOfflineJobFakeSpotBroker(fakeManager))

    def getStatistics(self, fakeManager: LogicManager) -> statsModel.LogicRunnerStatistics:
        broker_stats = self.manager.broker.getStatistics()
        return broker_stats