from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.messages.contracts.IBaseMessage import IBaseMessage
from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.providers.messages.contracts.ISendImageContent import ISendImageContent
from nerualpha.providers.messages.contracts.sendImagePayload import SendImagePayload
from nerualpha.providers.messages.contracts.sendTextPayload import SendTextPayload
from nerualpha.providers.messages.contracts.unsubscribeEventsPayload import UnsubscribeEventsPayload
from nerualpha.providers.messages.contracts.sendResponse import SendResponse


#interface
class IMessages(ABC):
    @abstractmethod
    def send(self,message):
        pass
    @abstractmethod
    def sendText(self,from_,to,message):
        pass
    @abstractmethod
    def sendImage(self,from_,to,imageContent):
        pass
    @abstractmethod
    def listenMessages(self,from_,to,callback):
        pass
    @abstractmethod
    def listenEvents(self,from_,to,callback):
        pass
    @abstractmethod
    def onMessage(self,callback,from_,to):
        pass
    @abstractmethod
    def onMessageEvents(self,callback,from_,to):
        pass
    @abstractmethod
    def unsubscribeEvents(self,id):
        pass
