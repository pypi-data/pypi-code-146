import math
import threading
from typing import List
import abc
from coinlib.broker.BrokerDTO import BrokerDetailedInfo, BrokerSymbol
from coinlib.brokerWorker.BrokerSession import BrokerSession
from coinlib.logics.manager import LogicManager
import coinlib.dataWorker_pb2 as statsModel
import simplejson as json
import coinlib.dataWorker_pb2_grpc as stats

import queue
import datetime

class ILogicBrokerInterfaceListener(metaclass=abc.ABCMeta):
    def onBrokerErrorHappenedInCommunication(self, error):
        raise NotImplementedError
    def onBrokerCommandReceived(self, command):
        raise NotImplementedError

class LogicBrokerInterface:
    interface = None
    listener: ILogicBrokerInterfaceListener = None
    waitingQueue = None
    waitingQueue = None
    commandStream = None
    listenThread = None

    def __init__(self, workerJob, sessionId, interface: stats.AppWorkerStub, listener: ILogicBrokerInterfaceListener):
        self.interface = interface
        self.listener = listener
        self.command_running = False
        self.commandQueue = []
        self.workerJob = workerJob
        self.sessionId = sessionId
        self.waitingQueue = None
        self.connectBrokerCommandThread()
        pass

    def onCommandReceived(self, command):
        self.listener.onBrokerCommandReceived(command)

    def wait_for_commands(self, restart = False):

        try:
            if self.waitingQueue is not None:
                self.waitingQueue.put(None)
            self.waitingQueue = None
            self.waitingQueue = queue.SimpleQueue()

            self.commandStream = self.interface.WatchBrokerCommands(iter(self.waitingQueue.get, None))
            registration = statsModel.AppWorkerSessionRegistration()
            registration.worker.CopyFrom(self.workerJob)
            registration.sessionId = self.sessionId
            self.waitingQueue.put(registration)

            for command in self.commandStream:
                self.onCommandReceived(command)

        except Exception as e:
            self.onErrorHappenedInCommunication(e)

    def onErrorHappenedInCommunication(self, error):

        return self.listener.onBrokerErrorHappenedInCommunication(error)

    def connectBrokerCommandThread(self):
        self.listenThread = threading.Thread(target=self.wait_for_commands)
        self.listenThread.start()

        return None

    def getCommand(self, command: str, params={}):

        cmd = statsModel.AppWorkerBrokerCommand()
        cmd.sessionId = self.sessionId
        cmd.worker.CopyFrom(self.workerJob)
        cmd.command = command
        try:
            cmd.params = json.dumps(params, default=BrokerSession.serialize)
        except Exception as e:
            pass

        answer: statsModel.AppWorkerBrokerCommandAnswer = self.interface.RunBrokerCommand(cmd)
        data = None

        if answer.error == True and answer.errorMessage is not None:
            raise Exception(answer.errorMessage)

        try:
            data = json.loads(answer.response)
        except Exception as e:
            pass
        return data

