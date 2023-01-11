from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IRequestInterface import IRequestInterface
from nerualpha.session.ISession import ISession
from nerualpha.request.IRequestParams import IRequestParams

T = TypeVar("T")
K = TypeVar("K")

@dataclass
class RequestInterfaceWithParams(IRequestInterface,Generic[T,K]):
    requestParams: IRequestParams[T]
    session: ISession
    def __init__(self,session,params):
        self.session = session
        self.requestParams = params
    
    async def execute(self):
        return await self.session.bridge.request(self.requestParams)
    
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
