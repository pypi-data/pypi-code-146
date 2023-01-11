from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.services.commandService.ICommandService import ICommandService
from nerualpha.session.ISession import ISession
from nerualpha.providers.state.IState import IState
from nerualpha.providers.state.IStateCommand import IStateCommand
from nerualpha.providers.state.stateCommand import StateCommand
from nerualpha.providers.state.stateOperations import StateOperations
from nerualpha.request.requestMethods import RequestMethods
from nerualpha.services.config.urlObject import UrlObject
from nerualpha.providers.state.expireOptions import ExpireOptions

@dataclass
class State(IState):
    commandService: ICommandService
    session: ISession
    bridge: IBridge
    url: UrlObject
    namespace: str
    provider: str = field(default = "client-persistence-api")
    def __init__(self,session,namespace = None):
        self.bridge = session.bridge
        self.url = session.config.getExecutionUrl(self.provider)
        if namespace is None:
            self.namespace = f'state:{session.id}'
        
        else: 
            self.namespace = namespace
        
        self.session = session
        self.commandService = session.commandService
    
    def createCommand(self,op,key,args):
        return StateCommand(op,self.namespace,key,args)
    
    async def executeCommand(self,command):
        return await self.commandService.executeCommand(self.url,RequestMethods.POST,command,self.session.constructRequestHeaders())
    
    async def set(self,key,value):
        payload = []
        payload.append(self.bridge.jsonStringify(value))
        command = self.createCommand(StateOperations.SET,key,payload)
        return await self.executeCommand(command)
    
    async def get(self,key):
        payload = []
        command = self.createCommand(StateOperations.GET,key,payload)
        result = await self.executeCommand(command)
        return self.bridge.jsonParse(result)
    
    async def delete(self,key):
        payload = []
        command = self.createCommand(StateOperations.DEL,key,payload)
        return await self.executeCommand(command)
    
    async def hdel(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HDEL,htable,payload)
        return await self.executeCommand(command)
    
    async def hexists(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HEXISTS,htable,payload)
        return await self.executeCommand(command)
    
    async def hgetall(self,htable):
        payload = []
        command = self.createCommand(StateOperations.HGETALL,htable,payload)
        response = await self.executeCommand(command)
        result = {}
        for i in range(0,response.__len__(),2):
            result[response[i]] = response[i + 1]
        
        return result
    
    async def hmget(self,htable,keys):
        command = self.createCommand(StateOperations.HMGET,htable,keys)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def hvals(self,htable):
        payload = []
        command = self.createCommand(StateOperations.HVALS,htable,payload)
        response = await self.executeCommand(command)
        result = []
        for i in range(0,response.__len__()):
            result.append(response[i])
        
        return result
    
    async def hget(self,htable,key):
        payload = [key]
        command = self.createCommand(StateOperations.HGET,htable,payload)
        result = await self.executeCommand(command)
        return result
    
    async def hset(self,htable,keyValuePairs):
        payload = []
        keys = self.bridge.getObjectKeys(keyValuePairs)
        for i in range(0,keys.__len__()):
            payload.append(keys[i])
            payload.append(keyValuePairs[keys[i]])
        
        command = self.createCommand(StateOperations.HSET,htable,payload)
        return await self.executeCommand(command)
    
    async def hlen(self,htable):
        payload = []
        command = self.createCommand(StateOperations.HLEN,htable,payload)
        return await self.executeCommand(command)
    
    async def rpush(self,list,value):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.RPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def rpop(self,list,count = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.RPOP,list,args)
        response = await self.executeCommand(command)
        result = self.parseResponse(response)
        return result
    
    async def lpush(self,list,value):
        payload = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LPUSH,list,payload)
        return await self.executeCommand(command)
    
    async def lpop(self,list,count = 1):
        args = [self.bridge.jsonStringify(count)]
        command = self.createCommand(StateOperations.LPOP,list,args)
        response = await self.executeCommand(command)
        result = self.parseResponse(response)
        return result
    
    async def lrem(self,list,value,count = 0):
        args = [self.bridge.jsonStringify(count),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LREM,list,args)
        return await self.executeCommand(command)
    
    async def llen(self,list):
        payload = []
        command = self.createCommand(StateOperations.LLEN,list,payload)
        return await self.executeCommand(command)
    
    async def lrange(self,list,startPos = 0,endPos = -1):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LRANGE,list,args)
        response = await self.executeCommand(command)
        result = self.parseResponse(response)
        return result
    
    async def ltrim(self,list,startPos,endPos):
        args = [self.bridge.jsonStringify(startPos),self.bridge.jsonStringify(endPos)]
        command = self.createCommand(StateOperations.LTRIM,list,args)
        response = await self.executeCommand(command)
        return response
    
    async def linsert(self,list,before,pivot,value):
        direction = "AFTER"
        if before is True:
            direction = "BEFORE"
        
        args = [direction,self.bridge.jsonStringify(pivot),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LINSERT,list,args)
        response = await self.executeCommand(command)
        return response
    
    async def lindex(self,list,position):
        args = [self.bridge.jsonStringify(position)]
        command = self.createCommand(StateOperations.LINDEX,list,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def lset(self,list,position,value):
        args = [self.bridge.jsonStringify(position),self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.LSET,list,args)
        return await self.executeCommand(command)
    
    async def incrby(self,key,value):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.INCRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def decrby(self,key,value):
        args = [self.bridge.jsonStringify(value)]
        command = self.createCommand(StateOperations.DECRBY,key,args)
        response = await self.executeCommand(command)
        return self.bridge.jsonParse(response)
    
    async def expire(self,key,seconds,option = None):
        args = [self.bridge.jsonStringify(seconds)]
        if option is not None:
            args.append(option)
        
        command = self.createCommand(StateOperations.EXPIRE,key,args)
        return await self.executeCommand(command)
    
    def parseResponse(self,response):
        result = []
        if response is not None:
            for i in range(0,response.__len__()):
                result.append(self.bridge.jsonParse(response[i]))
            
        
        return result
    
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
