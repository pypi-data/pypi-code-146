from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IChannelSIPEndpoint import IChannelSIPEndpoint
from nerualpha.providers.voice.csChannelTypes import CSChannelTypes

@dataclass
class ChannelSIPEndpoint(IChannelSIPEndpoint):
    headers: Dict[str,str]
    uri: str
    type_: str
    username: str = None
    password: str = None
    def __init__(self,uri,headers,username = None,password = None):
        self.type_ = CSChannelTypes.SIP
        self.uri = uri
        self.headers = headers
        if username is not None:
            self.username = username
        
        if password is not None:
            self.password = password
        
    
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
