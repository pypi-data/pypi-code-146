from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.neruSession import NeruSession
from nerualpha.IBridge import IBridge
from nerualpha.services.config.IConfig import IConfig
from nerualpha.services.jwt.jwt import JWT
from nerualpha.bridge import Bridge
from nerualpha.services.config.config import Config
from nerualpha.request.IRequest import IRequest
from nerualpha.providers.state.state import State
from nerualpha.services.jwt.IJwt import IJWT
from nerualpha.INeru import INeru
from nerualpha.services.commandService.ICommandService import ICommandService
from nerualpha.services.commandService.commandService import CommandService

@dataclass
class Neru(INeru):
    commandService: ICommandService
    jwt: IJWT
    config: IConfig
    bridge: IBridge
    def __init__(self):
        self.bridge = Bridge()
        self.config = Config(self.bridge)
        self.jwt = JWT(self.bridge,self.config)
        self.commandService = CommandService(self.bridge)
    
    def createSession(self,ttl = 7 * 24 * 60 * 60):
        if self.bridge.isInteger(ttl) is False or ttl < 0:
            raise Exception("ttl must be a positive integer")
        
        id = self.bridge.uuid()
        session = self.createSessionWithId(id)
        self.bridge.runBackgroundTask(session.emitSessionCreatedEvent(ttl))
        return session
    
    def createSessionWithId(self,id):
        return NeruSession(self.commandService,self.bridge,self.config,self.jwt,id)
    
    def getSessionById(self,id):
        if id is None:
            raise Exception("id is required")
        
        return self.createSessionWithId(id)
    
    def getAppUrl(self):
        return self.config.appUrl
    
    def getSessionFromRequest(self,req):
        if req is None:
            raise Exception("getSessionFromRequest: function requires request object to be provided")
        
        if req.headers is None:
            raise Exception("getSessionFromRequest: invalid request object proivided")
        
        id = req.headers["x-neru-sessionid"]
        if id is None:
            raise Exception(f'getSessionFromRequest: request does not contain \"x-neru-sessionid\" header')
        
        return self.getSessionById(id)
    
    def getGlobalSession(self):
        uuid = "00000000-0000-0000-0000-000000000000"
        return self.getSessionById(uuid)
    
    def getGlobalState(self):
        session = self.getGlobalSession()
        return State(session,f'application:{self.config.instanceId}')
    
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
