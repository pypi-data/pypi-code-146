import copy
import re

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import json

from coinlib.config import grpc_chan_ops
from coinlib.helper import is_in_ipynb, get_current_plugin_code_type, get_current_plugin_code, find_current_runner_file
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
import os
import ipynb_path
import sys
from coinlib.Registrar import Registrar
import inspect
from google.protobuf.json_format import MessageToDict


class Statistics:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.statisticsInterface = stats.StatisticsStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)


    def registerStatisticsRuleFunction(self, process, identifier,
                                   name, description, inputs,
                                   group=""):
        type = "stats_function"

        registration = statsModel.StatisticRuleFunctionRegistration()
        registration.identifier = identifier
        registration.name = name
        registration.group = group
        registration.description = description

        registration.stage = self.registrar.environment

        if not is_in_ipynb:

            abs_path, only_filename = find_current_runner_file()
            registration.code = get_current_plugin_code(abs_path)
            code_version = self.checkIfCodeContainsVersionorExit(registration.code)
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

        for input in inputs:
            inputModel = statsModel.StatisticFunctionInputs()
            inputModel.type = input["type"]
            inputModel.identifier = input["identifier"]
            inputModel.label = input["label"]
            if "default" in input:
                inputModel.defaultValue = input["default"]
            registration.inputs.append(inputModel)


        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.statisticsCallbacks["rule_"+group + "." + identifier] = registration_dict
        self.registrar.statisticsCallbacks["rule_"+group + "." + identifier]["process"] = process

        self.statisticsInterface.registerStatisticRuleFunction(registration)

        return True

    def checkIfCodeContainsVersionorExit(self, code):
        found = False
        try:
            found = re.search('(#version:)[ ]*([0-9a-z]*\.[0-9a-z]*\.[0-9a-z]*)([\n,\\\n])', code).group(2)

        except AttributeError:
            found = False

        if not found:
            print("ERROR: You should add '#version: 1.X.X' to your file")
            sys.exit(0)
        return found

    def registerStatisticMethod(self, process, identifier, name,
                                   description, inputs: [], refreshOn=[]):
        type = "stats_method"

        registration = statsModel.StatisticMethodRegistration()
        registration.identifier = identifier
        registration.name = name
        for r in refreshOn:
            registration.refreshOn.append(r)
        registration.description = description
        registration.stage = self.registrar.environment

        if not is_in_ipynb:

            abs_path, only_filename = find_current_runner_file()
            registration.code = get_current_plugin_code(abs_path)

            code_version = self.checkIfCodeContainsVersionorExit(registration.code)
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

        for input in inputs:
            inputModel = statsModel.StatisticMethodInputs()
            inputModel.type = input["type"]
            inputModel.identifier = input["identifier"]
            inputModel.label = input["label"]
            if "values" in input:
                inputModel.values = json.dumps(input["values"])
            if "default" in input:
                inputModel.defaultValue = input["default"]
            if "defaultValue" in input:
                inputModel.defaultValue = input["defaultValue"]
            registration.inputs.append(inputModel)


        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.statisticsCallbacks["method_"+identifier] = registration_dict
        self.registrar.statisticsCallbacks["method_"+identifier]["process"] = process

        self.statisticsInterface.registerStatisticMethod(registration, metadata=self.registrar.getAuthMetadata())

        return True
