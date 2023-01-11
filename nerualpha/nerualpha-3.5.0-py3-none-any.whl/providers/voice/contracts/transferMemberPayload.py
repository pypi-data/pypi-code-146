from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.ITransferMemberPayload import ITransferMemberPayload
from nerualpha.providers.voice.memberActions import MemberActions
from nerualpha.providers.voice.memberStates import MemberStates
from nerualpha.providers.voice.contracts.IUser import IUser
from nerualpha.providers.voice.csChannelTypes import CSChannelTypes
from nerualpha.providers.voice.contracts.user import User
from nerualpha.providers.voice.contracts.IChannel import IChannel
from nerualpha.providers.voice.contracts.channel import Channel

@dataclass
class TransferMemberPayload(ITransferMemberPayload):
    user: IUser
    state: str
    channel: IChannel
    action: str
    def __init__(self,userId,legId):
        self.action = MemberActions.Join
        self.channel = Channel()
        self.channel.id = legId
        self.channel.type_ = CSChannelTypes.PHONE
        self.state = MemberStates.Joined
        user = User()
        user.id = userId
        self.user = user
    
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
