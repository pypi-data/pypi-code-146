import re

from coinlib.config import grpc_chan_ops
from coinlib.helper import get_current_kernel, get_current_plugin_code_type, get_current_plugin_code, \
    find_current_runner_file
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


class Notification:
    def __init__(self):
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.notificationInterface = stats.NotificationStub(self.channel)
        pass


    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)



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

    def registerNotification(self, process, identifier, name, inputs = [], description = '', isInteractive=False, interactionCallback=None):

        registration = statsModel.NotificationRegistration()
        registration.identifier = identifier
        registration.name = name
        registration.isInteractive = isInteractive
        registration.description = description
        registration.stage = self.registrar.environment

        for o in inputs:
            option = statsModel.NotificationOptions()
            option.identifier = o["id"] if "id" in o else o["identifier"]
            option.type = o["type"] if "type" in o else "string"
            option.defaultValue = o["defaultValue"] if "defaultValue" in o else ""
            registration.inputs.append(option)

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
        self.registrar.notificationCallbacks["method_"+registration.identifier] = registration_dict
        self.registrar.notificationCallbacks["method_"+registration.identifier]["process"] = process
        if interactionCallback is not None:
            self.registrar.notificationCallbacks["method_" + registration.identifier]["process_extractCallback"] = interactionCallback

        self.notificationInterface.registerNotification(registration, metadata=self.registrar.getAuthMetadata())

        return None