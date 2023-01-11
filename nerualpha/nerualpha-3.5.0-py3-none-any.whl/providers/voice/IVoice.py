from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.vapiCreateCallPayload import VapiCreateCallPayload
from nerualpha.providers.voice.conversation import Conversation
from nerualpha.providers.voice.contracts.IVapiEventParams import IVapiEventParams
from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint
from nerualpha.providers.voice.contracts.vapiCreateCallResponse import VapiCreateCallResponse


#interface
class IVoice(ABC):
    @abstractmethod
    def onInboundCall(self,callback,to,from_ = None):
        pass
    @abstractmethod
    def createConversation(self,name = None,displayName = None):
        pass
    @abstractmethod
    def onVapiAnswer(self,callback):
        pass
    @abstractmethod
    def onVapiEvent(self,params):
        pass
    @abstractmethod
    def vapiCreateCall(self,from_,to,ncco):
        pass
    @abstractmethod
    def uploadNCCO(self,uuid,ncco):
        pass
    @abstractmethod
    def getConversation(self,id):
        pass
