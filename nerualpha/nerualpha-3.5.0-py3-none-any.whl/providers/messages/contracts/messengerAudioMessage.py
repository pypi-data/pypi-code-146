from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.IMessenger import IMessenger
from nerualpha.providers.messages.contracts.IMessengerAudioMessage import IMessengerAudioMessage
from nerualpha.providers.messages.contracts.IURLPayload import IURLPayload

@dataclass
class MessengerAudioMessage(IMessengerAudioMessage):
    from_: str
    to: str
    audio: IURLPayload
    message_type: str = field(default = "audio")
    channel: str = field(default = "messenger")
    messenger: IMessenger = None
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
