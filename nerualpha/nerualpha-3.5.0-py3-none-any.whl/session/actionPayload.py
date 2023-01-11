from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IActionPayload import IActionPayload
from nerualpha.session.IWrappedCallback import IWrappedCallback

T = TypeVar("T")

@dataclass
class ActionPayload(IActionPayload,Generic[T]):
    payload: T
    action: str
    provider: str
    description: str = None
    successCallback: IWrappedCallback = None
    errorCallback: IWrappedCallback = None
    def __init__(self,provider,action,payload,description = None):
        self.provider = provider
        self.action = action
        self.payload = payload
        if description is not None:
            self.description = description
        
    
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
