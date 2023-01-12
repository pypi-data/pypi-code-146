from datetime import datetime

from chipmunkdb.ChipmunkDb import ChipmunkDb

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import simplejson as json

from coinlib.config import grpc_chan_ops
from coinlib.helper import is_in_ipynb
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
from coinlib.Registrar import Registrar
import grpc

import inspect
from google.protobuf.json_format import MessageToDict
import os
import sys
from google.protobuf.json_format import MessageToJson

class CoinlibDataInterface:
    channel = None

    def __init__(self):
        self.registrar = Registrar()


    def connect(self):
        self.channel = self.createChannel()
        self.dataInterface = stats.DataLoaderWorkerStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def getAllExchanges(self):

        b = statsModel.ExchangeDataRequestInfo()

        ret = self.dataInterface.getAllExchanges(b)

        retData = MessageToDict(ret)

        return retData["exchanges"]

    def getAllSymbols(self, additionalDataFeatures=[]):

        b = statsModel.SymbolDataRequestInfo()
        b.additionalDataFeatures = json.dumps(additionalDataFeatures)

        ret = self.dataInterface.getAllSymbols(b)

        retData = MessageToDict(ret)

        return retData["symbols"]

    def getAvailableFeatures(self):

        b = statsModel.AdditionalDataFeatureRequest()

        ret = self.dataInterface.getAdditionalDataFeatures(b)

        retData = MessageToDict(ret)

        return retData["featureInfos"]

    def getMarketData(self, symbol, startDate, endDate, timeframe="1h", exchange=None, contractType="spot", additionalDataFeatures=[]):

        b = statsModel.MarketDataRequest()
        s = statsModel.SymbolBrokerSymbolSmall()
        if exchange is not None:
            s.exchange_id = exchange
        s.symbol = symbol

        b.symbol.CopyFrom(s)
        b.timeframe = timeframe
        b.startDate = datetime.strftime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        b.endDate = datetime.strftime(endDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        b.contractType = contractType
        b.additionalDataFeatures = json.dumps(additionalDataFeatures)

        ret = self.dataInterface.getMarketData(b)

        self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(ret.chipmunkdbHost))
        df = self.chipmunkDb.collection_as_pandas_additional(ret.database_id, additionalCollections=[])

        return df

    def getFeatures(self, featureData: [str], startDate, endDate, timeframe="1h", target_symbol:str = None, target_exchange: str = None):

        b = statsModel.FeatureDataRequest()
        for s in featureData:
            b.feature_name.append(s)

        b.stage = self.registrar.environment
        b.timeframe = timeframe
        b.startDate = datetime.strftime(startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        b.endDate = datetime.strftime(endDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        if target_symbol is not None:
            b.target_symbol = target_symbol
        if target_exchange is not None:
            b.target_exchange = target_exchange

        ret = self.dataInterface.getFeatureData(b)

        self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(ret.chipmunkdbHost))
        df = self.chipmunkDb.collection_as_pandas_additional(ret.database_id, additionalCollections=[])

        return df