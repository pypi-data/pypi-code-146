from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.voice.contracts.IInviteMemberPayload import IInviteMemberPayload
from nerualpha.providers.voice.contracts.IUser import IUser
from nerualpha.providers.voice.memberActions import MemberActions
from nerualpha.providers.voice.memberStates import MemberStates
from nerualpha.providers.voice.contracts.IChannel import IChannel
from nerualpha.providers.voice.contracts.user import User

@dataclass
class InviteMemberPayload(IInviteMemberPayload):
    channel: IChannel
    state: str
    action: str
    user: IUser
    def __init__(self,userName,channel):
        user = User()
        user.name = userName
        self.user = user
        self.action = MemberActions.Join
        self.state = MemberStates.Invited
        self.channel = channel
    
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
