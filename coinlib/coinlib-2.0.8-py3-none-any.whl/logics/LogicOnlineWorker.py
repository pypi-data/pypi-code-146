import random
import string
import time
import traceback
from collections import namedtuple
from munch import munchify
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import pandas as pd
import inspect
import numpy as np
import pyarrow as pa

from coinlib import PluginsWorker
from coinlib.PluginLoader import PluginLoader
from coinlib.PluginsWorker import PluginConfigInfo
from coinlib.data.DataTable import DataTable
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.logics.LogicBasicWorker import LogicBasicWorker
from coinlib.logics.LogicOfflineJob import LogicOfflineJob

import queue
import datetime

from coinlib.logics.LogicOnlineJob import LogicOnlineJob
from coinlib.logics.broker.LogicBrokerInterface import LogicBrokerInterface
from coinlib.logics.manager.LogicManager import LogicManager, LogicCommandParams
from coinlib.logics.manager.PortfolioModel import PortfolioModel
from coinlib.logics.onlineManager.LogicOnlineJobBroker import LogicOnlineJobBroker


class CommandCallbackData:
    data = ""
    command: string
    module: string
    message: string

class NotificationInteractiveEvent:
    client_id: string
    callback_id: string
    data = ""

class LogicOnlineWorker(LogicBasicWorker):
    brokerInterface: LogicBrokerInterface
    commandCallbacks: {}

    def initialize(self):
        super().initialize()
        self.registrar = Registrar()
        self.command_running = False
        self.commandQueue = []
        self.commandCallbacks = {}
        self.logicInterface = stats.AppWorkerStub(self.getChannel())
        logicInfoFullData = self.logicInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata()).startSessionConfig
        self.logicConfig = logicInfoFullData.logicInfo
        self.logicInfoFull = logicInfoFullData
        self.portfolio = logicInfoFullData.portfolio
        self.brokerConfig = logicInfoFullData.brokerConfig
        self.canceled = False
        self.sessionId = logicInfoFullData.sessionId
        self.waitingQueue = None

        self.chartConfigData = self.logicConfig.chartData
        pass

    def setConfig(self, configuration):
        self.logicConfig = configuration
        pass

    def generateJob(self, table, logicComponentInfo, logic, inputs, manager):
        return LogicOnlineJob(table, logicComponentInfo, logic, inputs, manager, self)


    def onLogicRunnerError(self, job, error):

        statsError = statsModel.AppWorkerError()
        statsError.error.message = str(error)
        statsError.worker.CopyFrom(self.workerJob)

        self.logicInterface.OnAppWorkerErrorOccured(statsError, metadata=self.registrar.getAuthMetadata())

        return False

    def getLogicMethodConfiguration(self, element):
        return json.loads(str(element.indicatorConfig, 'ascii'))


    def unqueueCommand(self, command):
        self.commandQueue.remove(command)

    def queueCommand(self, command):
        self.commandQueue.append(command)

        if self.command_running == False:
            self.runNextCommand()



    def shutdown(self):
        self.canceled = True
        self.commandStream.cancel()
        super().stop()
        super().closeChannel()


    def sendCommandAnswer(self, command, answerData = None):
        try:
            answer = statsModel.AppWorkerCommandsAnswer()
            answer.sessionId = self.sessionId
            answer.commandId = command.commandId

            try:
                answer.answerData = json.dumps(answerData, default=LogicOnlineWorker.serialize)
            except Exception as e:
                pass
            self.logicInterface.SendCommandAnswer(answer, metadata=self.registrar.getAuthMetadata())
        except Exception as sendError:
            pass

        return True

    def convertParams(self, params: any, className: str):
        try:
            return munchify(params)
        except Exception as e:
            return None

    def onCommandReceived_Thread(self, command: statsModel.AppWorkerCommands):

        try:
            params = json.loads(command.commandParams)
            # at first check for internal commands
            if command.command == "exit":
                self.sendCommandAnswer(command)
                self.shutdown()
                return True
            elif command.command == "runLogic":
                commandParams = self.convertParams(params, "LogicCommandParams")
                answerData = self.runLogic(commandParams)
            elif command.command == "notificiation.onButtonPressed":
                notificationEvent = self.convertParams(params, "NotificationInteractiveEvent")
                self.onNotificationButtonPressed(notificationEvent)
            print(command.command)

            answerData = {}
            ##answerData = self.session.runCommand(command.command, params, command)

        except Exception as e:
            self.onCommandErrorHappened(str(e), command)
            self.unqueueCommand(command)
            self.runNextCommand()
            return False

        self.sendCommandAnswer(command, answerData)

        self.unqueueCommand(command)
        self.runNextCommand()

        pass

    def generateLocalJob(self):
        table = DataTable()
        table.from_df(self.dataFrame)

        manager = LogicManager("", self.logicConfig, self.logicConfig.brokerAccount, self.portfolio)
        self.currentManager = manager
        manager.setTable(table)
        manager.broker = LogicOnlineJobBroker(manager, self.brokerInterface)
        inputs = {}
        logicWithInfo = self.logicComponentsWithInfo[0]
        logic = logicWithInfo.logic
        logicComponentInfo = logicWithInfo.info

        logicJob = self.generateJob(table, logicComponentInfo, logic, inputs, manager)
        logicJob.setParameterTable(self.parameterTable)
        return logicJob

    def onNotificationButtonPressed(self, notificationEvent: NotificationInteractiveEvent):
        if notificationEvent.client_id in self.commandCallbacks:
            cba = self.commandCallbacks[notificationEvent.client_id]
            cba.cb(notificationEvent.callback_id, self.generateLocalJob())
            self.onLogicRunningFinished()
        pass

    def onBrokerErrorHappenedInCommunication(self, error):
        pass

    def onBrokerCommandReceived(self, command):
        pass

    def getDataFrameLogicsActivityName(self):
        return self.chartConfigData.workspace_id

    def extractPortfolio(self, params: LogicCommandParams):
        portfolioDTO = params.portfolio

        return PortfolioModel.from_live_logics_model(portfolioDTO)


    def runLogic(self, params):
        self.reloadDataFrame()

        table = DataTable()
        table.from_df(self.dataFrame)

        infoStorageRaw = self.dataFrame.loc[:, self.dataFrame.columns.str.contains('result.', case=False)].rename(columns = lambda x: x.replace('result.logics.', '')).to_dict(orient="index")
        infoStorage = {}
        for key in infoStorageRaw:
            infoStorage[key.strftime("%Y-%m-%d-%H:%M:%S")] = infoStorageRaw[key]

        if "portfolio" in params:
            self.portfolio = self.extractPortfolio(params)
        else:
            self.portfolio = None

        manager = LogicManager("", self.logicConfig, self.logicConfig.brokerAccount, self.portfolio, infoStorage)
        manager.setLogicParams(params)
        self.currentManager = manager
        manager.setTable(table)
        manager.broker = LogicOnlineJobBroker(manager, self.brokerInterface)

        self.runLogicComponents(table, manager)

        manager.onLogicStepFinished()

        if self.portfolio is not None:
            manager.savePortfolio()

        self.extractLogicInfosFromManagerData(manager.getStorageIndexed())

        self.onLogicRunningFinished()

        return True

    def onLogicRunningFinished(self):
        super().onLogicRunningFinished()

        message = statsModel.AppWorkerFinishedStepInfos()
        message.sessionId = self.sessionId
        message.worker.CopyFrom(self.workerJob)
        message.signalData = json.dumps({"keys": self.currentManager.getSignalData()}, ensure_ascii=False).encode('gbk')

        self.logicInterface.OnAppWorkerLogicFinished(message, metadata=self.registrar.getAuthMetadata())



    def onCommandErrorHappened(self, message: str, command: statsModel.AppWorkerCommands):
        answer = statsModel.AppWorkerCommandsAnswerError()
        answer.sessionId = self.sessionId
        answer.commandId = command.commandId
        answer.error = message
        self.logicInterface.SendCommandAnswerError(answer, metadata=self.registrar.getAuthMetadata())
        return True

    @staticmethod
    def serialize(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, datetime.date):
            return datetime.datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S.%fZ")
        serialize_op = getattr(obj, "serialize", None)
        if callable(serialize_op):
            return obj.serialize(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__

        return None

    def runCommandWithCallbackAsync(self, module, commandName, data, callback):
        command = statsModel.AppWorkerModuleCommand()
        command.command = commandName
        command.module = module
        command.params = "{}"
        command.commandId = self.get_random_string(20)
        cbaa = CommandCallbackData()
        cbaa.command = command
        cbaa.module = module
        cbaa.message = data
        cbaa.cb = callback
        self.commandCallbacks[command.commandId] = cbaa
        try:
            command.params = json.dumps(data)
        except Exception as e:
            pass
        command.sessionId = self.sessionId
        self.logicInterface.RunModuleCommand(command, metadata=self.registrar.getAuthMetadata())
        return True

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def runCommand(self, module, commandName, data):
        command = statsModel.AppWorkerModuleCommand()
        command.command = commandName
        command.module = module
        command.params = ""
        command.commandId = self.get_random_string(20)
        try:
            command.params = json.dumps(data)
        except Exception as e:
            pass
        command.sessionId = self.sessionId
        self.logicInterface.RunModuleCommand(command, metadata=self.registrar.getAuthMetadata())

        return True

    def runNextCommand(self):
        if len(self.commandQueue) > 0:
            self.command_running = True
            command = self.commandQueue[0]
            commandThread = threading.Thread(target=self.onCommandReceived_Thread, args=[command])
            commandThread.start()
        else:
            self.command_running = False

    def wait_for_commands(self, restart = False):

        try:
           # self.session.start(is_restart=restart, session=DataTable())

            registrationData = statsModel.AppWorkerSessionRegistration()
            registrationData.sessionId = self.sessionId
            registrationData.worker.CopyFrom(self.workerJob)
            data = self.logicInterface.RegisterAppWorkerSession(registrationData, metadata=self.registrar.getAuthMetadata())
            if data.success == False:
                ### this is an error exit session now
                self.shutdown()

            if (self.waitingQueue != None):
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()
            self.commandStream = self.logicInterface.WatchAppWorkerCommands(iter(self.waitingQueue.get, None))
            registration = statsModel.AppWorkerSessionRegistration()
            registration.worker.CopyFrom(self.workerJob)
            registration.sessionId = self.sessionId
            self.waitingQueue.put(registration)
            for command in self.commandStream:
                self.queueCommand(command)

        except Exception as e:
            self.onErrorHappenedInCommunication(e)

    def onErrorHappenedInCommunication(self, e):
        # hmmm lets see if thi sis cool
        if not self.canceled:
            start_time = threading.Timer(2, self.restartCommandWatcher)
            start_time.start()
        #self.stop()

    def restartCommandWatcher(self):
        self.wait_for_commands(True)

    def installLogicPluginCode(self):

        code = self.logicInfoFull.code
        filename = self.logicInfoFull.codeId
        codeType = self.logicInfoFull.codeType
        codeVersion = self.logicInfoFull.codeVersion

        pluginWorker = PluginsWorker.PluginsWorker(None, None)
        config = PluginConfigInfo()
        config.filetype = codeType
        config.filecontent = code
        config.type = "logic"
        config.testOnly = False
        config.name = filename
        config.version = codeVersion
        pluginWorker.installPlugin(config)

    def loadLogicPluginCode(self):
        code = self.logicInfoFull.code
        filename = self.logicInfoFull.codeId
        codeType = self.logicInfoFull.codeType
        codeVersion = self.logicInfoFull.codeVersion
        version_fixed = str(codeVersion).replace(".", "-").replace("/", "-").replace(":", "-")

        pluginLoader = PluginLoader()
        pluginLoader.loadPlugin(".logic_modules/"+filename+"_"+version_fixed)


    def startSession(self):

        try:
            index = 0
            lastPercentage = 0
            rowLength = len(self.dataFrame.index)
            logicComponentsWithInfo = []
            self.parameterTable = self.logicConfig.parameterTable

            #if self.dataFrame.shape[0] <= 0:
            #    raise Exception("The Dataframe you send is empty - thats an error because i need 'cold data' to start the trader")

            self.installLogicPluginCode()
            self.loadLogicPluginCode()

            self.onBeforeWorkerStarts()
            self.generateLogicComponentsInfo()
            self.brokerInterface = LogicBrokerInterface(self.workerJob, self.sessionId, self.logicInterface, self)

            self.listenThread = threading.Thread(target=self.wait_for_commands)
            self.listenThread.start()

        except Exception as e:
            tb = traceback.format_exc()
            self.logger().error(tb)
            self.onLogicRunnerError(None, e)
            return False

        return True

    def run(self):

        t = threading.Thread(target=self.startSession, args=[], daemon=True)
        t.start()

        try:
            t.join()
        except Exception as e:
            pass

        return True
