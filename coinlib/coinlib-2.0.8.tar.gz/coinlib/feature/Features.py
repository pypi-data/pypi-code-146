import asyncio
from enum import Enum
from typing import List
from coinlib.Registrar import Registrar
from coinlib.broker.BrokerDTO import BrokerContractType, BrokerAssetType, BrokerExchangeEntry

from coinlib.broker.CoinlibBrokerFuture import CoinlibBrokerFuture
from coinlib.broker.CoinlibBrokerMargin import CoinlibBrokerMargin
from coinlib.broker.CoinlibBrokerSpot import CoinlibBrokerSpot
from coinlib.config import grpc_chan_ops
from coinlib.feature.CoinlibFeature import CoinlibFeature
from coinlib.helper import get_current_kernel, get_current_plugin_code_type, get_current_plugin_code, \
    find_current_runner_file, printError, checkIfCodeContainsVersionorExit, serializeDTO
import copy
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import simplejson as json
from coinlib.helper import is_in_ipynb
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
import inspect
from google.protobuf.json_format import MessageToDict
import os
import sys
from typing import TypedDict


def convertContractTypesToGrpc(types: List[BrokerContractType]):
    list = []
    for type in types:
        t = statsModel.BrokerExchange.ContractType.SPOT
        if type == BrokerContractType.SPOT:
            t = statsModel.BrokerExchange.ContractType.SPOT
        if type == BrokerContractType.CREDIT:
            t = statsModel.BrokerExchange.ContractType.CREDIT
        if type == BrokerContractType.FUTURE:
            t = statsModel.BrokerExchange.ContractType.FUTURE
        if type == BrokerContractType.MARGIN:
            t = statsModel.BrokerExchange.ContractType.MARGIN
        if type == BrokerContractType.INDEX:
            t = statsModel.BrokerExchange.ContractType.INDEX
        list.append(t)

    return list

def convertAssetTypesToGrpc(types: List[BrokerAssetType]) :
    list = []

    for type in types:
        t = statsModel.BrokerExchange.AssetType.COIN
        if type == BrokerAssetType.COIN:
            t = statsModel.BrokerExchange.AssetType.COIN
        if type == BrokerAssetType.FOREX:
            t = statsModel.BrokerExchange.AssetType.FOREX
        if type == BrokerAssetType.STOCK:
            t = statsModel.BrokerExchange.AssetType.STOCK

        list.append(t)

    return list


class FeatureType(Enum):
    Global = "global"
    Symbol = "symbol"
    Feature = "feature"

class FeatureModuleType(Enum):
    fetcher = "fetcher"
    processors = "processors"
    lake = "lake"

class Features:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.featureInterface = stats.FeaturesStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def registerFeature(self, callbackClass: CoinlibFeature, featureIdentifier: str,
                       featureTitle: str,
                       type: FeatureModuleType = FeatureModuleType.processors,
                       description: str = "",
                       estimatedDataInterval: int = 60*60,
                       options=None):

        registration = statsModel.FeatureRegistration()
        registration.identifier = featureIdentifier
        registration.name = featureTitle
        registration.estimatedDataInterval = estimatedDataInterval
        registration.description = description
        registration.type = type.name
        registration.stage = self.registrar.environment

        try:

            ctx = callbackClass()

            loop = asyncio.new_event_loop()
            feature_infos = loop.run_until_complete(ctx.get_feature_infos())

            registration.feature_infos = json.dumps(feature_infos, default=serializeDTO)

        except Exception as e:
            self.registrar.logger.error("We cannot load your features rom your Class ")
            raise e

        if options is not None:
            for o in options:
                option = statsModel.FeatureOptions()
                option.identifier = o["id"] if "id" in o else o["name"] if "name" in o else o["identifier"]
                option.type = o["type"] if "type" in o else "string"
                option.defaultValue = o["defaultValue"] if "defaultValue" in o else ""
                registration.options.append(option)

        if not is_in_ipynb:

            abs_path, only_filename = find_current_runner_file()
            registration.code = get_current_plugin_code(abs_path)
            code_version = checkIfCodeContainsVersionorExit(registration.code)

            if self.registrar.isLiveEnvironment():
                splitted = only_filename.split("_")
                only_filename_without_version = "_".join(splitted[:-1])
                registration.plugin = only_filename_without_version
                registration.pluginVersion = splitted[-1].replace("-", ".")
            else:
                registration.plugin = only_filename
                registration.pluginVersion = code_version

        else:
            abs_path = ipynb_path.get()
            only_filename = os.path.splitext(os.path.basename(abs_path))[0]

            registration.plugin = only_filename
            registration.pluginVersion = "?"

        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.featureCallbacks["feature_"+registration.identifier] = registration_dict
        self.registrar.featureCallbacks["feature_"+registration.identifier]["process"] = callbackClass

        try:
            d = self.featureInterface.registerFeature(registration)
            print(d)
        except Exception as e:
            print(e)
            return False

        return True