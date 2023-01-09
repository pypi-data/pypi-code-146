import importlib
from IPython import get_ipython
from coinlib.helper import in_ipynb
from coinlib.helper import pip_install_or_ignore
import subprocess
import sys
import timeit
import math

#CHART_DATA_INFLUXDB_HOST="116.203.110.177"
#CHART_DATA_INFLUXDB_DB="coindeck-chartdata"
#CHART_DATA_INFLUXDB_USER="coindeck"
#CHART_DATA_INFLUXDB_PWD="6j8l0gbxsNkpAQXuL8C9"

CHART_DATA_INFLUXDB_HOST="localhost"
CHART_DATA_INFLUXDB_DB="coindeck-chartdata"
CHART_DATA_INFLUXDB_USER=""
CHART_DATA_INFLUXDB_PWD=""

pip_install_or_ignore("influxdb", "influxdb", "5.3.1")

from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from timeit import default_timer as timer
from datetime import timedelta



class InfluxDatabase:

    def __init__(self):
        self.database = CHART_DATA_INFLUXDB_DB
        self.influxClient = InfluxDBClient(CHART_DATA_INFLUXDB_HOST, 8086,
                                   CHART_DATA_INFLUXDB_USER, CHART_DATA_INFLUXDB_PWD, CHART_DATA_INFLUXDB_DB)
        self.dfclient = DataFrameClient(CHART_DATA_INFLUXDB_HOST, 8086,
                                   CHART_DATA_INFLUXDB_USER, CHART_DATA_INFLUXDB_PWD, CHART_DATA_INFLUXDB_DB)

    def getFullChartDataById(self, chart_id):
        data_result = self.dfclient.query('select * from "'+self.database+'"."autogen"."'+chart_id+'"')
        return data_result[chart_id]

    def writeDataFrameColumns(self, chart_id, dataFrame, columns):
        return self.dfclient.write_points(dataFrame, chart_id, field_columns=columns)


    def writeDataFrame(self, chart_id, dataFrame):
        return self.dfclient.write_points(dataFrame, chart_id)


    def writeRawDataColumn(self, chart_id, column, indexes, data):
        points = []
        data_length = 0
        column_formatter = ""
        columns = []
        type = "y"
        for col in data:
            columns.append(col)
            if col == "open":
                type = "ohlc"

        for key in data:
            data_length = len(data[key])
        for i in range(data_length):
            t = indexes[i]
            fields_data = {}
            if type == "y":
                if data["y"][i] is None or math.isnan(data["y"][i]):
                    continue
                fields_data[column+":y"] = data["y"][i]

            if type == "ohlc":
                if data["close"][i] is None or math.isnan(data["close"][i]):
                    continue
                fields_data[column + ":open"] = data["open"][i]
                fields_data[column + ":close"] = data["close"][i]
                fields_data[column + ":high"] = data["high"][i]
                fields_data[column + ":low"] = data["low"][i]
                fields_data[column + ":volume"] = data["volume"][i]
            row = {
                "measurement": chart_id,
                "time": t,
                "fields": fields_data
            }
            points.append(row)

        d = None
        if len(points) > 0:
            d = self.influxClient.write_points(points)
        return d