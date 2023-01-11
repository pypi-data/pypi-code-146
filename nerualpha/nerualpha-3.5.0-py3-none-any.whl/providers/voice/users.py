from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.session.ISession import ISession
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.createUserPayload import CreateUserPayload
from nerualpha.providers.voice.IUsers import IUsers
from nerualpha.providers.voice.contracts.getUsersResponse import GetUsersResponse
from nerualpha.providers.voice.contracts.userResponse import UserResponse
from nerualpha.providers.voice.contracts.updateUserPayload import UpdateUserPayload

@dataclass
class Users(IUsers):
    bridge: IBridge
    baseUrl: str
    vonageAPI: IVonageAPI
    session: ISession
    def __init__(self,session):
        self.session = session
        self.bridge = session.bridge
        self.vonageAPI = VonageAPI(self.session)
        self.baseUrl = "https://api.nexmo.com/v0.3"
    
    def getUsers(self,page_size = None,order = None,pageUrl = None):
        url = ""
        if pageUrl is not None:
            url = pageUrl
        
        else: 
            options = {}
            if page_size:
                options["page_size"] = page_size
            
            if order:
                options["order"] = order
            
            url = self.buildUrl(f'{self.baseUrl}/users',options)
        
        method = "GET"
        return self.vonageAPI.invoke(url,method,None)
    
    def getUser(self,user_id):
        url = f'{self.baseUrl}/users/{user_id}'
        method = "GET"
        return self.vonageAPI.invoke(url,method,None)
    
    def createUser(self,createUserPayload):
        url = f'{self.baseUrl}/users'
        method = "POST"
        return self.vonageAPI.invoke(url,method,createUserPayload)
    
    def updateUser(self,user_id,updateUserPayload):
        url = f'{self.baseUrl}/users/{user_id}'
        method = "PATCH"
        return self.vonageAPI.invoke(url,method,updateUserPayload)
    
    def deleteUser(self,user_id):
        url = f'{self.baseUrl}/users/{user_id}'
        method = "DELETE"
        return self.vonageAPI.invoke(url,method,None)
    
    def buildUrl(self,baseUrl,options):
        keys = self.bridge.getObjectKeys(options)
        queryString = ""
        for i in range(0,keys.__len__()):
            key = keys[i]
            value = options[key]
            queryString += f'{key}={value}'
            if i + 1 < keys.__len__():
                queryString += "&"
            
        
        if queryString.__len__() > 0:
            return f'{baseUrl}?{queryString}'
        
        return baseUrl
    
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
