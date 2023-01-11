from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.jwt.jwtPayload import JWTPayload
from nerualpha.request.IRequestParams import IRequestParams


#interface
class IBridge(ABC):
    @abstractmethod
    def testRegEx(self,str,regExp):
        pass
    @abstractmethod
    def isInteger(self,value):
        pass
    @abstractmethod
    def substring(self,str,start,end = None):
        pass
    @abstractmethod
    def jsonStringify(self,data):
        pass
    @abstractmethod
    def jsonParse(self,json):
        pass
    @abstractmethod
    def getEnv(self,name):
        pass
    @abstractmethod
    def request(self,params):
        pass
    @abstractmethod
    def requestWithoutResponse(self,params):
        pass
    @abstractmethod
    def uuid(self):
        pass
    @abstractmethod
    def isoDate(self):
        pass
    @abstractmethod
    def runBackgroundTask(self,task):
        pass
    @abstractmethod
    def createReadStream(self,path):
        pass
    @abstractmethod
    def toISOString(self,seconds):
        pass
    @abstractmethod
    def jwtSign(self,payload,privateKey,algorithm):
        pass
    @abstractmethod
    def jwtVerify(self,token,privateKey,algorithm):
        pass
    @abstractmethod
    def jwtDecode(self,token):
        pass
    @abstractmethod
    def getSystemTime(self):
        pass
    @abstractmethod
    def log(self,data):
        pass
    @abstractmethod
    def getObjectKeys(self,obj):
        pass
