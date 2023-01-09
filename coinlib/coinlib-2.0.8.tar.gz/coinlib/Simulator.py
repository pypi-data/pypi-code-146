import os
import sys
import inspect
from typing import TypedDict

from coinlib.broker.Broker import BrokerAssetType, BrokerContractType
from coinlib.brokerWorker.BrokerFactory import BrokerFactory
from coinlib.config import grpc_chan_ops
from coinlib.feature.FeatureFactory import FeatureFactory
from coinlib.logics.LogicLoader import LogicFactory
from coinlib.helper import get_current_kernel
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from grpc._cython.cygrpc import CompressionAlgorithm
from grpc._cython.cygrpc import CompressionLevel
import grpc
from coinlib.helper import in_ipynb
from coinlib.notification.NotificationFactory import NotificationFactory
from coinlib.statistics.StatisticsMethodFactory import StatisticsMethodFactory
from coinlib.ChartsFactory import ChartsFactory
from coinlib.statistics.StatisticsRuleFactory import StatisticsRuleFactory

from coinlib.Registrar import Registrar
import simplejson as json

from coinlib.DataWorker import WorkerJobListener
from coinlib.symbols.SymbolFactory import SymbolFactory

class BrokerLoginInfo(TypedDict):
    apikey: str
    secret: str

class BrokerTestLoginData(TypedDict):
    exchange_id: str
    paperMode: bool
    loginInfo: BrokerLoginInfo
    assetType: BrokerAssetType
    contractType: BrokerContractType


class Simulator:
    def __init__(self):
        self._isConnected = False
        self._registrar = Registrar()
        self.workerJobs = None

        return None

    def connectSimulator(self):
        if self.__isLiveStage() == False:
            self.channel = self.__createChannel()
            self.stub = stats.SimulatorStub(self.channel)

    def connect(self):
        self._isConnected = True
        if not self._registrar.isRegistered:
            self.__registerAsWorker()

    def __isPluginFile(self):
        if self._registrar.currentPluginLoading is not None:
            callstack = inspect.stack()
            for call in callstack:
                if self._registrar.currentPluginLoading in call.filename:
                    return True
        return False

    def __canNotUseSimulatorInCurrentFile(self):
        return self.__isLiveStage() or self.__isPluginFile()

    def __isLiveStage(self):
        return self._registrar.isLiveEnvironment()

    def __registerAsWorker(self):
        if self.__canNotUseSimulatorInCurrentFile():
            return False
        if not self._registrar.isRegistered:
            self._registrar.isRegistered = True

            self._registrar.statsRuleFactory = StatisticsRuleFactory()
            self._registrar.statsMethodFactory = StatisticsMethodFactory()
            self._registrar.chartsFactory = ChartsFactory()
            self._registrar.logicFactory = LogicFactory()
            self._registrar.brokerFactory = BrokerFactory()
            self._registrar.symbolFactory = SymbolFactory()
            self._registrar.featureFactory = FeatureFactory()
            self._registrar.notificationFactory = NotificationFactory()

            self.workerJobs = WorkerJobListener(simulator=True)
            self.workerJobs.start()
            self._registrar.initialization_running = False

            if "offlineLogics" in self.workerJobs.workerSettings.activeModules:
                ### sometimes we want the functions inside the logics thats why we
                ### load all the plugins of the chartfactory
                self._registrar.chartsFactory.loadPlugins()

        return True

    def __createChannel(self):
        return grpc.insecure_channel(self._registrar.get_coinlib_backend_grpc(), options=grpc_chan_ops,
                                     compression=grpc.Compression.Gzip)

    def plot(self, plotly_fig):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerAsWorker()

        json = plotly_fig.to_json()

        iframe_src = 'http://' + self._registrar.iframe_host + '/simulator/plotly/' + get_current_kernel(
            self.workerJobs.workerId)
        if in_ipynb():

            self.__displayCoinChartFrame(iframe_src, iframe_width=str(1140), message='{type: "jupyter", plotly:'+json+', command: "reloadPlotlyChartData"}')


        return True

    def testBroker(self, broker_id: str, broker_login_data: BrokerTestLoginData):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerSimulator()

        self._registrar.logger.info("We are testing your symbol broker - but this can take 4-5 minutes - we´ll send you some infos when finished.");

        brokerInputs = statsModel.BrokerSimulatorRequest()
        brokerInputs.brokerId = broker_id
        brokerInputs.workerId = self._registrar.worker_id
        brokerInputs.paperMode = broker_login_data["paperMode"]

        brokerInfoData = statsModel.BrokerSimulatorBrokerData()
        brokerInfoData.exchange_id = broker_login_data["exchange_id"]

        brokerInfoData.assetType = "COIN"
        if "assetType" in broker_login_data:
            if broker_login_data["assetType"] == BrokerAssetType.COIN:
                brokerInfoData.assetType = "COIN"
            if broker_login_data["assetType"] == BrokerAssetType.STOCK:
                brokerInfoData.assetType = "STOCK"
            if broker_login_data["assetType"] == BrokerAssetType.FOREX:
                brokerInfoData.assetType = "FOREX"

        brokerInfoData.contractType = "spot"
        if "contractType" in broker_login_data:
            if broker_login_data["contractType"] == BrokerContractType.FUTURE:
                brokerInfoData.contractType = "future"
            if broker_login_data["contractType"] == BrokerContractType.SPOT:
                brokerInfoData.contractType = "spot"
            if broker_login_data["contractType"] == BrokerContractType.MARGIN:
                brokerInfoData.contractType = "margin"
            if broker_login_data["contractType"] == BrokerContractType.OPTION:
                brokerInfoData.contractType = "option"

        brokerLoginInfo = statsModel.BrokerSimulatorBrokerLoginData()
        brokerLoginInfo.secret = broker_login_data["loginInfo"]["secret"]
        brokerLoginInfo.apikey = broker_login_data["loginInfo"]["apikey"]

        brokerInfoData.loginInfo.CopyFrom(brokerLoginInfo)

        brokerInputs.brokerInfo.CopyFrom(brokerInfoData)

        info = self.stub.simulateBroker(brokerInputs, metadata=self._registrar.getAuthMetadata())
        exit = False
        if info.success:
            self._registrar.logger.info("Your symbol Broker does work, read message after!")

            self._registrar.logger.info(info.simulatorResponseText+"\r\n")

            iframe_src = info.rootServerPath + '/simulator/broker/' + info.workspaceId + "/" + get_current_kernel(
                self.workerJobs.workerId) + "/" + info.sessionId + "/" + info.targetdepotId
            if in_ipynb():

                self.__displayCoinChartFrame(iframe_src,
                                             iframe_width=str(1140),
                                             messageData=str(json.dumps({"workspaceId": info.workspaceId},
                                                                        ignore_nan=True)))
            else:
                # we are in anything of?????
                # printing iframe:
                self._registrar.logger.info("Broker works - here is your Testframe: " + iframe_src)

        else:
            exit = True
            self._registrar.logger.error("ERROR! Your symbol Broker does not work, read message after!")
            self._registrar.logger.error(info.simulatorResponseText)


        return info

    def simulateFeature(self, identifier, options=None):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerSimulator()

        self._registrar.logger.info("We are testing your Feature Class. When finished we will report the data to you.")
        self._registrar.logger.info("  => Please beware: When you have a lake Feature - we will start it and then please trigger some data inputs. ")
        self._registrar.logger.info("  => This process will finish when any data is inserted into the data storage and we will return the info to you")

        notificationInputs = statsModel.FeatureSimulatorRequest()
        notificationInputs.identifier = identifier
        notificationInputs.workerId = self._registrar.worker_id
        notificationInputs.options = str(json.dumps(options, ignore_nan=True))

        info = self.stub.simulateFeature(notificationInputs, metadata=self._registrar.getAuthMetadata())
        exit = False
        if info.success:
            self._registrar.logger.info("Your Feature system works fine!!")
        else:
            exit = True
            self._registrar.logger.error("ERROR! Your Feature service does not work, read message after!")

        print(info.simulatorResponseText)

        return info

    def testNotification(self, identifier, channels, inputs):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerSimulator()

        self._registrar.logger.info("We are testing your Notification and sending two messages to it. Please click on the second one to finish the test")

        notificationInputs = statsModel.NotificationSimulatorRequest()
        notificationInputs.identifier = identifier
        notificationInputs.channels = str(json.dumps(channels, ignore_nan=True))
        notificationInputs.workerId = self._registrar.worker_id
        notificationInputs.inputs = str(json.dumps(inputs, ignore_nan=True))

        info = self.stub.simulateNotification(notificationInputs, metadata=self._registrar.getAuthMetadata())
        exit = False
        if info.success:
            self._registrar.logger.info("Your Notification system works fine!!")
        else:
            exit = True
            self._registrar.logger.error("ERROR! Your Notification service does not work, read message after!")

        self._registrar.logger.info(info.simulatorResponseText)

        return info



    def testSymbolBroker(self, symbolbroker_id, testSymbol1, testSymbol2, options):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerSimulator()

        self._registrar.logger.info("We are testing your symbol broker - but this can take 4-5 minutes - we´ll send you some infos when finished.");

        symbolBrokerInputs = statsModel.SymbolBrokerSimulatorRequest()
        symbolBrokerInputs.symbolBrokerId = symbolbroker_id
        symbolBrokerInputs.workerId = self._registrar.worker_id
        symbolBrokerInputs.testSymbol1 = testSymbol1
        symbolBrokerInputs.testSymbol2 = testSymbol2
        symbolBrokerInputs.options = str(json.dumps(options, ignore_nan=True))

        info = self.stub.simulateSymbolBroker(symbolBrokerInputs, metadata=self._registrar.getAuthMetadata())
        exit = False
        if info.success:
            self._registrar.logger.info("Your symbol Broker does work, read message after!")
        else:
            exit = True
            self._registrar.logger.error("ERROR! Your symbol Broker does not work, read message after!")

        self._registrar.logger.info(info.simulatorResponseText)

        return info

    def __registerSimulator(self):
        self.connectSimulator()

    def statsMethod(self, methods, name="simulatorDefaultWorkspace"):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self._registrar.worker_modules = ["stats"]
        self.__registerSimulator()

        simulatorChartConfig = statsModel.SimulatorMethodCallChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel(self.workerJobs.workerId)
        simulatorChartConfig.simulatorName = name
        simulatorChartConfig.workerId = self.workerJobs.workerId

        for method in methods:
            meth = statsModel.SimulatorMethodCall()
            meth.method = method["method"]
            meth.params = str(json.dumps(method["params"], ignore_nan=True))

            simulatorChartConfig.methods.append(meth)

        info = self.stub.simulateStatisticsMethod(simulatorChartConfig, metadata=self._registrar.getAuthMetadata())

        iframe_src = info.rootServerPath + '/simulator/statsMethod/' + info.workspaceId + "/" + get_current_kernel(self.workerJobs.workerId)
        if in_ipynb():


            self.__displayCoinChartFrame(iframe_src,
                                         iframe_width=str(1140),
                                         messageData=str(json.dumps({"methods": methods,
                                                                     "workspaceId": info.workspaceId}, ignore_nan=True)))
        else:
            # we are in anything of?????
            # printing iframe:
            self._registrar.logger.info("Your Testframe: "+iframe_src)

        return True

    def statsRule(self, name="simulatorDefaultWorkspace"):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self._registrar.worker_modules = ["stats"]
        self.__registerSimulator()

        simulatorChartConfig = statsModel.SimulatorStatisticChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel(self.workerJobs.workerId)
        simulatorChartConfig.simulatorName = name

        info = self.stub.simulateStatisticsRule(simulatorChartConfig, metadata=self._registrar.getAuthMetadata())
        iframe_src = info.rootServerPath + '/simulator/stats/' + info.workspaceId + "/" + get_current_kernel(self.workerJobs.workerId)
        if in_ipynb():

            self.__displayCoinChartFrame(iframe_src,
                                         messageData=str(json.dumps({"workspaceId": info.workspaceId}, ignore_nan=True)),
                                         iframe_width=str(1140))

        else:
            # we are in anything of?????
            # printing iframe:
            self._registrar.logger.info("Your Testframe: "+iframe_src)

        return True

    def __displayCoinChartFrame(self, iframe_src, iframe_width = str(980), iframe_height = str(360), messageData='', message=''):
        from IPython.display import Javascript
        from IPython.core.display import display
        postmessage = message
        if (messageData == ''):
            messageData = "{}"

        if message == "":
            postmessage = '{type: "jupyter", kernel_id: "'+get_current_kernel(self.workerJobs.workerId)+'", command: "reloadChartDataFromNotebook", data: '+messageData+'}'
        display(Javascript(' const currentNotebookPanel = document.querySelector(".jp-NotebookPanel:not(.p-mod-hidden)");'\
                           ' if (currentNotebookPanel.querySelector(".coinchartoutput") != null) '\
                           ' { '\
                           '    currentNotebookPanel.querySelector(".coinchartoutput").querySelector("iframe").contentWindow.postMessage('+postmessage+', "*"); '\
                           ' } '\
                           ' else '\
                           ' { '\
                           '    const elem = document.createElement("div"); '\
                           '    elem.innerHTML = "<iframe src=\'' + iframe_src + '\' border=0 width=\'' + iframe_width + '\' height=\'' + iframe_height + '\' />";'\
                           '    elem.style = "position: absolute;width:' + iframe_width + 'px;height:' + iframe_height + 'px;bottom: 0px;opacity: 0.9;z-index: 9999;"; '\
                           '    elem.className = "coinchartoutput";'\
                           '    currentNotebookPanel.appendChild(elem); '\
                           ' } '))

        return True

    def simulateChart(self, broker, symbol, timeframe, indicators):
        return self.chart(broker, symbol, timeframe, indicators)

    def chart(self, broker, symbol, timeframe, indicators):

        if self.__canNotUseSimulatorInCurrentFile():
            return False
        self.__registerSimulator()

        simulatorChartConfig = statsModel.SimulatorChartConfig()
        simulatorChartConfig.kernel_id = get_current_kernel(self.workerJobs.workerId)
        simulatorChartConfig.broker = broker
        simulatorChartConfig.symbol = symbol
        simulatorChartConfig.timeframe = timeframe
        simulatorChartConfig.workerId = self.workerJobs.workerId
        indilist = []
        for indi in indicators:
            indicator = statsModel.SimulatorChartConfigIndicator()
            indicator.feature = indi["feature"]
            indicator.subfeature = indi["subfeature"]
            if "chartIndex" in indi:
                indicator.chartIndex = indi["chartIndex"]

            for key in indi["inputs"]:
                indicator.inputs[key] = str(indi["inputs"][key])

            simulatorChartConfig.indicators.append(indicator)

        info = self.stub.simulateChart(simulatorChartConfig, metadata=self._registrar.getAuthMetadata())

        iframe_src = info.rootServerPath + '/simulator/chart/' + info.workspaceId + "/" + get_current_kernel(self.workerJobs.workerId)
        if in_ipynb():


            self.__displayCoinChartFrame(iframe_src,
                                         iframe_width=str(1140),
                                         messageData=str(json.dumps({
                                                                     "workspaceId": info.workspaceId}, ignore_nan=True)))
        else:
            # we are in anything of?????
            # printing iframe:
            self._registrar.logger.info("Your Testframe: "+iframe_src)

        return True