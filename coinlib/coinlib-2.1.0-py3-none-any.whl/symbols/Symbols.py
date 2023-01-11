from coinlib.config import grpc_chan_ops
from coinlib.helper import get_current_kernel, get_current_plugin_code_type, get_current_plugin_code, \
    find_current_runner_file, checkIfCodeContainsVersionorExit
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
from coinlib.Registrar import Registrar
from google.protobuf.json_format import MessageToDict
import os
import sys


class Symbols:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.symbolInterface = stats.SymbolStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def registerSymbolBroker(self, brokerInfoProcess,
                             downloadHistorical,
                             consumeLive, fetchCandles, consumeOrderBook,
                             brokerIdentifier, brokerName, options):

        registration = statsModel.SymbolBrokerRegistration()
        registration.identifier = brokerIdentifier
        registration.name = brokerName
        registration.stage = self.registrar.environment

        for o in options:
            option = statsModel.SymbolBrokerOptions()
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
        self.registrar.symbolBrokerCallbacks["method_"+registration.identifier] = registration_dict
        self.registrar.symbolBrokerCallbacks["method_"+registration.identifier]["process"] = {
            "brokerInfoProcess": brokerInfoProcess,
            "downloadHistorical": downloadHistorical,
            "fetchCandles": fetchCandles,
            "consumeLive": consumeLive,
            "consumeOrderBook": consumeOrderBook
        }

        self.symbolInterface.registerSymbolBroker(registration, metadata=self.registrar.getAuthMetadata())

        return None