import abc
import asyncio
import threading
import datetime
from coinlib import Registrar
from coinlib.broker import Broker, CoinlibBroker
import simplejson as json
from coinlib.broker.BrokerDTO import Order, CoinlibBrokerAccount, BrokerEvent, CoinlibBrokerLoginParams, \
    BrokerContractType, BrokerAssetType
from coinlib.brokerWorker.BrokerSessionWorker import BrokerSessionWorker, BrokerCommand, BrokerSessionWorkerListener
from coinlib.data.DataTable import DataTable
from coinlib.dataWorker_pb2 import BrokerInfoStartSessionConfig

import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats


class BrokerSessionListener:

    @abc.abstractmethod
    def onSessionClose(self):
        raise NotImplementedError

    @abc.abstractmethod
    def onCommandErrorHappenedInBroker(self, error: str, command: BrokerCommand):
        raise NotImplementedError

    @abc.abstractmethod
    def onCommandAnswerInBroker(self, answer: statsModel.BrokerCommandsAnswer):
        raise NotImplementedError

    @abc.abstractmethod
    def onEventReceivedInBroker(self, event: statsModel.BrokerEventData):
        raise NotImplementedError

    pass


class BrokerSession(BrokerSessionWorkerListener):
    config: BrokerInfoStartSessionConfig
    _listener: BrokerSessionListener
    session: BrokerSessionWorker

    def __init__(self, config: BrokerInfoStartSessionConfig, listener: BrokerSessionListener):
        self.config = config
        self.commandQueue = []
        self.session: BrokerSessionWorker = None
        self._listener = listener
        self.command_running = False
        self._registrar = Registrar()
        self.initialize()
        pass

    def getLoop(self):
        return self.session.getLoop()

    def initialize(self):
        self.brokerWorkerRegistrationInfo = self._registrar.brokerCallbacks[
            "broker_" + self.config.brokerIdentifier]
        self.brokerWorkerProcessInfo = self.brokerWorkerRegistrationInfo["process"]

    def getBrokerClass(self):
        self.brokerType = "brokerSpot"
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.SPOT:
            self.brokerType = "brokerSpot"
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.FUTURE:
            self.brokerType = "brokerFuture"
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.MARGIN:
            self.brokerType = "brokerMargin"

        return self.brokerWorkerProcessInfo[self.brokerType]

    def getInstance(self) -> CoinlibBroker:
        return self.session.get_broker_instance()

    def shutdown(self):
        self.stop()
        if self._listener is not None:
            self._listener.onSessionClose()

    def stop(self):
        try :
            if self.session:
                self.session.stop()
        except Exception as e:
            pass

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

    def onCommandReceived_Thread(self, command: statsModel.BrokerCommands):
        params = json.loads(command.brokerCommandParams)
        try:
            print(command.brokerCommand)
            # at first check for internal commands
            if command.brokerCommand == "exit":
                self.shutdown()
                return True

            answerData = self.session.runCommand(command.brokerCommand, params, command)

        except Exception as e:
            try:
                if self._listener is not None:
                    self._listener.onCommandErrorHappenedInBroker(str(e), command)
            except Exception as ie:
                pass
            self.unqueueCommand(command)
            self.runNextCommand()
            return False

        answer = statsModel.BrokerCommandsAnswer()
        answer.sessionId = self.config.sessionId
        answer.commandId = command.commandId

        try:
            answer.answerData = json.dumps(answerData, default=BrokerSession.serialize)
        except Exception as e:
            pass
        try:
            if self._listener is not None:
                self._listener.onCommandAnswerInBroker(answer)
        except Exception as e:
            pass
        self.unqueueCommand(command)
        self.runNextCommand()

        pass

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

    def runCommand(self, command: BrokerCommand):

        self.queueCommand(command)

        return True

    def onEventReceived(self, event: BrokerEvent, data: any):
        try:
            dataBlock = statsModel.BrokerEventData()
            dataBlock.event = str(event)
            dataBlock.data = json.dumps(data, default=BrokerSession.serialize)
            dataBlock.sessionId = self.config.sessionId
            if self._listener is not None:
                self._listener.onEventReceivedInBroker(dataBlock)
        except Exception as e:
            pass

    def start(self, is_restart=False):

        brokerClass = self.getBrokerClass()

        brokerAccountData = CoinlibBrokerAccount()
        loginInfo = CoinlibBrokerLoginParams()
        loginInfo.apiKey = self.config.accountInfo.loginInfo.apikey
        loginInfo.secret = self.config.accountInfo.loginInfo.secret

        brokerAccountData.sandbox = self.config.accountInfo.sandbox
        brokerAccountData.exchange_id = self.config.accountInfo.exchange_id
        brokerAccountData.loginInfo = loginInfo
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.FUTURE:
            brokerAccountData.contractType = BrokerContractType.FUTURE
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.SPOT:
            brokerAccountData.contractType = BrokerContractType.SPOT
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.ContractType.MARGIN:
            brokerAccountData.contractType = BrokerContractType.MARGIN
        brokerAccountData.assetType = BrokerAssetType.COIN
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.AssetType.COIN:
            brokerAccountData.assetType = BrokerAssetType.COIN
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.AssetType.STOCK:
            brokerAccountData.assetType = BrokerAssetType.STOCK
        if self.config.accountInfo.contractType == statsModel.BrokerSessionAccountInfo.AssetType.FOREX:
            brokerAccountData.assetType = BrokerAssetType.FOREX

        shortSessionId = self.config.shortSessionId
        self.session = BrokerSessionWorker(self.config.sessionId,
                                           shortSessionId,
                                           brokerClass, brokerAccountData, self)

        self.session.start(is_restart=is_restart, session=DataTable())

        return self.session
