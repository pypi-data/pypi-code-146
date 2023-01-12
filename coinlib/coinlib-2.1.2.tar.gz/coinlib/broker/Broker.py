from enum import Enum
from typing import List
from coinlib.Registrar import Registrar
from coinlib.broker.BrokerDTO import BrokerContractType, BrokerAssetType, BrokerExchangeEntry

from coinlib.broker.CoinlibBrokerFuture import CoinlibBrokerFuture
from coinlib.broker.CoinlibBrokerMargin import CoinlibBrokerMargin
from coinlib.broker.CoinlibBrokerSpot import CoinlibBrokerSpot
from coinlib.config import grpc_chan_ops
from coinlib.helper import get_current_kernel, get_current_plugin_code_type, get_current_plugin_code, \
    find_current_runner_file, printError, checkIfCodeContainsVersionorExit
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

class Broker:
    def __init__(self):
        self.registrar = Registrar()
        self.brokerInterface = None
        self.channel = None
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.brokerInterface = stats.BrokerStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def registerBroker(self, brokerIdentifier: str,
                       brokerName: str, brokerExchanges: List[BrokerExchangeEntry], brokerSpotClass : CoinlibBrokerSpot = None,
                       brokerFutureClass : CoinlibBrokerFuture =None, brokerMarginClass  : CoinlibBrokerMargin =None,
                       options=None):

        registration = statsModel.BrokerRegistration()
        registration.identifier = brokerIdentifier
        registration.name = brokerName
        registration.stage = self.registrar.environment
        if brokerSpotClass is not None:
            registration.brokerTypes.append(statsModel.BrokerRegistration.SPOT)
        if brokerFutureClass is not None:
            registration.brokerTypes.append(statsModel.BrokerRegistration.FUTURE)
        if brokerMarginClass is not None:
            registration.brokerTypes.append(statsModel.BrokerRegistration.MARGIN)

        if len(registration.brokerTypes) <= 0:
            printError("ERROR: You need minimum one Broker Class (brokerSpotClass, brokerFutureClass or brokerMarginClass) otherwise your plugin is useless.")
            return

        anyExchange = False
        for o in brokerExchanges:
            broker = statsModel.BrokerExchange()
            broker.key = o["key"]
            broker.name = o["name"]
            broker.supportDemo = o["supportDemo"] if "supportDemo" in o else False
            broker.positionModeFuture = o["positionModeFuture"] if "positionModeFuture" in o else "merge"
            broker.supportLive = o["supportLive"] if "supportLive" in o else True
            broker.icon = o["icon"] if "icon" in o else ""
            broker.loginMode = o["loginMode"] if "loginMode" in o else statsModel.BrokerExchange.LoginMode.API_KEY
            broker.description = o["description"] if "description" in o else ""
            contracts = convertContractTypesToGrpc(o["contractTypes"]) if "contractTypes" in o else [statsModel.BrokerExchange.ContractType.SPOT]
            for c in contracts:
                broker.contractTypes.append(c)
            assets = convertAssetTypesToGrpc(o["assetTypes"]) if "assetTypes" in o else [
                statsModel.BrokerExchange.AssetType.COIN]
            for a in assets:
                broker.assetTypes.append(a)
            registration.exchanges.append(broker)
            anyExchange = True

        if not anyExchange:
            print("Error: You need to add minimum one exchange to your module.")
            return

        if options is not None:
            for o in options:
                option = statsModel.BrokerOptions()
                option.identifier = o["id"] if "id" in o else o["identifier"]
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
        self.registrar.brokerCallbacks["broker_"+registration.identifier] = registration_dict
        self.registrar.brokerCallbacks["broker_"+registration.identifier]["process"] = {
            "brokerSpot": brokerSpotClass,
            "brokerFuture": brokerFutureClass,
            "brokerMargin": brokerMarginClass
        }

        if self.brokerInterface is not None:
            self.brokerInterface.registerBroker(registration)

        return None