from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.request.requestMethods import RequestMethods
from nerualpha.request.requestParams import RequestParams
from nerualpha.services.config.IConfig import IConfig
from nerualpha.session.ISession import ISession
from nerualpha.providers.events.eventFactory import EventFactory
from nerualpha.providers.events.IEventEmitter import IEventEmitter
from nerualpha.providers.events.IEventFactory import IEventFactory
from nerualpha.providers.events.ISessionCreatedDetails import ISessionCreatedDetails
from nerualpha.providers.events.sessionCreatedDetails import SessionCreatedDetails
from nerualpha.providers.events.neruEventTypes import NeruEventTypes
from nerualpha.providers.events.INeruEvent import INeruEvent
from nerualpha.services.config.urlObject import UrlObject

@dataclass
class EventEmitter(IEventEmitter):
    url: UrlObject
    session: ISession
    eventFactory: IEventFactory
    bridge: IBridge
    config: IConfig
    provider: str = field(default = "events-submission")
    def __init__(self,session):
        self.config = session.config
        self.bridge = session.bridge
        self.session = session
        self.eventFactory = EventFactory(self.session)
        self.url = self.config.getExecutionUrl(self.provider)
    
    async def emitSessionCreatedEvent(self,ttl):
        expiresAt = self.bridge.toISOString(ttl)
        details = SessionCreatedDetails(expiresAt)
        event = self.eventFactory.createEvent(NeruEventTypes.SESSION_CREATED,details)
        await self.emit(event)
    
    async def emit(self,e):
        requestParams = RequestParams()
        requestParams.method = RequestMethods.POST
        requestParams.url = self.url
        requestParams.data = e
        requestParams.headers = self.session.constructRequestHeaders()
        await self.bridge.requestWithoutResponse(requestParams)
    
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
