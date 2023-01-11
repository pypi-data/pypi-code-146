from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.session.ISession import ISession
from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.providers.numbers.contracts.IGetNumbersOptions import IGetNumbersOptions
from nerualpha.providers.numbers.contracts.INumberOptions import INumberOptions
from nerualpha.providers.numbers.contracts.ISearchNumbersOptions import ISearchNumbersOptions
from nerualpha.providers.numbers.contracts.IUpdateNumberOptions import IUpdateNumberOptions
from nerualpha.providers.numbers.contracts.getNumbersResponse import GetNumbersResponse
from nerualpha.providers.numbers.contracts.numbersOperationResponse import NumbersOperationResponse

@dataclass
class Numbers:
    bridge: IBridge
    accountUrl: str
    baseUrl: str
    vonageAPI: IVonageAPI
    session: ISession
    def __init__(self,session):
        self.session = session
        self.bridge = session.bridge
        self.vonageAPI = VonageAPI(self.session)
        self.baseUrl = "https://rest.nexmo.com/number"
        self.accountUrl = "https://rest.nexmo.com/account/numbers"
    
    def getNumbers(self,apiKey,apiSecret,getNumberOptions = None):
        url = f'{self.accountUrl}?api_key={apiKey}&api_secret={apiSecret}'
        options = {}
        if getNumberOptions.application_id is not None:
            options["application_id"] = getNumberOptions.application_id
        
        if getNumberOptions.has_application is not None:
            options["has_application"] = getNumberOptions.has_application
        
        if getNumberOptions.country is not None:
            options["country"] = getNumberOptions.country
        
        if getNumberOptions.pattern is not None:
            options["pattern"] = getNumberOptions.pattern
        
        if getNumberOptions.search_pattern is not None:
            options["search_pattern"] = getNumberOptions.search_pattern
        
        if getNumberOptions.size is not None:
            options["size"] = getNumberOptions.size
        
        if getNumberOptions.index is not None:
            options["index"] = getNumberOptions.index
        
        url = self.buildUrl(url,options)
        method = "GET"
        return self.vonageAPI.invoke(url,method,None)
    
    def searchNumbers(self,apiKey,apiSecret,searchNumberOptions):
        url = f'{self.baseUrl}/search?api_key={apiKey}&api_secret={apiSecret}'
        options = {}
        if searchNumberOptions.country is not None:
            options["country"] = searchNumberOptions.country
        
        if searchNumberOptions.type_ is not None:
            options["type_"] = searchNumberOptions.type_
        
        if searchNumberOptions.pattern is not None:
            options["pattern"] = searchNumberOptions.pattern
        
        if searchNumberOptions.search_pattern is not None:
            options["search_pattern"] = searchNumberOptions.search_pattern
        
        if searchNumberOptions.features is not None:
            options["features"] = searchNumberOptions.features
        
        if searchNumberOptions.size is not None:
            options["size"] = searchNumberOptions.size
        
        if searchNumberOptions.index is not None:
            options["index"] = searchNumberOptions.index
        
        url = self.buildUrl(url,options)
        method = "GET"
        return self.vonageAPI.invoke(url,method,None)
    
    def buyNumber(self,apiKey,apiSecret,numberOptions):
        url = f'{self.baseUrl}/buy?api_key={apiKey}&api_secret={apiSecret}'
        options = {}
        if numberOptions.country is not None:
            options["country"] = numberOptions.country
        
        if numberOptions.msisdn is not None:
            options["msisdn"] = numberOptions.msisdn
        
        if numberOptions.target_api_key is not None:
            options["target_api_key"] = numberOptions.target_api_key
        
        url = self.buildUrl(url,options)
        method = "POST"
        return self.vonageAPI.invoke(url,method,None)
    
    def cancelNumber(self,apiKey,apiSecret,numberOptions):
        url = f'{self.baseUrl}/cancel?api_key={apiKey}&api_secret={apiSecret}'
        options = {}
        if numberOptions.country is not None:
            options["country"] = numberOptions.country
        
        if numberOptions.msisdn is not None:
            options["msisdn"] = numberOptions.msisdn
        
        if numberOptions.target_api_key is not None:
            options["target_api_key"] = numberOptions.target_api_key
        
        url = self.buildUrl(url,options)
        method = "POST"
        return self.vonageAPI.invoke(url,method,None)
    
    def updateNumber(self,apiKey,apiSecret,updateNumberOptions):
        url = f'{self.baseUrl}/update?api_key={apiKey}&api_secret={apiSecret}'
        options = {}
        if updateNumberOptions.country is not None:
            options["country"] = updateNumberOptions.country
        
        if updateNumberOptions.msisdn is not None:
            options["msisdn"] = updateNumberOptions.msisdn
        
        if updateNumberOptions.app_id is not None:
            options["app_id"] = updateNumberOptions.app_id
        
        if updateNumberOptions.moHttpUrl is not None:
            options["moHttpUrl"] = updateNumberOptions.moHttpUrl
        
        if updateNumberOptions.moSmppSysType is not None:
            options["moSmppSysType"] = updateNumberOptions.moSmppSysType
        
        if updateNumberOptions.voiceCallbackType is not None:
            options["voiceCallbackType"] = updateNumberOptions.voiceCallbackType
        
        if updateNumberOptions.voiceCallbackValue is not None:
            options["voiceCallbackValue"] = updateNumberOptions.voiceCallbackValue
        
        if updateNumberOptions.voiceStatusCallback is not None:
            options["voiceStatusCallback"] = updateNumberOptions.voiceStatusCallback
        
        url = self.buildUrl(url,options)
        method = "POST"
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
