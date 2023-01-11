from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.selfLink import SelfLink
from nerualpha.providers.voice.contracts.userEmbedded import UserEmbedded
from nerualpha.providers.voice.contracts.memberTimestamp import MemberTimestamp
from nerualpha.providers.voice.contracts.media import Media

@dataclass
class MemberResponse:
    channel: object
    media: Media
    timestamp: MemberTimestamp
    _links: SelfLink
    _embedded: UserEmbedded
    state: str
    id: str = None
    conversation_id: str = None
    knocking_id: str = None
    invited_by: str = None
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
