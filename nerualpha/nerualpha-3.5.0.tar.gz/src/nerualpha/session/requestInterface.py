from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.ISession import ISession
from nerualpha.session.IActionPayload import IActionPayload
from nerualpha.request.requestMethods import RequestMethods

T = TypeVar("T")
K = TypeVar("K")

@dataclass
class RequestInterface(Generic[T,K]):
    method: str
    action: IActionPayload[T]
    session: ISession
    def __init__(self,session,action,method = RequestMethods.POST):
        self.session = session
        self.action = action
        self.method = method
    
    def onSuccess(self,route):
        self.action.successCallback = self.session.wrapCallback(route,[])
        return self
    
    def onError(self,route):
        self.action.errorCallback = self.session.wrapCallback(route,[])
        return self
    
    async def execute(self):
        return await self.session.executeAction(self.action,self.method)
    
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
