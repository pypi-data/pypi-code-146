from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.meetings.contracts.ICreateRoomPayload import ICreateRoomPayload

@dataclass
class CreateRoomPayload(ICreateRoomPayload):
    display_name: str
    metadata: str = None
    type_: str = None
    expires_at: str = None
    expire_after_use: bool = None
    recording_options: str = None
    def __init__(self,display_name,metadata = None,type_ = None,expires_at = None,expire_after_use = None,recording_options = None):
        self.display_name = display_name
        self.metadata = metadata
        self.type_ = type_
        self.expires_at = expires_at
        self.expire_after_use = expire_after_use
        self.recording_options = recording_options
    
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
