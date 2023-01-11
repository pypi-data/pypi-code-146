from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.scheduler.schedulerActions import SchedulerActions
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.scheduler.IScheduler import IScheduler
from nerualpha.providers.scheduler.contracts.startAtPayload import StartAtPayload
from nerualpha.providers.scheduler.contracts.schedulerPayload import SchedulerPayload
from nerualpha.providers.scheduler.contracts.IStartAtParams import IStartAtParams
from nerualpha.session.ISession import ISession
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.scheduler.contracts.listAllSchedulersResponse import ListAllSchedulersResponse
from nerualpha.providers.scheduler.contracts.getSchedulerResponse import GetSchedulerResponse
from nerualpha.providers.scheduler.contracts.listAllPayload import ListAllPayload
from nerualpha.providers.scheduler.contracts.IListAllPayload import IListAllPayload
from nerualpha.IBridge import IBridge

@dataclass
class Scheduler(IScheduler):
    bridge: IBridge
    session: ISession
    provider: str = field(default = "vonage-scheduler")
    def __init__(self,session):
        self.session = session
        self.bridge = session.bridge
    
    def startAt(self,params):
        if params.id is not None and self.bridge.testRegEx(params.id,"^[a-zA-Z0-9][a-zA-Z0-9-_]*$") is not True:
            raise Exception("Error: The input does not match the required pattern ^[a-zA-Z0-9][a-zA-Z0-9-_]*$. Please enter a string that starts with a letter or a digit, and contains only letters, digits, hyphens, and underscores.")
        
        startAtPayload = StartAtPayload()
        startAtPayload.startAt = params.startAt
        startAtPayload.callback = self.session.wrapCallback(params.callback,[])
        if params.payload is not None:
            startAtPayload.payload = params.payload
        
        if params.interval is not None:
            startAtPayload.interval = params.interval
        
        if params.id is not None:
            startAtPayload.id = params.id
        
        action = ActionPayload(self.provider,SchedulerActions.Create,startAtPayload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def listAll(self,size = 10,cursor = None):
        payload = ListAllPayload(size,cursor)
        action = ActionPayload(self.provider,SchedulerActions.List,payload)
        return RequestInterface(self.session,action)
    
    def get(self,scheduleId):
        payload = SchedulerPayload(scheduleId)
        action = ActionPayload(self.provider,SchedulerActions.Get,payload)
        return RequestInterface(self.session,action)
    
    def cancel(self,scheduleId):
        payload = SchedulerPayload(scheduleId)
        action = ActionPayload(self.provider,SchedulerActions.Cancel,payload)
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
