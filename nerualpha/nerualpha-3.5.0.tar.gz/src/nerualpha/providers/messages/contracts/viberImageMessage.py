from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.IURLPayload import IURLPayload
from nerualpha.providers.messages.contracts.IViberService import IViberService
from nerualpha.providers.messages.contracts.IViberImageMessage import IViberImageMessage

@dataclass
class ViberImageMessage(IViberImageMessage):
    image: IURLPayload
    from_: str
    to: str
    message_type: str = field(default = "image")
    channel: str = field(default = "viber_service")
    viber_service: IViberService = None
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
