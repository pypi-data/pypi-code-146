import logging
import os

import grpc

from coinlib.ChartsFactory import ChartsFactory
from coinlib.brokerWorker.BrokerFactory import BrokerFactory
from coinlib.config import grpc_chan_ops
from coinlib.feature.FeatureFactory import FeatureFactory
from coinlib.logics.LogicLoader import LogicFactory
from coinlib.notification import NotificationFactory
from coinlib.statistics.StatisticsMethodFactory import StatisticsMethodFactory
from coinlib.statistics.StatisticsRuleFactory import StatisticsRuleFactory
from coinlib.symbols import SymbolFactory
from coinlib.helper import is_in_ipynb
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats


class Registrar(object):
    _instance = None
    functionsCallbacks = {}
    statisticsCallbacks = {}
    logicCallbacks = {}
    logicDataRegistration = {}
    featureCallbacks = {}
    symbolBrokerCallbacks = {}
    logger = logging
    logicCollectionRegistration = {}
    logicEventRegistration = {}
    coinlib_backend_host = None
    coinlib_backend = None
    brokerCallbacks = {}
    logicEventCallback = {}
    notificationCallbacks = {}
    symbolFactory: SymbolFactory = None
    brokerFactory: BrokerFactory = None
    auth_metadata = [( "authorization", "")]
    auth_key_valid_until = None
    currentPluginLoading = None
    notificationFactory: NotificationFactory = None
    chartsFactory: ChartsFactory = None
    featureFactory: FeatureFactory = None
    workerEndpoint = None
    workerEndpointPort = None
    statsRuleFactory: StatisticsRuleFactory = None
    logicFactory: LogicFactory = None
    api_key_id = None
    workspaceId = None
    environment = None
    statsMethodFactory: StatisticsMethodFactory = None
    worker_modules = []
    connected = False
    initialization_running = True
    pluginInstallationRunning = False
    isRegistered = False
    iframe_host = None
    worker_id = None

    coinlib_fixed_backend = False
    ##chipmunkdb = "localhost"

    notifications = None
    simulator = None
    statistics = None
    logic = None
    brokers = None
    collectionInterfaceList = {}
    data = None
    functions = None
    features = None
    featureSaverServer = None
    fixed_modules = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Registrar, cls).__new__(cls)
            cls._instance.initFirstTime()
            # Put any initialization here.

        return cls._instance

    def isAuthKeyValid(self):
        if self.auth_key_valid_until is not None:
            return True
        return False

    def shouldRegisterFunction(self):
        return self.isLiveEnvironment() or (not self.isLiveEnvironment() and not self.initialization_running)

    def initFirstTime(self):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()
        return True

    def hasEnvironment(self):
        return self.environment is not None

    def setEnvironment(self, env):
        if self.environment is not None and env != self.environment:
            self.logger.error("You are trying to change the environment - thats probably an error - we have not handled that!")
            return False
        self.environment = env

    def isLiveEnvironment(self):
        return self.environment == "live"

    def createRegistryChannnel(self):
        registry = "localhost"
        if os.getenv("REGISTRY") is not None:
            registry = os.getenv("REGISTRY")
        if self.coinlib_fixed_backend:
            host = "registry."+self.coinlib_backend
        else:
            if ":" not in registry:
                host = registry+":9555"
            else:
                host = registry
        return grpc.insecure_channel(host, options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def generateAuthKey(self):
        if self.api_key_id is not None:
            channel = self.createRegistryChannnel()
            registryStub = stats.DataWorkerRegistryStub(channel)
            wd = statsModel.ApiKey()
            wd.api_key_id = self.api_key_id
            wd.modules = ",".join(self.worker_modules)
            auth_key = registryStub.getAuthKey(wd)
            self.setAuthKey(auth_key.auth_key, auth_key.valid_until)
            channel.close()

    def getAuthMetadata(self):
        if not self.isAuthKeyValid():
            self.generateAuthKey()
        return self.auth_metadata

    def setAuthKey(self, auth_key, valid_until):
        self.auth_metadata = [("authorization", auth_key)]
        self.auth_key_valid_until = valid_until
    
    def setBackendPath(self, path):
        if ":" not in path:
            self.iframe_host = path + ":3000"
            self.coinlib_backend = path + ":" + str(self.get_port())
            self.coinlib_backend_host = path
        else:
            self.coinlib_backend = path
            self.coinlib_backend_host = path.split(':', 1)[0]
        self.coinlib_fixed_backend = True
            # self.chipmunkdb = path

    def get_chipmunkdb_host(self, host: str):
        if self.coinlib_fixed_backend:
            return host+"."+self.coinlib_backend_host
        return host

    def get_port(self):
        return self.workerEndpointPort

    def set_coinlib_backend(self, endpoint):
        self.workerEndpoint = endpoint
        self.coinlib_backend = endpoint
        self.iframe_host = endpoint + ":3000"

    # IP address
    def get_coinlib_backend(self):
        return self.workerEndpoint

    def get_coinlib_backend_chipmunk(self):
        return self.get_coinlib_backend()

    def get_coinlib_backend_grpc(self):
        if self.coinlib_fixed_backend:
            if self.workerEndpoint == "localhost":
                return self.get_coinlib_backend() + ":" + self.get_port()
            else:
                return self.workerEndpoint+"."+self.coinlib_backend
        return self.get_coinlib_backend() + ":" + self.get_port()
