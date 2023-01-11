from coinlib.logics.LogicOfflineWorker import LogicOfflineWorker
from coinlib.logics.manager.PortfolioModel import PortfolioModel

class LogicOfflineWorkerScreener(LogicOfflineWorker):
    _portfolio: PortfolioModel

    def initialize(self):
        super().initialize()
