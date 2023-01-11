import asyncio

import grpc

from coinlib.brokerWorker.BrokerWorker import BrokerWorker
from coinlib.config import grpc_chan_ops
from coinlib.feature.FeatureWorker import FeatureWorkerWrapper
from coinlib.helper import is_in_ipynb
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib.helper import get_current_kernel
from coolname import generate_slug
from coinlib.Registrar import Registrar
import time
import sys
from chipmunkdb.ChipmunkDb import ChipmunkDb

from coinlib.helper import pip_install_or_ignore
from coinlib.logics.LogicOfflineWorker import LogicOfflineWorker
from coinlib.logics.LogicOfflineWorkerData import LogicOfflineWorkerData
from coinlib.logics.LogicOfflineWorkerScreener import LogicOfflineWorkerScreener
from coinlib.logics.LogicOfflineWorkerTrader import LogicOfflineWorkerTrader
from coinlib.logics.LogicOnlineDataWorker import LogicOnlineDataWorker
from coinlib.logics.LogicOnlineScreenerWorker import LogicOnlineScreenerWorker
from coinlib.logics.LogicOnlineTraderWorker import LogicOnlineTraderWorker
from coinlib.logics.LogicOnlineWorker import LogicOnlineWorker
from coinlib.logics.LogicTestBrokerWorker import LogicTestBrokerWorker
from coinlib.notification.NotificationWorker import NotificationWorker
from coinlib.symbols.SymbolWorker import SymbolWorkerFetchHistoricalData, SymbolWorkerBrokerInfo, \
    SymbolWorkerConsumeMarketData

pip_install_or_ignore("semver", "semver", "2.13.0")

import os

from coinlib.statistics import StatisticsMethodWorker, StatisticsRuleWorker
from coinlib import ChartsWorker
from coinlib import PluginsWorker

import threading
import queue

import semver
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel


class WorkerJobListener:
    channel = None
    def __init__(self, simulator=False):
        self.listenThread = None
        self.registrar = Registrar()
        self.waitingQueue = None
        self.workerSettings = None
        self.serverPlugins = None
        self.stopped = True
        self.simulator = simulator
        self.workerRegistered = False
        self._restart_timer = None
        self.workerList = []

        file_name = os.path.basename(sys.argv[0]) + "-".join(self.registrar.worker_modules)
        if os.getenv("WORKERNAME") is not None:
            file_name = os.getenv("WORKERNAME")
            self.workerId = file_name
        else:
            fixed_worker_file = "."+file_name+".pid"
            if not is_in_ipynb:
                if os.path.exists(fixed_worker_file):
                    with open(fixed_worker_file, 'r') as file:
                        self.workerId = file.read()
                else:
                    self.workerId = self.generate_worker_id()
                    f = open(fixed_worker_file, "a")
                    f.write(self.workerId)
                    f.close()
            else:
                self.workerId = self.generate_worker_id()

        self.registrar.worker_id = self.workerId
        self.createWorker()

        return None

    def createWorker(self):

        availablePlugins = []
        try:
            all_plugins = self.getAllPluginsAvailable()
            for p in all_plugins:
                availablePlugins.append(statsModel.WorkerAvailablePlugins(name=p["name"], version=p["version"], type=p["module"]))
        except Exception as e:
            pass

        worker_modules = self.registrar.worker_modules
        if self.registrar.fixed_modules is not None:
            worker_modules = self.registrar.fixed_modules
        self.worker = statsModel.Worker(workerId=self.workerId,
                                        activeModules=worker_modules,
                                        availablePlugins=availablePlugins,
                                        workspaceId=self.registrar.workspaceId,
                                        environment=self.registrar.environment)

    def registerWorker(self):
        self.createWorker()
        self.registrar.connected = True
        self.workerSettings = self.stub.RegisterWorker(self.worker, metadata=self.registrar.getAuthMetadata())
        self.updateWorkerSettings(self.workerSettings)


    def createRegistryChannnel(self):
        registry = "localhost"
        if os.getenv("REGISTRY") is not None:
            registry = os.getenv("REGISTRY")
        if self.registrar.coinlib_fixed_backend:
            host = "registry."+self.registrar.coinlib_backend
        else:
            if ":" not in registry:
                host = registry+":9555"
            else:
                host = registry
            if is_in_ipynb:
                host = os.environ["COINLIB_WB"]+":9555"
        return grpc.insecure_channel(host, options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def createChannel(self):
        if self.registrar.coinlib_fixed_backend:
            if self.registrar.workerEndpoint == "localhost":
                endpoint = self.registrar.workerEndpoint + ":"+ self.registrar.workerEndpointPort
            else:
                port = self.registrar.workerEndpointPort
                if self.registrar.api_key_port is not None:
                    port = self.registrar.api_key_port
                endpoint = self.registrar.workerEndpoint+"."+self.registrar.coinlib_backend_host+":"+ port
        else:
            endpoint = self.registrar.workerEndpoint + ":" + self.registrar.workerEndpointPort

        return grpc.insecure_channel(endpoint, options=grpc_chan_ops,

                                     compression=grpc.Compression.Gzip)

    def getChannel(self):
        return self.channel

    def onWorkerJobProcessError(self, workerJobProcess, err):
        try:
            self.workerList.remove(workerJobProcess)
        except Exception as e:
            pass
        self.registrar.logger.info("Errored " + str(err))
        self.registrar.logger.info("Errored Worker: " + str(workerJobProcess.workerJob))
        self.registrar.logger.info("Now worker running: " + str(len(self.workerList)))
        workerError = statsModel.WorkerJobError()
        workerError.workerJobId = workerJobProcess.workerJob.workerJobId
        workerError.errorMessage = str(err)
        workerError.workerJobType = workerJobProcess.workerJob.workerJobType
        self.stub.ErroredWorkerJob(workerError, metadata=self.registrar.getAuthMetadata())

    def onWorkerJobProcessFinished(self, workerJobProcess):
        try:
            self.workerList.remove(workerJobProcess)
        except Exception as e:
            pass
        self.registrar.logger.info("Finished Worker: " + str(workerJobProcess.workerJob))
        self.registrar.logger.info("Now worker running: " + str(len(self.workerList)))
        self.stub.FinishedWorkerJob(workerJobProcess.workerJob, metadata=self.registrar.getAuthMetadata())

    def generate_worker_id(self):
        if is_in_ipynb:
            return get_current_kernel()
        return self.get_random_string()

    def get_random_string(self, length=3):
        return generate_slug(length)

    def stop(self):
        self.stopped = True
        self.waitingQueue.put(None)

    def canWorkOnJob(self, job):
        return True

    def onJobStarted(self):
        pass

    def installPlugin(self, plugin):
        pluginWorker = PluginsWorker.PluginsWorker(None, self)
        pluginWorker.installPlugin(plugin)

    def checkIfPluginShouldInstall(self, pluginConfig):
        module_directory = ".chart_modules"
        if pluginConfig.type == "chart":
            module_directory = ".chart_modules"
        if pluginConfig.type == "notification":
            module_directory = ".notification_modules"
        elif pluginConfig.type == "stats":
            module_directory = ".statsrules_modules"
        elif pluginConfig.type == "symbols":
            module_directory = ".symbolbroker_modules"
        elif pluginConfig.type == "statsMethod":
            module_directory = ".statsmethod_modules"
        elif pluginConfig.type.endswith("Logics"):
            module_directory = ".logic_modules"
        elif pluginConfig.type == "symbolBroker":
            module_directory = ".symbolbroker_modules"
        elif pluginConfig.type == "broker":
            module_directory = ".broker_modules"
        elif pluginConfig.type == "features" or pluginConfig.type == "feature":
            module_directory = ".feature_modules"

        if not os.path.exists(module_directory):
            os.makedirs(module_directory)

        file_name = None
        version = "?"
        for file_name in os.listdir("./"+module_directory):
            try:
                if file_name.startswith(pluginConfig.name):
                    version = os.path.splitext(file_name)[0].split("_")[1]
                    version = version.replace("-", ".")
                    if semver.compare(pluginConfig.version, version) == 0:
                        return False
                    break
            except Exception as e:
                pass

        if file_name is not None:
            self.registrar.logger.info("New Version for "+file_name+" => old: "+version+" new: "+pluginConfig.version)
        return True

    def getAllPluginsAvailable(self):

        plugins = []
        for module_directory in os.listdir("./"):
            if module_directory.startswith(".") and module_directory.endswith("_modules"):
                for file_name in os.listdir("./" + module_directory):
                    if file_name.endswith(".py"):
                        version = os.path.splitext(file_name)[0].split("_")[1]
                        plugin_name = os.path.splitext(file_name)[0].replace("_"+version, "")
                        version = version.replace("-", ".")
                        plugins.append({
                            "module": module_directory,
                            "name": plugin_name,
                            "file": file_name,
                            "file_path": "./"+module_directory+"/"+file_name,
                            "version": version
                        })

        return plugins

    def getDirectoryForPluginType(self, type):
        if type == "stats":
            return ".statsrules_modules"
        if type == "statsMethod":
            return ".statsmethod_modules"
        if type == "symbols":
            return ".symbolbroker_modules"
        if type == "broker":
            return ".broker_modules"
        if type == "notification":
            return ".notification_modules"
        if type == "chart":
            return ".chart_modules"
        if type == "symbolBroker":
            return ".symbolbroker_modules"
        if type == "features" or type == "feature":
            return ".feature_modules"
        if type.endswith("Logics"):
            return ".logic_modules"
        return None

    def downloadAllPlugins(self):
        try:
            ##  we dont do this when not in live environment
            #if not self.registrar.isLiveEnvironment():
            #    return False

            self.registrar.pluginInstallationRunning = True
            newPluginsFound = False
            self.serverPlugins = self.stub.GetAllPlugins(self.worker, metadata=self.registrar.getAuthMetadata())

            foundPlugins = []
            for p in self.serverPlugins.plugin:
                try:
                    foundPlugins.append(p)
                    if self.checkIfPluginShouldInstall(p):
                        self.installPlugin(p)
                        newPluginsFound = True
                except Exception as e:
                    self.registrar.logger.error("Error installing Plugin "+p.name, e)
                    pass

            ## remove all
            availablePlugins = self.getAllPluginsAvailable()

            for p in availablePlugins:
                found = False
                for p2 in foundPlugins:
                    dirName = self.getDirectoryForPluginType(p2.type)
                    if p["name"].lower() == p2.name.lower() and dirName == p["module"]:
                        found = True

                if found == False:
                    ## delete the plugin
                    #self.deletePlugin(p["file_path"])
                    self.registrar.logger.info("Deleting Plugin "+p["name"])
        except Exception as e:
            self.registrar.logger.error("Error in download Plugins", e)
        finally:
            self.registrar.pluginInstallationRunning = False
        return newPluginsFound

    def deletePlugin(self, full_path):
        return os.remove(full_path)

    def wait_for_jobs(self):

        try:
            self.registerWorker()
            #if self.registrar.isLiveEnvironment():
            newPlugins = self.downloadAllPlugins()
            if newPlugins:
                self.registerWorker()

            self.workerRegistered = True

            self.workerStream = self.stub.WatchWorkerJobs(iter(self.waitingQueue.get, None))
            m = statsModel.WorkerRegistration()
            m.worker_id = self.workerId
            self.waitingQueue.put(m)

            for job in self.workerStream:
                if (self.canWorkOnJob(job)):
                    self.acceptJob(job)
                else:
                    self.declineJob(job)

        except Exception as e:
            print("Can not connect to the server"+str(e))
            self.onErrorHappenedInCommunication(e)

    def onErrorHappenedInCommunication(self, e):
        if self._restart_timer is None:
            self._restart_timer = threading.Timer(5, self.restart)
            self._restart_timer.start()

    def declineJob(self, job):
        self.stub.DeclineWorkerJob(job, metadata=self.registrar.getAuthMetadata())

    def acceptJob(self, job):
        self.stub.AcceptWorkerJob(job, metadata=self.registrar.getAuthMetadata())
        workerStartingThread = threading.Thread(target=self.startWorkerProcess, args=[job], daemon=True)
        workerStartingThread.start()


    def getDataWorkerEndpoint(self):
        res = statsModel.WorkerRegistryResponse()
        try:
            workerRequest = statsModel.WorkerRegistryRequest()
            workerRequest.worker_id = self.registrar.worker_id
            for m in self.registrar.worker_modules:
                workerRequest.activeModules.append(m)

            channel = self.createRegistryChannnel()
            self.registryStub = stats.DataWorkerRegistryStub(channel)
            res = self.registryStub.getDataWorkerServerEndpoint(workerRequest, metadata=self.registrar.getAuthMetadata())
            self.registrar.workerEndpoint = res.targetendpoint
            self.registrar.workerEndpointPort = res.targetport
            self.registrar.logger.info("Found Worker Server "+res.targetendpoint+":"+res.targetport)
        except Exception as e:
            self.registrar.logger.error("Can not connect to registry, i will retry %s", str(e))
            raise e

    def connect(self):
        try:
            if self.channel is not None:
                try:
                    self.channel.close()
                except Exception as e:
                    pass

            self.getDataWorkerEndpoint()
            self.channel = self.createChannel()
            self.stub = stats.DataWorkerStub(self.channel)

        except Exception as e:
            self.onErrorHappenedInCommunication(e)

    def getWorkerBulkJobData(self, chartData):
        start = time.time()
        self.chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(chartData.chipmunkdbHost))
        df = self.chipmunkDb.collection_as_pandas_additional(chartData.workspace_id, additionalCollections=[chartData.workspace_id+"_"+chartData.activity_id] ,columns=[])
        end = time.time()
        self.registrar.logger.info("Downloading DataFrame from chipmunk %d", end - start)

        return df

    def runBulkProcesses(self, workerJob):
        # lets download
        statisticInterface = stats.StatisticsMethodWorkerStub(self.getChannel())
        statisticConfig = statisticInterface.GetConfig(workerJob, metadata=self.registrar.getAuthMetadata())

        # download
        dataFrame = self.getWorkerBulkJobData(statisticConfig.chartData)

        for workerJobChildConfig in statisticConfig.configs:
            try:
                workerJobChild = None
                if workerJobChildConfig.HasField("rule"):
                    workerJobChild = StatisticsRuleWorker.StatisticsRuleWorker(workerJob, self)
                    workerJobChild.setConfig(workerJobChildConfig.rule)
                else:
                    workerJobChild = StatisticsMethodWorker.StatisticsMethodWorker(workerJob, self)
                    workerJobChild.setConfig(workerJobChildConfig.methodWindow)

                if workerJobChild is not None:
                    workerJobChild.startProcessWithDataFrame(dataFrame.copy())

            except Exception as e:
                self.registrar.logger.error("Data %s", str(e))
                pass


        return None

    def reRegisterWorker(self):
        self.connect()
        self.registerWorker()

    def updateWorkerSettings(self, settings: statsModel.WorkerSettings):

        activeModules = settings.activeModules

        for mod in activeModules:
            try:
                if mod == "chart":
                    self.registrar.functions.connect()
                    self.registrar.chartsFactory.loadPlugins()
                elif mod == "data":
                    self.registrar.data.connect()
                elif mod == "statsMethod":
                    self.registrar.statistics.connect()
                    self.registrar.statsMethodFactory.loadPlugins()
                elif mod == "broker":
                    self.registrar.broker.connect()
                    if self.registrar.isLiveEnvironment():
                        self.registrar.brokerFactory.loadPlugins()
                elif mod == "stats":
                    self.registrar.statistics.connect()
                    self.registrar.statsRuleFactory.loadPlugins()
                elif mod == "onlineLogics":
                    self.registrar.logic.connect()
                    self.registrar.logicFactory.loadPlugins()
                    self.registrar.logicFactory.loadChildModules(mod)
                elif mod.endswith("Logics"):
                    self.registrar.logic.connect()
                    self.registrar.logicFactory.loadPlugins()
                elif mod == "symbolBroker":
                    self.registrar.symbols.connect()
                    if self.registrar.isLiveEnvironment():
                        self.registrar.symbolFactory.loadPlugins()
                elif mod == "notification":
                    self.registrar.notifications.connect()
                    self.registrar.notificationFactory.loadPlugins()
                elif mod == "broker":
                    self.registrar.brokers.connect()
                    self.registrar.brokerFactory.loadPlugins()
                elif mod == "features" or mod == "feature":
                    self.registrar.features.connect()
                    self.registrar.featureFactory.loadPlugins()
                elif mod == "featureSaver":
                    self.registrar.featureSaverServer.start()
            except Exception as e:
                self.registrar.logger.error("Error loading module "+mod+", %s", e)

        return None

    def generateWorkerProcess(self, workerJob):

       try:
           workerJobProcess = None
           # instantiate a new channel and stub so that the requests are parallel
           if workerJob.workerJobType == "stats":
               workerJobProcess = StatisticsRuleWorker.StatisticsRuleWorker(workerJob, self)
           elif workerJob.workerJobType == "statsMethod":
               workerJobProcess = StatisticsMethodWorker.StatisticsMethodWorker(workerJob, self)
           elif workerJob.workerJobType == "charts":
               workerJobProcess = ChartsWorker.ChartsWorker(workerJob, self)
           elif workerJob.workerJobType == "plugin":
               workerJobProcess = PluginsWorker.PluginsWorker(workerJob, self)
           elif workerJob.workerJobType == "fetchHistoricalData":
               workerJobProcess = SymbolWorkerFetchHistoricalData(workerJob, self)
           elif workerJob.workerJobType == "symbolBrokerInfo":
               workerJobProcess = SymbolWorkerBrokerInfo(workerJob, self)
           elif workerJob.workerJobType == "consumeMarketData":
               workerJobProcess = SymbolWorkerConsumeMarketData(workerJob, self)
           elif workerJob.workerJobType == "runLogicOffline_trader":
               workerJobProcess = LogicOfflineWorkerTrader(workerJob, self)
           elif workerJob.workerJobType == "runLogicOffline_screener":
               workerJobProcess = LogicOfflineWorkerScreener(workerJob, self)
           elif workerJob.workerJobType == "runLogicOffline_logic":
               workerJobProcess = LogicOfflineWorkerData(workerJob, self)
           elif workerJob.workerJobType == "runLogicOffline_data":
               workerJobProcess = LogicOfflineWorkerData(workerJob, self)
           elif workerJob.workerJobType == "startBrokerSession":
               workerJobProcess = BrokerWorker(workerJob, self)
           elif workerJob.workerJobType == "testBrokerModule":
               workerJobProcess = LogicTestBrokerWorker(workerJob, self)
           elif workerJob.workerJobType == "startTraderSession":
               workerJobProcess = LogicOnlineTraderWorker(workerJob, self)
           elif workerJob.workerJobType == "startLogicSession":
               workerJobProcess = LogicOnlineDataWorker(workerJob, self)
           elif workerJob.workerJobType == "startScreenerSession":
               workerJobProcess = LogicOnlineScreenerWorker(workerJob, self)
           elif workerJob.workerJobType == "startFeature":
               workerJobProcess = FeatureWorkerWrapper(workerJob, self)
           elif workerJob.workerJobType == "sendNotification":
               workerJobProcess = NotificationWorker(workerJob, self)
           elif workerJob.workerJobType == "extractMessageCallback":
               workerJobProcess = NotificationWorker(workerJob, self)
           elif workerJob.workerJobType == "forcePluginUpdates":
               self.reloadAllPlugins()
           elif workerJob.workerJobType == "workerSettings":
               self.reRegisterWorker()
           else:
               self.registrar.logger.error("Unknown Worker Type received")
               return workerJobProcess
       except Exception as e:
           self.registrar.logger.error("Erorr in creating worker"+", %s", e)
           pass

       return workerJobProcess


    def startWorkerProcess(self, workerJob):
        try:
            workerJobProcess = None

            if workerJob.workerJobType == "statsBulked":
                return self.runBulkProcesses(workerJob)
            else:
                workerJobProcess = self.generateWorkerProcess(workerJob)

            self.workerList.append(workerJobProcess)
            self.registrar.logger.info("Now worker running: " + str(len(self.workerList)))

            workerJobProcess.startProcess()
            return workerJobProcess
        except Exception as e:
            self.registrar.logger.error(e)
            pass

    def reloadAllPlugins(self):

        for mod in self.workerSettings.activeModules:
            try:
                self.reloadPluginsForType(mod)
            except Exception as e:
                pass
        return True

    def loadSpecificPlugin(self, mod, plugin):

        if mod == "chart":
            return self.registrar.chartsFactory.loadPluginForTest(mod, plugin)
        if mod == "statsMethod":
            return self.registrar.statsMethodFactory.loadPluginForTest(mod, plugin)
        if mod == "stats":
            return self.registrar.statsRuleFactory.loadPluginForTest(mod, plugin)
        if mod.endswith("Logics") or mod == "logic":
            return self.registrar.logicFactory.loadPluginForTest(mod, plugin)
        if mod == "features" or mod == "feature":
            return self.registrar.featureFactory.loadPluginForTest(mod, plugin)
        if mod == "notification":
            return self.registrar.notificationFactory.loadPluginForTest(mod, plugin)
        if mod == "broker":
            return self.registrar.brokerFactory.loadPluginForTest(mod, plugin)
        if mod == "symbols" or mod == "symbolBroker":
            return self.registrar.symbolFactory.loadPluginForTest(mod, plugin)
        if mod == "orderBroker" or mod == "broker":
            return self.registrar.brokerFactory.loadPluginForTest(mod, plugin)

        return False

    def reloadPluginsForType(self, mod):

        if mod == "chart":
            self.registrar.chartsFactory.reloadPlugins()
        if mod == "statsMethod":
            self.registrar.statsMethodFactory.reloadPlugins()
        if mod == "stats":
            self.registrar.statsRuleFactory.reloadPlugins()
        if mod.endswith("Logics") or mod == "logic":
            self.registrar.logicFactory.reloadPlugins()
        if mod == "features" or mod == "feature":
            self.registrar.featureFactory.reloadPlugins()
        if mod == "notification":
            self.registrar.notificationFactory.reloadPlugins()
        if mod == "broker":
            self.registrar.brokerFactory.reloadPlugins()
        if mod == "symbols" or mod == "symbolBroker":
            self.registrar.symbolFactory.reloadPlugins()
        if mod == "orderBroker" or mod == "broker":
            self.registrar.brokerFactory.reloadPlugins()

        return True

    def restart(self):
        self._restart_timer = None
        if (self.stopped == False):
            self.connect()

            if (self.waitingQueue != None):
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()

            self.listenThread = threading.Thread(target=self.wait_for_jobs, daemon=True)
            self.listenThread.start()

    async def lockMethodUntilCallback(self):
        while True:
            if self.workerRegistered:
                return True

            await asyncio.sleep(0.1)
        return False

    def waitUntilWorkerRegistered(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.lockMethodUntilCallback())

    def start(self):
        if (self.stopped == False):
            self.stop()
        self.stopped = False
        self.connect()
        self.restart()
        self.waitUntilWorkerRegistered()


