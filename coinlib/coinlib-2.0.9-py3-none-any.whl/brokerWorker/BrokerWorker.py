import datetime
import queue
import time

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
import threading
import inspect

from coinlib.broker.Broker import BrokerContractType, BrokerAssetType
from coinlib.broker.BrokerDTO import CoinlibBrokerAccount, CoinlibBrokerLoginParams, BrokerEvent, OrderUpdateInformation
from coinlib.brokerWorker.BrokerSession import BrokerSession, BrokerSessionListener
from coinlib.data.DataTable import DataTable
import pandas as pd
import asyncio
import simplejson as json
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.Registrar import Registrar
from coinlib.statistics.StatisticMethodJob import StatisticMethodJob

class BrokerWorker(WorkerJobProcess, BrokerSessionListener):
    brokerSession: BrokerSession

    def __init__(self, workerJob, factory):
        self.brokerWorkerConfig = None
        self.waitingQueue = None
        self.brokerWorkerProcessInfo = None
        self.canceled = False
        self.command_running = False
        self.brokerWorkerRegistrationInfo = None
        super(BrokerWorker, self).__init__(workerJob, factory)

    def initialize(self):
        self.registrar = Registrar()
        self.brokerWorkerInterface = stats.BrokerWorkerStub(self.getChannel())
        if self.brokerWorkerConfig is None:
            brokerWorkerConfigGlobal = self.brokerWorkerInterface.GetConfig(self.workerJob, metadata=self.registrar.getAuthMetadata())
            if brokerWorkerConfigGlobal.HasField("startSessionConfig"):
                self.brokerWorkerConfig = brokerWorkerConfigGlobal.startSessionConfig

            self.brokerSession = BrokerSession(self.brokerWorkerConfig, self)
        pass

    def onEventReceivedInBroker(self, event: statsModel.BrokerEventData):
        try:

            event.worker.CopyFrom(self.workerJob)
            self.brokerWorkerInterface.OnBrokerEvent(event, metadata=self.registrar.getAuthMetadata())
        except Exception as e:
            pass

    def onErrorHappened(self, message):

        indicatorError = statsModel.BrokerError()
        indicatorError.error.message = str(message)
        indicatorError.sessionId = self.brokerWorkerConfig.sessionId
        indicatorError.worker.CopyFrom(self.workerJob)

        self.logger().error("Error in Broker Worker - "+str(message))

        self.brokerWorkerInterface.OnBrokerErrorOccured(indicatorError, metadata=self.registrar.getAuthMetadata())

    def error(self, message):
        self.onErrorHappened(message)
        return False

    def setConfig(self, configuration):
        self.brokerWorkerConfig = configuration
        pass


    def shutdown(self):
        self.canceled = True
        self.shutdownAllBrokers()
        super().stop()
        self.commandStream.cancel()
        super().closeChannel()

    def onCommandErrorHappenedInBroker(self, message: str, command: statsModel.BrokerCommands):
        answer = statsModel.BrokerCommandsAnswerError()
        answer.sessionId = self.brokerWorkerConfig.sessionId
        answer.commandId = command.commandId
        answer.error = message
        self.brokerWorkerInterface.SendCommandAnswerError(answer, metadata=self.registrar.getAuthMetadata())
        return True

    def onCommandAnswerInBroker(self, event: statsModel.BrokerCommandsAnswer):

        return self.brokerWorkerInterface.SendCommandAnswer(event, metadata=self.registrar.getAuthMetadata())

    def wait_for_commands(self, restart = False):

        try:
            self.brokerSession.start(is_restart=restart)
            registrationData = statsModel.BrokerSessionRegistration()
            registrationData.sessionId = self.brokerWorkerConfig.sessionId
            self.brokerWorkerInterface.RegisterBrokerSession(registrationData, metadata=self.registrar.getAuthMetadata())

            if (self.waitingQueue != None):
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()
            self.commandStream = self.brokerWorkerInterface.WatchBrokerCommands(iter(self.waitingQueue.get, None))
            registration = statsModel.BrokerCommandRegistration()
            registration.sessionId = self.brokerWorkerConfig.sessionId
            self.waitingQueue.put(registration)
            for command in self.commandStream:
                self.brokerSession.runCommand(command)

        except Exception as e:
            self.onErrorHappenedInCommunication(e)

    def onErrorHappenedInCommunication(self, e):
        # hmmm lets see if thi sis cool
        self.logger().error(e)
        if not self.canceled:
            start_time = threading.Timer(5, self.restartCommandWatcher)
            start_time.start()

    def restartCommandWatcher(self):
        if not self.canceled:
            self.wait_for_commands(True)

    def shutdownAllBrokers(self):
        if self.brokerSession:
            self.brokerSession.stop()

    def onSessionClose(self):
        self.shutdown()

    def startBrokerSession(self):

        self.brokerSession.start()

        self.listenThread = threading.Thread(target=self.wait_for_commands)
        self.listenThread.start()

    def get_broker_instance(self):
        return self.session.get_broker_instance()

    def getOptions(self):
        return json.loads(self.brokerWorkerConfig.options)

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


        self.startBrokerSession()
        """
        t = threading.Thread(target=self.startBrokerSession, args=[], daemon=True)

        t.start()

        try:
           t.join()
        except Exception as e:
           self.onErrorHappened(e.message)
           pass
"""
        return True
