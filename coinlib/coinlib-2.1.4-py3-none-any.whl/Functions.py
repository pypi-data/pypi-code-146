import copy
import re

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import json

from coinlib.config import grpc_chan_ops
from coinlib.helper import is_in_ipynb, get_current_plugin_code_type, find_current_runner_file, get_current_plugin_code
import ipynb_path
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
from coinlib.Registrar import Registrar
from google.protobuf.json_format import MessageToDict
import os
import sys

class Functions:
    def __init__(self):
        self.functionsInterface = None
        self.registrar = Registrar()
        pass

    def connect(self):
        self.channel = self.createChannel()
        self.functionsInterface = stats.FunctionsStub(self.channel)
        pass

    def createChannel(self):
        return grpc.insecure_channel(self.registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops, compression=grpc.Compression.Gzip)
        
    def registerChartFunction(self, process, group, name, short, inputs, description, 
                              dynamicTimeseries=False, unstablePeriod=False, mode=""):
        """
            dynamicTimeseries =  for example ATR based charts which have the special problem of "recalculating" past events (for example renko) 
                            If dynamicTimeseries != False then we will handle this indicator very special
        """
        inputs.insert(0, {"type": "symbol", "name": "symbol", "required": "true"})
        
        self.registerIndicatorFunction(process, group, name, short, 
                                       inputs, description, type="chartType", chartType="line", mode=mode,
                                       dynamicTimeseries=dynamicTimeseries, unstablePeriod=unstablePeriod)
        
        return True
        


    def checkIfCodeContainsVersionorExit(self, code):
        found = False
        try:
            found = re.search('(#version:)[ ]*([0-9a-z]*\.[0-9a-z]*\.[0-9a-z]*)([\n,\\\n])', code).group(2)

        except AttributeError:
            found = False

        if not found:
            self.registrar.logger.error("ERROR: You should add '#version: 1.X.X' to your file")
            sys.exit(0)
        return found

    def registerIndicatorFunction(self, process, group, name, short, inputs, 
                                  description, chartType="", type="function", mode="",
                                  dynamicTimeseries=False, unstablePeriod=False):
        """Register Indicator with callback Functions.
        
            types: 
                - color
                - integer
                - float
                - symbol
                - series
                - select
                - feature
                    if you need some feature we fetch it for you and push it as an input
                    format of feature:
                
                    {name: inputname, feature: featureName, subfeature: None}
                
        
        """
        
        registration = statsModel.ChartWorkerIndicatorRegistration()
        registration.chartType = chartType
        registration.name = name
        registration.group = group
        registration.short_description = short
        registration.dynamicTimeseries = dynamicTimeseries
        registration.type = type
        registration.mode = mode
        registration.inputs = json.dumps(inputs, ensure_ascii=False).encode('gbk')
        registration.stage = self.registrar.environment
        registration.description = description


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

        ### We ignore double registrations to overwrite the plugins in the same worker.
        #if group+"."+name in self.registrar.functionsCallbacks and not self.registrar.isLiveEnvironment():
        #    return True
        # before we send the data, we need to add the "callback"
        # to a global handler list
        if group+"."+name in self.registrar.functionsCallbacks:
            # this is a double registration
            if self.registrar.pluginInstallationRunning:
                return False

        self.registrar.functionsCallbacks[group+"."+name] = registration_dict
        self.registrar.functionsCallbacks[group+"."+name]["process"] = process

        ## if this is a saimulator - we dont want to send that we can "work" with the live
        # plugins because its not relevant for the chart worker server and leads to misunderstandings
        if not self.registrar.shouldRegisterFunction():
            return False

        if self.functionsInterface is not None:
            self.functionsInterface.registerIndicatorFunction(registration, metadata=self.registrar.getAuthMetadata())
        
        return True

    
