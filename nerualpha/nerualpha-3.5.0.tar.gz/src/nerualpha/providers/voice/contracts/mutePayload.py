from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IMutePayload import IMutePayload
from nerualpha.providers.voice.csEvents import CSEvents

@dataclass
class MutePayload(IMutePayload):
    to: str
    type_: str
    from_: str = None
    def __init__(self,enable,to,from_ = None):
        if enable:
            self.type_ = CSEvents.MuteOn
        
        else: 
            self.type_ = CSEvents.MuteOff
        
        self.to = to
        if from_ is not None:
            self.from_ = from_
        
    
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
