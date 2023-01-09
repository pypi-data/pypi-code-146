import abc
import asyncio

from coinlib import Registrar
from coinlib.broker import Broker
from coinlib.broker.BrokerDTO import Order, CoinlibBrokerAccount, BrokerEvent
from coinlib.broker.CoinlibBroker import CoinlibBroker, CoinlibBrokerListener
from coinlib.broker.CoinlibSessionManager import CoinlibSessionManager
from coinlib.data.DataTable import DataTable

class BrokerCommand:
    pass

class BrokerSessionWorkerListener:

    @abc.abstractmethod
    def onEventReceived(self, event: BrokerEvent, data: any):
        raise NotImplementedError



class BrokerSessionWorker(CoinlibBrokerListener):
    def __init__(self, sessionId: str, short_session_id: str, brokerClass: CoinlibBroker, accountData: CoinlibBrokerAccount, worker: BrokerSessionWorkerListener):
        self.worker: BrokerSessionWorkerListener = worker
        self.sessionId = sessionId
        self.short_session_id = short_session_id
        self.loop = asyncio.new_event_loop()
        self.commandsFinished = True
        self.brokerAccount = accountData
        self.sessionManager = CoinlibSessionManager()
        self.brokerClass: CoinlibBroker = brokerClass
        self.broker: CoinlibBroker = None
        self.registrar = Registrar()
        pass

    def getLoop(self):
        return self.loop

    def get_broker_instance(self) -> CoinlibBroker:
        return self.broker

    def start(self, is_restart=False, session=DataTable()):

        self.sessionManager = CoinlibSessionManager(session)
        self.broker: CoinlibBroker = self.brokerClass()
        self.broker.register_callback(self)
        self.loop.run_until_complete(self.broker.start_session(self.loop, self.sessionId, self.short_session_id,
                                                          self.brokerAccount, self.sessionManager, is_restart=is_restart))

    def stop(self):
        if self.broker:
            try:
                self.loop.run_until_complete(self.broker.stop_session())
            except Exception as e:
                pass

    def shutdown(self):
        self.stop()
        self.loop.close()

    def buildParams(self, params):

        paramList = ""
        comma = ""
        for p in params:
            paramValue = ""

            if isinstance(params[p], str):
                paramValue = "'"+params[p]+"'"
            elif isinstance(params[p], float):
                paramValue = str(params[p])
            elif isinstance(params[p], int):
                paramValue = str(params[p])

            paramList = paramList + comma + p + "="+paramValue+""
            comma = ","

        return paramList

    def runCommand(self, command: str, params: any, commandRaw):

        processData = self.loop.run_until_complete(eval("self.broker."+command+"("+self.buildParams(params)+")"))
        return processData

    def onEventReceived(self, event: BrokerEvent, data: any):
        return self.worker.onEventReceived(event, data)

