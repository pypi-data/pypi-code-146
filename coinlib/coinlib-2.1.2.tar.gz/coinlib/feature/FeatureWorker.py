import datetime
import queue
import sys
import time

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import inspect

from coinlib.data.DataTable import DataTable
from coinlib.feature.CoinlibFeature import CoinlibFeature
from coinlib.feature.FeatureDTO import FeatureDatabaseInfo, RabbitInfo
import pandas as pd
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.statistics.StatisticMethodJob import StatisticMethodJob


class FeatureWorkerWrapper(WorkerJobProcess):

    def __init__(self, workerJob, factory):
        self.workerConfig = None
        self.waitingQueue = None
        self.workerProcessInfo = None
        self.loop = asyncio.new_event_loop()
        self.commandQueue = []
        self.canceled = False
        self.command_running = False
        self.workerRegistrationInfo = None
        super(FeatureWorkerWrapper, self).__init__(workerJob, factory)

    def initialize(self):
        self.registrar = Registrar()
        self.workerInterface = stats.FeatureWorkerStub(self.getChannel())
        if self.workerConfig is None:
            workerConfigGlobal = self.workerInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
            if workerConfigGlobal.HasField("startSessionConfig"):
                self.workerConfig = workerConfigGlobal.startSessionConfig

            self.workerRegistrationInfo = self.registrar.featureCallbacks["feature_"+self.workerConfig.identifier]
            self.workerProcessInfo = self.workerRegistrationInfo["process"]
        pass

    def onErrorHappened(self, message, critical=False):

        indicatorError = statsModel.FeatureError()
        indicatorError.error.critical = critical
        indicatorError.error.message = str(message)
        indicatorError.worker.CopyFrom(self.workerJob)

        self.workerInterface.OnErrorOccured(indicatorError, metadata=self.registrar.getAuthMetadata())

    def send_event(self, eventName, data=None):
        event = statsModel.FeatureEventData()
        event.event = eventName
        event.sessionId = self.workerConfig.sessionId
        event.data = json.dumps(data)
        event.worker.CopyFrom(self.workerJob)
        self.workerInterface.OnEvent(event, metadata=self.registrar.getAuthMetadata())
        return True

    def error(self, message):
        self.onErrorHappened(message)
        return False

    def setConfig(self, configuration):
        self.workerConfig = configuration
        pass

    def getTargetClass(self):

        return self.workerProcessInfo

    def getIdentifier(self):
        return self.workerConfig.identifier

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

    def onCommandReceived_Thread(self, command: statsModel.FeatureCommands):
        params = json.loads(command.commandParams)
        try:
            answerData = None

            # at first check for internal commands
            if command.command == "log":
                # DONT REMOVE - please let this print because its needed for the developer to see some log infos from worker
                print(params["message"])
            elif command.command == "triggerRun":
                answerData = self.targetWorker.triggerRun(params)
            elif command.command == "fetchData":
                answerData = self.targetWorker.start_fetch_data(params)
            elif command.command == "exit":
                self.shutdown()
                return True


        except Exception as e:
            self.onCommandErrorHappened(str(e), command)
            self.unqueueCommand(command)
            self.runNextCommand()
            return False

        answer = statsModel.FeatureCommandsAnswer()
        answer.sessionId = self.workerConfig.sessionId
        answer.commandId = command.commandId

        try:
            answer.answerData = json.dumps(answerData, default=FeatureWorkerWrapper.serialize)
        except Exception as e:
            pass

        self.workerInterface.SendCommandAnswer(answer, metadata=self.registrar.getAuthMetadata())
        self.unqueueCommand(command)
        self.runNextCommand()

        pass

    def shutdown(self):
        self.canceled = True
        self.targetWorker.stop()
        super().stop()
        self.commandStream.cancel()
        self.workerInterface.close()
        super().closeChannel()

    def runNextCommand(self):
        if len(self.commandQueue) > 0:
            self.command_running = True
            command = self.commandQueue[0]
            commandThread = threading.Thread(target=self.onCommandReceived_Thread, args=[command])
            commandThread.start()
        else:
            self.command_running = False

    def unqueueCommand(self, command):
        self.commandQueue.remove(command)

    def queueCommand(self, command):
        self.commandQueue.append(command)

        if self.command_running == False:
            self.runNextCommand()

    def onCommandErrorHappened(self, message: str, command: statsModel.FeatureCommands):
        answer = statsModel.FeatureCommandsAnswerError()
        answer.sessionId = self.workerConfig.sessionId
        answer.commandId = command.commandId
        answer.error = message
        self.workerInterface.SendCommandAnswerError(answer, metadata=self.registrar.getAuthMetadata())
        return True

    def wait_for_commands(self, restart = False):

        try:

            registrationData = statsModel.FeatureSessionRegistration()
            registrationData.sessionId = self.workerConfig.sessionId
            info = self.workerInterface.RegisterSession(registrationData, metadata=self.registrar.getAuthMetadata())
            try:
                if (self.waitingQueue != None):
                    self.waitingQueue.put(None)
            except Exception as e:
                pass
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()

            if info.success:
                self.commandStream = self.workerInterface.WatchCommands(iter(self.waitingQueue.get, None))
                m = statsModel.FeatureCommands()
                m.sessionId = self.workerConfig.sessionId
                self.waitingQueue.put(m)
                for command in self.commandStream:
                    self.queueCommand(command)
            else:
                self.shutdown()

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

    def runWorkerInThread(self):

        try:
            instance = self.getTargetClass()
            self.targetWorker : CoinlibFeature = instance()
            self.targetWorker.set_worker(self)

            try:
                sessData = json.loads(self.workerConfig.sessionData)
            except Exception as je:
                 sessData = {}

            rabbitInfo = RabbitInfo()
            rabbitInfo.ip = self.workerConfig.rabbitServer
            rabbitInfo.user = self.workerConfig.rabbitUser
            rabbitInfo.pwd = self.workerConfig.rabbitPwd
            rabbitInfo.port = self.workerConfig.rabbitPort
            rabbitInfo.prefix = self.workerConfig.rabbitQueuePrefix

            databaseInfo = FeatureDatabaseInfo()
            databaseInfo.server = self.workerConfig.targetDatabaseServer
            databaseInfo.id = self.workerConfig.targetDatabaseID

            self.targetWorker.set_database_info(databaseInfo)
            self.targetWorker.set_session_data(sessData)
            self.targetWorker.set_session_id(self.workerConfig.sessionId)
            self.targetWorker.set_rabbit_info(rabbitInfo)

            self.loop.run_until_complete(self.targetWorker.start(self.loop, self.getOptions()))


        except Exception as e:
            print(e)
            self.onErrorHappened(str(e), True)
            return False

        return True

    def startWorker(self):
        self.workerThread = threading.Thread(target=self.runWorkerInThread, args=[])
        self.workerThread.start()

        self.listenThread = threading.Thread(target=self.wait_for_commands)
        self.listenThread.start()

        pass

    def getOptions(self):
        try:
            return json.loads(self.workerConfig.optionValues)
        except Exception as e:
            return {}

    def runProcess(self):
        try:
            self.run()

        except Exception as e:
            self.logger().error(e)
            self.onErrorProcess(e)
            return

        self.factory.onWorkerJobProcessFinished(self)
        self.logger().info("Finished")
        return True

    def run(self):


        try:
            self.startWorker()
        except Exception as e:
           self.onErrorHappened(e.message)
           pass

        return True
