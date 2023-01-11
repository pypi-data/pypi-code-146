import os
import re
import sys

import ipynb_path

import simplejson as json
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib import Registrar
from coinlib.helper import get_current_plugin_code, find_current_runner_file, is_in_ipynb, get_current_plugin_code_type
from coinlib.logics.LogicDTo import CollectionField


class LogicRegistrationInstance:
    def __init__(self, type: str, registration,
                                logicInterface, logic):
        self.type = type
        self.registrar = Registrar()
        self.logicInterface = logicInterface
        self.registration = registration
        self.logic = logic

    def addLogicToWorkspace(self, identifier, type, logicComponentId, params=None, workspaceId=None):
        return self.logic.addLogicToWorkspace(identifier, type, logicComponentId, params, workspaceId)

    def monitorEvent(self, eventName: str, params: object, callback, description=""):

        registration = statsModel.LogicMonitorEvent()

        registration.name = eventName
        registration.params = json.dumps(params, ignore_nan=True)
        registration.stage = self.registrar.environment
        registration.logicType = self.type
        registration.description=description
        registration.workerId = self.registrar.worker_id

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
        registration.logic_identifier = self.registration.identifier
        registration.logic_version = registration.pluginVersion

        self.logicInterface.registerMonitorEvent(registration)

        if eventName not in self.registrar.logicEventCallback:
            self.registrar.logicEventCallback[eventName] = {
                "name": eventName,
                "callbacks": []
            }

        self.registrar.logicEventCallback[eventName]["callbacks"].append(callback)

        return True

    def useEvent(self, eventName: str, description=""):

        registration = statsModel.LogicEventUsage()

        registration.event = eventName
        registration.stage = self.registrar.environment
        registration.logicType = self.type
        registration.description=description

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

        registration.logic_identifier = self.registration.identifier
        registration.logic_version = registration.pluginVersion
        registration.code_type = get_current_plugin_code_type()

        self.logicInterface.registerEventUsage(registration)

        self.registrar.logicEventRegistration[eventName] = {
            "name": eventName
        }


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

    def useCollection(self, collectionName: str, fields: [CollectionField], description=""):

        registration = statsModel.LogicCollectionUsage()

        registration.name = collectionName
        registration.stage = self.registrar.environment
        registration.fields = str(json.dumps(fields, ignore_nan=True))
        registration.description=description
        registration.logicType = self.type

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

        registration.logic_identifier = self.registration.identifier
        registration.logic_version = registration.pluginVersion
        self.logicInterface.registerCollectionUsage(registration)

        self.registrar.logicCollectionRegistration[collectionName] = {
            "name": collectionName,
            "fields": fields
        }

    def useData(self, groupName: str, dataBlockName: str, name: str=None, type="number",
                symbol: bool = False, exchange: bool = False, description=""):

        registration = statsModel.LogicDataUsage()

        if name is None:
            name = dataBlockName

        registration.group = groupName
        registration.stage = self.registrar.environment
        registration.identifier = dataBlockName
        registration.logicType = self.type
        registration.type = type
        registration.name = name
        registration.symbol = symbol
        registration.exchange = exchange
        registration.description=description


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
        registration.logic_identifier = self.registration.identifier
        registration.logic_version = registration.pluginVersion

        self.logicInterface.registerDataUsage(registration)

        self.registrar.logicDataRegistration[groupName+"_"+dataBlockName] = {
            "groupName": groupName,
            "type": type
        }
