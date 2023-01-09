import pandas as pd
import numpy as np

from coinlib.BasicJob import BasicJob
from coinlib.data.DataTable import DataTable


class StatisticRuleJob(BasicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, df, inputs, statisticId, worker):
        super(StatisticRuleJob, self).__init__(DataTable(df), inputs)
        self.statisticId = statisticId
        self.worker = worker
        self.result_col = None

        pass

    def getOutputCol(self):
        return "r_"+self.statisticId

    def getResultColumns(self):
        return self.result_col

    def result(self, resultList, colname=None, fillType="front"):
        ret = super().result([np.int(i if not np.isnan(i) else 0) for i in resultList], colname, fillType)

        if "to_numpy" in ret:
            self.result_col = ret.to_numpy()
        else:
            self.result_col = ret

        return self.result_col
