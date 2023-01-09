import asyncio
import threading
import time

from typing import List
import datetime
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import pandas as pd
import numpy as np
import json

from coinlib import Registrar, CoinlibDataInterface, helper
from coinlib.ChartsIndicatorJob import ChartsIndicatorJob
from coinlib.BasicJob import BasicJob
from coinlib.broker.BrokerDTO import BrokerSymbol
from coinlib.data.CollectionInterface import CollectionInterface
from coinlib.data.DataTable import DataTable
from coinlib.dataWorker_pb2 import ParameterTable
from coinlib.drawable.CoinlibDrawable import CoinlibDrawable
from coinlib.event.EventInterface import EventInterface
from coinlib.helper import serializeDTO, to_trendline, trendline
from coinlib.logics.LogicBasicWorker import LogicBasicWorker
from coinlib.logics.manager.LogicJobBroker import LogicJobBroker
import aio_pika
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from coinlib.logics.manager.LogicManager import LogicManager


class LogicJob(BasicJob):
    trader: LogicJobBroker = None
    broker: LogicJobBroker = None
    function_results: any = {}

    # , name, group, inputs, df, indicator, worker
    def __init__(self, table: DataTable, logicComponentInfo, logicElement, inputs, manager: LogicManager,
                 worker: LogicBasicWorker):
        super(LogicJob, self).__init__(table, inputs, manager)

        self.registrar = Registrar()
        self.trader: LogicJobBroker = None
        self.broker: LogicJobBroker = None
        self.drawable: CoinlibDrawable = CoinlibDrawable(manager, worker)
        self.component = logicComponentInfo
        self.setUniqueName(logicElement.identifier)
        self.logicElement = logicElement
        self.worker: LogicBasicWorker = worker
        self.name = logicElement.identifier
        self.manager: LogicManager = manager

        self.params = {}
        self.connectDataInterface()

        self.trader: LogicJobBroker = manager.getBroker()
        # both names can work
        self.broker = manager.getBroker()
        self.alerts = self
        self.screener = self

    def connectDataInterface(self):
        self.data = CoinlibDataInterface()
        self.data.connect()

    def getWorker(self) -> LogicBasicWorker:
        return self.worker

    def getSymbol(self, chart=None) -> [BrokerSymbol]:
        return self.manager.getSymbolForChart(chartId=chart)

    def getStub(self) -> stats.DataWorkerStub:
        return self.worker.getStub()

    def collection(self, nameOfCollection: str) -> CollectionInterface:
        if nameOfCollection not in self.registrar.collectionInterfaceList:
            self.registrar.collectionInterfaceList[nameOfCollection] = CollectionInterface(nameOfCollection,
                                                                                           self.worker.getDataServerForCollection(
                                                                                               nameOfCollection))
        return self.registrar.collectionInterfaceList[nameOfCollection]

    def traderName(self):
        return "ASDASD"

    def event(self) -> EventInterface:
        return EventInterface(self)


    def onPartialChartDataReceived(self, indicator, name, result_data, options):

        self.function_results[indicator["group"]+"."+indicator["name"]][name] = result_data

        return True

    def setParameterTable(self, parameterTable: ParameterTable):
        params = {}
        for p in parameterTable.parameters:
            val = json.loads(p.value)
            params[p.name] = val
        self.params = params

    def hasParam(self, paramName: str):
        if paramName in self.params:
            return True
        return False

    def param(self, paramName: str):
        if paramName in self.params:
            return self.params[paramName]
        return None

    def function(self, group: str, functn: str, parameters):

        worker = self.getWorker()

        indicator_method = worker.getIndicatorMethodByName(group, functn)

        if indicator_method is not None:

            raw_inputs = {}
            raw_inputs["name"] = indicator_method.subfeature
            raw_inputs["group"] = indicator_method.feature
            inputs = {}

            datatable = DataTable()

            for i in indicator_method.inputs:

                if i["name"] in parameters:
                    raw_inputs[i["name"]] = parameters[i["name"]]

                    if i["type"] == "symbol":
                        datatable.setColumn(i["name"]+":y", parameters[i["name"]])

                    if i["type"] == "input":
                        datatable.setColumn(i["name"]+":y", parameters[i["name"]])
                else:
                    if "required" in i and i["required"] == 'true':
                        raise Exception(
                            "Missing the parameter: " + i["name"] + ". Please check all nededed input parameters.")
                    raw_inputs[i["name"]] = None
            self.function_results[group+"."+functn] = {}
            
            chart = ChartsIndicatorJob(indicator_method.subfeature, indicator_method.feature,
                                       inputs, datatable, indicator_method.original, self)
               
            ### lets see
            worker.callIndicator(indicator_method.original, raw_inputs, chart)


            extracted_data = []
            for d in self.function_results[group+"."+functn].keys():
                datatable = self.function_results[group+"."+functn][d]
                extracted_data.append(datatable.asArray())
            if len(extracted_data) == 1:
                return extracted_data[0]

            return extracted_data

        return None

    def log(self, log: str, data: any = None):
        result = ""
        o = log
        if log is not None and not isinstance(log, str):
            o = json.dumps(log, default=serializeDTO)
        result += o
        # this is only for development
        print(log, data)
        # Iterating over the Python kwargs dictionary
        try:
            o = data
            if data is not None and not isinstance(data, str):
                o = json.dumps(data, default=serializeDTO)
            result += o
        except Exception as e:
            pass

        self.manager.log(result)

        return result

    def getTrader(self) -> LogicJobBroker:
        return self.trader

    def getName(self):
        return self.name

    def isLivetrader(self):
        return self.manager.isLivetrader()

    def isPapertrader(self):
        return self.manager.isPapertrader()

    def isBacktrader(self):
        return self.manager.isBacktrader()

    #### Symbol Blocks

    ##### Trader Blocks

    ## reachable through .broker / .trader

    #### Alert blocks

    def notification(self, text, notificationModule, images=[], parameters={}, auth={}):

        self.manager.saveInfo("notification", "notification",
                              {"text": text, "module": notificationModule, "parameters": parameters})

        return True

    def notificationInteractive(self, callback, text, buttons, notificationModule, images=[], parameters={}, auth={}):

        self.manager.saveInfo("notification", "notificationInteractive",
                              {"text": text, "buttons": buttons, "module": notificationModule,
                               "parameters": parameters})

        return True
