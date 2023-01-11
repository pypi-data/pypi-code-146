from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.contracts.createConversationResponse import CreateConversationResponse
from nerualpha.providers.voice.conversation import Conversation
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.voice.voiceActions import VoiceActions
from nerualpha.providers.voice.IVoice import IVoice
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.session.ISession import ISession
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.providers.voice.contracts.IVapiEventParams import IVapiEventParams
from nerualpha.providers.voice.contracts.createConversationPayload import CreateConversationPayload
from nerualpha.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint
from nerualpha.providers.voice.contracts.vapiAnswerCallBack import VapiAnswerCallBack
from nerualpha.providers.voice.contracts.vapiEventCallBackPayload import VapiEventCallBackPayload
from nerualpha.providers.voice.contracts.vapiCreateCallPayload import VapiCreateCallPayload
from nerualpha.providers.voice.contracts.onInboundCallPayload import OnInboundCallPayload
from nerualpha.IBridge import IBridge
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.voice.contracts.vapiCreateCallResponse import VapiCreateCallResponse

@dataclass
class Voice(IVoice):
    bridge: IBridge
    vonageApi: IVonageAPI
    session: ISession
    provider: str = field(default = "vonage-voice")
    regionURL: str = field(default = "https://api.nexmo.com")
    def __init__(self,session,regionURL = None):
        self.session = session
        self.bridge = session.bridge
        self.vonageApi = VonageAPI(self.session)
        if regionURL is not None:
            self.regionURL = regionURL
        
    
    def onInboundCall(self,callback,to,from_ = None):
        if to.type_ is None:
            to.type_ = "phone"
        
        if from_ is not None and from_.type_ is None:
            from_.type_ = "phone"
        
        payload = OnInboundCallPayload(self.session.wrapCallback(callback,[]),to,from_)
        action = ActionPayload(self.provider,VoiceActions.ConversationSubscribeInboundCall,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    async def createConversation(self,name = None,displayName = None):
        conversationName = name
        conversationDisplayName = displayName
        if name is None:
            conversationId = self.bridge.substring(self.session.createUUID(),0,5)
            conversationName = f'name_cs_{conversationId}'
        
        if displayName is None:
            conversationDisplayName = f'dn_{conversationName};'
        
        payload = CreateConversationPayload(conversationName,conversationDisplayName)
        url = "https://api.nexmo.com/v0.3/conversations"
        method = "POST"
        res = await self.vonageApi.invoke(url,method,payload).execute()
        return Conversation(res.id,self.session)
    
    def onVapiAnswer(self,callback):
        payload = VapiAnswerCallBack(self.session.wrapCallback(callback,[]))
        action = ActionPayload(self.provider,VoiceActions.VapiSubscribeInboundCall,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onVapiEvent(self,params):
        payload = VapiEventCallBackPayload()
        payload.callback = self.session.wrapCallback(params.callback,[])
        if params.conversationID is None and params.vapiUUID is None:
            raise Exception("Either conversationID or vapiUUID is required")
        
        if params.vapiUUID is not None:
            payload.vapiID = params.vapiUUID
        
        elif params.conversationID is not None:
            payload.conversationID = params.conversationID
        
        action = ActionPayload(self.provider,VoiceActions.VapiSubscribeEvent,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def vapiCreateCall(self,from_,to,ncco):
        vapiCreateCallPayload = VapiCreateCallPayload(from_,to,ncco)
        return self.vonageApi.invoke(f'{self.regionURL}/v1/calls',"POST",vapiCreateCallPayload)
    
    def uploadNCCO(self,uuid,ncco):
        return self.vonageApi.invoke(f'{self.regionURL}/v1/calls/{uuid}',"PUT",ncco)
    
    def getConversation(self,id):
        return Conversation(id,self.session)
    
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
