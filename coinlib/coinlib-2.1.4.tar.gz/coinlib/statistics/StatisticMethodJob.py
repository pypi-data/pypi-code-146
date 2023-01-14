import pandas as pd
import numpy as np
import simplejson as json

from coinlib.data.DataTable import DataTable
from coinlib.BasicJob import BasicJob

class StatisticMethodJob(BasicJob):
    #, name, group, inputs, df, indicator, worker
    def __init__(self, df, inputs, worker):
        super(StatisticMethodJob, self).__init__(DataTable(df), inputs)
        self.worker = worker
        self.result_plots = []

        pass

    def getResultPlots(self):
        return self.result_plots

    def plot(self, plot_fig, name="default"):

        jsondata = plot_fig.to_json()
        plot = {
            "name": name,
            "data": json.loads(jsondata)
        }
        self.result_plots.append(plot)

        return plot
