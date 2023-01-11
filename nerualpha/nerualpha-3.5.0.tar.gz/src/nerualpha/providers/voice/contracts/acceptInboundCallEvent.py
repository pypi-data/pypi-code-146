from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IAcceptInboundCallBody import IAcceptInboundCallBody
from nerualpha.providers.voice.contracts.IAcceptInboundCallEvent import IAcceptInboundCallEvent

@dataclass
class AcceptInboundCallEvent(IAcceptInboundCallEvent):
    from_: str
    body: IAcceptInboundCallBody
    params: Dict[str,str]
    timestamp: str
    application_id: str
    type_: str
    def __init__(self):
        pass
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
