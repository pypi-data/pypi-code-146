from google.protobuf.empty_pb2 import Empty

from coinlib.config import grpc_chan_ops
from coinlib.helper import get_current_kernel, get_current_plugin_code, get_current_plugin_code_type, find_current_runner_file
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
import re

from coinlib.logics.LogicDTo import CollectionField
from coinlib.logics.LogicRegistrationInstance import LogicRegistrationInstance


class Logic:
    def __init__(self):
        self.registrar = Registrar()
        self.lastWorkspaceId = None
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.logicInterface = stats.LogicStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)


    def addLogicToWorkspace(self, identifier, type, logicComponentId, params=None ,workspaceId=None, autostart=False):

        if self.registrar.isLiveEnvironment():
            return None

        registration = statsModel.WorkspaceLogicRegistration()
        registration.logicComponentId = logicComponentId
        registration.identifier = identifier

        registration.workerId = self.registrar.worker_id
        registration.type = type
        if params is not None:
            registration.params = str(json.dumps(params, ignore_nan=True))

        registration.stage = self.registrar.environment
        if self.registrar.workspaceId is not None or workspaceId is not None:
            registration.workspaceId = self.registrar.workspaceId if workspaceId is None else workspaceId

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

        self.lastWorkspaceId = workspaceId
        registration.code_type = get_current_plugin_code_type()
        registration.autostart = True
        self.logicInterface.addLogicToWorkspace(registration, metadata=self.registrar.getAuthMetadata())

        return True

    def registerTrader(self, process, identifier, title,
                       inputs=[{"identifier": "symbol", "type": "symbol"}],
                       modules=[], description=""):
        """Register a Trader.

        """

        registration = statsModel.LogicTraderRegistration()
        registration.title = title
        registration.workerId = self.registrar.worker_id
        ## possibel solution for publishing
        ##registration.sourceCode = inspect.getsource(sys._getframe().f_back)
        registration.identifier = identifier
        for input in inputs:
            inputModel = statsModel.LogicInput()
            inputModel.type = input["type"]
            inputModel.identifier = input["identifier"]
            if "label" in input:
                inputModel.label = input["label"]
            if "values" in input:
                inputModel.values = json.dumps(input["values"])
            if "default" in input:
                inputModel.defaultValue = input["default"]
            if "defaultValue" in input:
                inputModel.defaultValue = input["defaultValue"]
            registration.inputs.append(inputModel)

        registration.stage = self.registrar.environment
        if self.registrar.workspaceId is not None:
            registration.workspaceId = self.registrar.workspaceId
        registration.description = description
        for module in modules:
            registration.modules.append(module)

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

        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.logicCallbacks["trader_"+identifier] = registration_dict
        self.registrar.logicCallbacks["trader_"+identifier]["process"] = process

        self.logicInterface.registerTrader(registration, metadata=self.registrar.getAuthMetadata())

        return LogicRegistrationInstance("trader", registration, self.logicInterface, self)

    def runLogic(self):
        logic = statsModel.LogicRunJob()
        logic.workspaceId = self.lastWorkspaceId
        return self.logicInterface.runLogic(logic)

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

    def registerLogic(self, process, identifier, title,
                       inputs=[],
                       modules=[], description=""):
        """Register a Alert.

        """

        registration = statsModel.LogicDataRegistration()
        registration.title = title
        registration.identifier = identifier
        registration.stage = self.registrar.environment
        registration.description = description

        registration.workerId = self.registrar.worker_id
        for input in inputs:
            inputModel = statsModel.LogicInput()
            inputModel.type = input["type"]
            inputModel.identifier = input["identifier"]
            if "label" in input:
                inputModel.label = input["label"]
            if "values" in input:
                inputModel.values = json.dumps(input["values"])
            if "default" in input:
                inputModel.defaultValue = input["default"]
            if "defaultValue" in input:
                inputModel.defaultValue = input["defaultValue"]
            registration.inputs.append(inputModel)

        registration.stage = self.registrar.environment
        if self.registrar.workspaceId is not None:
            registration.workspaceId = self.registrar.workspaceId
        registration.description = description
        for module in modules:
            registration.modules.append(module)


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

        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.logicCallbacks["logic_"+identifier] = registration_dict
        self.registrar.logicCallbacks["logic_"+identifier]["process"] = process

        self.logicInterface.registerDataLogic(registration, metadata=self.registrar.getAuthMetadata())

        return LogicRegistrationInstance("logic", registration, self.logicInterface, self)

    def registerScreener(self, process, identifier, title,
                       inputs=[],
                       modules=[], description=""):
        """Register a Alert.

        """

        registration = statsModel.LogicScreenerRegistration()
        registration.title = title
        registration.identifier = identifier

        registration.workerId = self.registrar.worker_id
        registration.stage = self.registrar.environment
        registration.description = description
        if self.registrar.workspaceId is not None:
            registration.workspaceId = self.registrar.workspaceId
        for input in inputs:
            inputModel = statsModel.LogicInput()
            inputModel.type = input["type"]
            inputModel.identifier = input["identifier"]
            if "label" in input:
                inputModel.label = input["label"]
            if "values" in input:
                inputModel.values = json.dumps(input["values"])
            if "default" in input:
                inputModel.defaultValue = input["default"]
            if "defaultValue" in input:
                inputModel.defaultValue = input["defaultValue"]
            registration.inputs.append(inputModel)

        registration.stage = self.registrar.environment
        registration.description = description
        for module in modules:
            registration.modules.append(module)



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

        registration.code_type = get_current_plugin_code_type()
        registration_dict = MessageToDict(registration)

        # before we send the data, we need to add the "callback"
        # to a global handler list
        self.registrar.logicCallbacks["screener_"+identifier] = registration_dict
        self.registrar.logicCallbacks["screener_"+identifier]["process"] = process

        self.logicInterface.registerScreener(registration, metadata=self.registrar.getAuthMetadata())

        return LogicRegistrationInstance("screener", registration, self.logicInterface, self)

