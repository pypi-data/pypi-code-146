from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.selfLink import SelfLink
from nerualpha.providers.voice.contracts.conversationTimestamp import ConversationTimestamp
from nerualpha.providers.voice.contracts.responseProperties import ResponseProperties

@dataclass
class CreateConversationResponse:
    sequence_number: int
    properties: ResponseProperties
    state: str
    name: str
    timestamp: ConversationTimestamp
    _links: SelfLink
    id: str
    display_name: str = None
    image_url: str = None
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
