from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.IBridge import IBridge
from nerualpha.providers.events.eventEmitter import EventEmitter
from nerualpha.providers.events.IEventEmitter import IEventEmitter
from nerualpha.providers.logger.ILogContext import ILogContext
from nerualpha.providers.logger.ILogger import ILogger
from nerualpha.providers.logger.logContext import LogContext
from nerualpha.providers.logger.logger import Logger
from nerualpha.providers.logger.logLevels import LogLevels
from nerualpha.services.commandService.ICommandService import ICommandService
from nerualpha.services.config.IConfig import IConfig
from nerualpha.services.jwt.IJwt import IJWT
from nerualpha.session.command import Command
from nerualpha.session.IActionPayload import IActionPayload
from nerualpha.session.ICommand import ICommand
from nerualpha.session.IFilter import IFilter
from nerualpha.session.ISession import ISession
from nerualpha.session.wrappedCallback import WrappedCallback
from nerualpha.services.config.urlObject import UrlObject

@dataclass
class NeruSession(ISession):
    eventEmitter: IEventEmitter
    commandService: ICommandService
    logger: ILogger
    bridge: IBridge
    jwt: IJWT
    config: IConfig
    id: str
    def __init__(self,commandService,bridge,config,jwt,id):
        self.commandService = commandService
        self.id = id
        self.bridge = bridge
        self.config = config
        self.jwt = jwt
        self.eventEmitter = EventEmitter(self)
        self.logger = Logger(self)
    
    async def emitSessionCreatedEvent(self,ttl):
        await self.eventEmitter.emitSessionCreatedEvent(ttl)
    
    def createUUID(self):
        return self.bridge.uuid()
    
    def getToken(self):
        if self.config.debug:
            return None
        
        return self.jwt.getToken()
    
    def log(self,level,message,context = None):
        if self.config.logsSubmission is False:
            self.bridge.log("Skipping sending logs as config.logsSubmission is set to false")
        
        elif self.bridge.getEnv("SKIP_LOGS_SUBMISSION") == "true":
            self.bridge.log("Skipping sending logs as SKIP_LOGS_SUBMISSION is set to true")
        
        else: 
            self.bridge.runBackgroundTask(self.logger.log(level,message,context))
        
    
    def wrapCallback(self,route,filters):
        wrappedCallback = WrappedCallback()
        wrappedCallback.filters = filters
        wrappedCallback.id = self.createUUID()
        wrappedCallback.instanceServiceName = self.config.instanceServiceName
        wrappedCallback.sessionId = self.id
        wrappedCallback.instanceId = self.config.instanceId
        wrappedCallback.path = route
        return wrappedCallback
    
    def constructCommandHeaders(self):
        headers = {}
        headers["traceId"] = self.createUUID()
        headers["instanceId"] = self.config.instanceId
        headers["sessionId"] = self.id
        headers["apiAccountId"] = self.config.apiAccountId
        headers["apiApplicationId"] = self.config.apiApplicationId
        headers["applicationName"] = self.config.instanceServiceName
        headers["applicationId"] = self.config.applicationId
        return headers
    
    def constructRequestHeaders(self):
        headers = {}
        headers["X-Neru-SessionId"] = self.id
        headers["X-Neru-ApiAccountId"] = self.config.apiAccountId
        headers["X-Neru-ApiApplicationId"] = self.config.apiApplicationId
        headers["X-Neru-InstanceId"] = self.config.instanceId
        headers["X-Neru-TraceId"] = self.bridge.uuid()
        headers["Content-Type"] = "application/json"
        token = self.getToken()
        if token is not None:
            headers["Authorization"] = f'Bearer {token}'
        
        return headers
    
    async def executeAction(self,actionPayload,method):
        try:
            commandHeaders = self.constructCommandHeaders()
            requestHeaders = self.constructRequestHeaders()
            payload = Command(commandHeaders,actionPayload)
            url = self.config.getExecutionUrl(actionPayload.provider)
            result = await self.commandService.executeCommand(url,method,payload,requestHeaders)
            context = LogContext(actionPayload.action,self.bridge.jsonStringify(actionPayload.payload),self.bridge.jsonStringify(result))
            self.log(LogLevels.info,f'Executing action: {actionPayload.action}, provider: {actionPayload.provider}',context)
            return result
        
        except Exception as e:
            context = LogContext(actionPayload.action,self.bridge.jsonStringify(actionPayload.payload),e.message)
            self.log(LogLevels.error,f'Error while executing action: {actionPayload.action}, provider: {actionPayload.provider}',context)
            raise e
        
    
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
