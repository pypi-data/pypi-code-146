from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.jwt.jwtPayload import JWTPayload
from nerualpha.IBridge import IBridge
from nerualpha.services.config.IConfig import IConfig
from nerualpha.services.jwt.IJwt import IJWT

@dataclass
class JWT(IJWT):
    config: IConfig
    bridge: IBridge
    _token: str = field(default = None)
    ttl: int = field(default = 300)
    def __init__(self,bridge,config):
        self.bridge = bridge
        self.config = config
    
    def getToken(self):
        try:
            if self._token is None or self.isExpired():
                exp = self.bridge.getSystemTime() + self.ttl
                self._token = self.mintToken(exp)
            
            return self._token
        
        except Exception as e:
            raise Exception("Error verifying JWT: " + e)
        
    
    def isExpired(self):
        nowInSeconds = self.bridge.getSystemTime()
        twentySeconds = 20
        payload = self.bridge.jwtDecode(self._token)
        return payload["exp"] - twentySeconds <= nowInSeconds
    
    def mintToken(self,exp):
        now = self.bridge.getSystemTime()
        payload = JWTPayload()
        payload.api_account_id = self.config.apiAccountId
        payload.api_application_id = self.config.apiApplicationId
        payload.sub = self.config.instanceServiceName
        payload.iat = now
        payload.exp = exp
        return self.bridge.jwtSign(payload,self.config.privateKey,"RS256")
    
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
