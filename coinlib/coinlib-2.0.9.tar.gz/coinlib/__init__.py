import datetime

from coinlib.CoinlibCrypto import getCoinlibInfoFroMkey
from coinlib.helper import in_ipynb
from coinlib.helper import pip_install_or_ignore, system_install_or_ignore
import asyncio

pip_install_or_ignore("ipynb_path", "ipynb-path", "0.1.4")
# pip_install_or_ignore("import_ipynb", "import_ipynb")
pip_install_or_ignore("websocket", "websocket-client", "0.58.0")
pip_install_or_ignore("plotly", "plotly", "4.14.3")
pip_install_or_ignore("simplejson", "simplejson", "3.17.2")
pip_install_or_ignore("aio_pika", "aio_pika", "6.8.0")
pip_install_or_ignore("grpc", "grpcio-tools", "1.35.0")
pip_install_or_ignore("matplotlib", "matplotlib", "3.3.4")
pip_install_or_ignore("pandas", "pandas", "1.2.4")
#pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil", "2.8.1")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client", "2.0.1")

global coinlib_job_task

from coinlib.feature import Features
from coinlib.Registrar import Registrar
from coinlib.logics.Logic import Logic
from coinlib.Functions import Functions
from coinlib.CoinlibDataInterface import CoinlibDataInterface
from coinlib.statistics.Statistics import Statistics
from coinlib.Simulator import Simulator
from coinlib.ChartsIndicatorJob import ChartsIndicatorJob
from coinlib.broker.Broker import Broker
from coinlib.notification.Notification import Notification
from coinlib.symbols.Symbols import Symbols
from coinlib.helper import trendline, to_trendline

registrar = Registrar()

if registrar.features is None:
    registrar.features = Features.Features()
    registrar.logic = Logic()
    registrar.functions = Functions()
    registrar.statistics = Statistics()
    registrar.simulator = Simulator()
    registrar.symbols = Symbols()
    registrar.data = CoinlibDataInterface()
    registrar.notifications = Notification()
    registrar.broker = Broker()


features = registrar.features
logic = registrar.logic
functions = registrar.functions
data = registrar.data
notifications = registrar.notifications
symbols = registrar.symbols
log=registrar.logger
statistics = registrar.statistics
simulator = registrar.simulator
broker = registrar.broker
pip_install_or_ignore = pip_install_or_ignore
system_install_or_ignore = system_install_or_ignore


def registerToWorkspace(workspaceId):
    registrar.workspaceId = workspaceId

def addLogicToWorkspace(identifier, type, logicComponentId, params=None, workspaceId=registrar.workspaceId, autostart=False):
    return logic.addLogicToWorkspace(identifier,
                                     type,
                                     logicComponentId,
                                     params, workspaceId, autostart)

def connectAsLogic(apiKey=None, apiKeySecret=None, workspaceId=None):
    logicModule = "offlineLogics"
    if registrar.isLiveEnvironment():
        logicModule = "onlineLogics"
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=workspaceId, worker_modules=[logicModule])

def connectAsBrokerSymbol(apiKey=None, apiKeySecret=None, workspaceId=None):
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=workspaceId, worker_modules=["symbolBroker"])

def connectAsBroker(apiKey=None, apiKeySecret=None, workspaceId=None):
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=workspaceId, worker_modules=["broker"])

def connectAsFeature(apiKey=None, apiKeySecret=None, ):
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=None, worker_modules=["features"])

def connectAsStatistic(apiKey=None, apiKeySecret=None, ):
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=None, worker_modules=["stats"])

def connectAsStatisticMethod(apiKey=None, apiKeySecret=None, ):
    return connectCoinlib(apiKey, apiKeySecret, workspaceId=None, worker_modules=["stats"])

def connectCoinlib(apiKey=None, apiKeySecret=None, workspaceId=None,
                   worker_modules=["chart", "stats", "data", "statsMethod", "spreadsheet", "notification"],
                   reconnect=False):
    if registrar.connected and not reconnect:
        return

    if apiKey is not None:
        extract = getCoinlibInfoFroMkey(apiKey, apiKeySecret)
        hostname = extract["hostname"]+":"+extract["port"]
        registrar.api_key_hostname = hostname
        registrar.api_key_port = extract["port"]
        registrar.api_key_id = extract["apikey"]
    else:
        hostname = None

    if hostname is not None or not registrar.hasEnvironment() or registrar.environment == "dev":
        if hostname is not None:
            registrar.setBackendPath(hostname)
        registrar.setEnvironment("dev")
        registrar.fixed_modules = worker_modules
        registrar.worker_modules = worker_modules
        registrar.workspaceId = workspaceId

    registrar.connected = True
    registrar.simulator.connect()


def set_loglevel(level):
    ##registrar.logger.set_loglevel(level)
    pass

def runAfterStart():
    if registrar.isLiveEnvironment():
        return False

    registrar.logic.runLogic()

def waitForJobs():

    # register as a worker if not already done
    # check if plugin and then ignore this
    if registrar.currentPluginLoading is None:

        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        finally:
            loop.close()

to_trendline = to_trendline
trendline = trendline

set_loglevel("INFO")