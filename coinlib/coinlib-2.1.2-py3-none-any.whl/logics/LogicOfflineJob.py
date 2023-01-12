from coinlib.data.DataTable import DataTable
from coinlib.logics.LogicJob import LogicJob


class LogicOfflineJob(LogicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, table: DataTable, logicComponentInfo, logicElement, inputs, fakeManager, worker):
        super(LogicOfflineJob, self).__init__(table, logicComponentInfo, logicElement, inputs, fakeManager, worker)
        self.worker = worker
        self.result_col = None

        pass


    def connectDataInterface(self):
        pass