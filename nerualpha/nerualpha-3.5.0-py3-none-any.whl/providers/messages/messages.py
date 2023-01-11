from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.messages.messageActions import MessageActions
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.messages.IMessages import IMessages
from nerualpha.session.ISession import ISession
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.providers.messages.contracts.unsubscribeEventsPayload import UnsubscribeEventsPayload
from nerualpha.providers.messages.contracts.listenEventsPayload import ListenEventsPayload
from nerualpha.providers.messages.contracts.sendTextPayload import SendTextPayload
from nerualpha.providers.messages.contracts.ISendImageContent import ISendImageContent
from nerualpha.providers.messages.contracts.sendImagePayload import SendImagePayload
from nerualpha.providers.messages.contracts.listenMessagesPayload import ListenMessagesPayload
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.messages.contracts.IBaseMessage import IBaseMessage
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.messages.contracts.sendResponse import SendResponse

@dataclass
class Messages(IMessages):
    vonageAPI: IVonageAPI
    session: ISession
    baseUrl: str = field(default = "https://api.nexmo.com")
    provider: str = field(default = "vonage-messaging")
    def __init__(self,session):
        self.session = session
        self.vonageAPI = VonageAPI(self.session)
    
    def send(self,message):
        url = f'{self.baseUrl}/v1/messages'
        method = "POST"
        return self.vonageAPI.invoke(url,method,message)
    
    def sendText(self,from_,to,message):
        payload = SendTextPayload(from_,to,message)
        url = f'{self.baseUrl}/v0.1/messages'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def sendImage(self,from_,to,imageContent):
        payload = SendImagePayload(from_,to,imageContent)
        url = f'{self.baseUrl}/v0.1/messages'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def listenMessages(self,from_,to,callback):
        payload = ListenMessagesPayload(from_,to,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,MessageActions.SubscribeInboundMessages,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def listenEvents(self,from_,to,callback):
        payload = ListenEventsPayload(from_,to,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,MessageActions.SubscribeInboundEvents,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onMessage(self,callback,from_,to):
        payload = ListenMessagesPayload(from_,to,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,MessageActions.SubscribeInboundMessages,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onMessageEvents(self,callback,from_,to):
        payload = ListenEventsPayload(from_,to,self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,MessageActions.SubscribeInboundEvents,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def unsubscribeEvents(self,id):
        payload = UnsubscribeEventsPayload(id)
        action = ActionPayload(self.provider,MessageActions.UnsubscribeEvents,payload)
        return RequestInterface(self.session,action)
    
    def reprJSON(self):
        result = {}
        dict = asdict(self)
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in dict:
            val = getattr(self, key)

            if val is not None:
                if type(val) is list:
                    parsedList = []
                    for i in val:
                        if hasattr(i,'reprJSON'):
                            parsedList.append(i.reprJSON())
                        else:
                            parsedList.append(i)
                    val = parsedList

                if hasattr(val,'reprJSON'):
                    val = val.reprJSON()
                if key in keywordsMap:
                    key = keywordsMap[key]
                result.__setitem__(key.replace('_hyphen_', '-'), val)
        return result
