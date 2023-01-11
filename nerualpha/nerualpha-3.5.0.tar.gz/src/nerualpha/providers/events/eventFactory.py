from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.ISession import ISession
from nerualpha.providers.events.IEventFactory import IEventFactory
from nerualpha.providers.events.INeruEvent import INeruEvent
from nerualpha.providers.events.neruEvent import NeruEvent
from nerualpha.providers.events.neruEventSourceTypes import NeruEventSourceTypes
from nerualpha.providers.events.neruEventTypes import NeruEventTypes

@dataclass
class EventFactory(IEventFactory):
    session: ISession
    def __init__(self,session):
        self.session = session
    
    def createEvent(self,eventName,details):
        if eventName is NeruEventTypes.SESSION_CREATED:
            event = NeruEvent()
            event.event_type = NeruEventTypes.SESSION_CREATED
            event.source_type = NeruEventSourceTypes.INSTANCE
            event.details = details
            self.setCommonFields(event)
            return event
        
        raise Exception("Event type not supported: " + eventName)
    
    def setCommonFields(self,event):
        event.timestamp = self.session.bridge.isoDate()
        event.id = self.session.bridge.uuid()
        event.source_id = self.session.config.instanceServiceName
        event.api_account_id = self.session.config.apiAccountId
        event.api_application_id = self.session.config.apiApplicationId
        event.session_id = self.session.id
        event.instance_id = self.session.config.instanceId
    
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
