from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.createUserPayload import CreateUserPayload
from nerualpha.providers.voice.contracts.userResponse import UserResponse
from nerualpha.providers.voice.contracts.getUsersResponse import GetUsersResponse
from nerualpha.providers.voice.contracts.updateUserPayload import UpdateUserPayload
from nerualpha.providers.voice.contracts.ICreateUserPayload import ICreateUserPayload
from nerualpha.providers.voice.contracts.IUpdateUserPayload import IUpdateUserPayload


#interface
class IUsers(ABC):
    @abstractmethod
    def getUsers(self,page_size = None,order = None,pageUrl = None):
        pass
    @abstractmethod
    def getUser(self,user_id = None):
        pass
    @abstractmethod
    def createUser(self,createUserPayload):
        pass
    @abstractmethod
    def updateUser(self,user_id,updateUserPayload):
        pass
    @abstractmethod
    def deleteUser(self,user_id):
        pass
