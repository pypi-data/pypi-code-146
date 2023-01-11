from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.meetings.contracts.recordingOptions import RecordingOptions
from nerualpha.providers.meetings.contracts.roomLinks import RoomLinks

@dataclass
class RoomResponse:
    _links: RoomLinks
    expire_after_use: bool
    expires_at: str
    created_at: str
    theme_id: str
    is_available: bool
    meeting_code: str
    recording_options: RecordingOptions
    type_: str
    metadata: str
    display_name: str
    id: str
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
