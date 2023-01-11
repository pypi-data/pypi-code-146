from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.ISendTextPayload import ISendTextPayload
from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.providers.messages.contracts.ISendTextMessagePayload import ISendTextMessagePayload
from nerualpha.providers.messages.contracts.sendTextMessagePayload import SendTextMessagePayload
from nerualpha.providers.messages.contracts.sendTextContent import SendTextContent

@dataclass
class SendTextPayload(ISendTextPayload):
    message: ISendTextMessagePayload
    to: IMessageContact
    from_: IMessageContact
    def __init__(self,from_,to,text):
        self.from_ = from_
        self.to = to
        self.message = SendTextMessagePayload(SendTextContent(text))
    
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
