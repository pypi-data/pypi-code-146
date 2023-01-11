from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.requestInterface import RequestInterface
from nerualpha.providers.vonageAPI.contracts.invokePayload import InvokePayload
from nerualpha.providers.voice.csEvents import CSEvents
from nerualpha.providers.voice.voiceActions import VoiceActions
from nerualpha.providers.vonageAPI.vonageAPI import VonageAPI
from nerualpha.session.filter import Filter
from nerualpha.session.actionPayload import ActionPayload
from nerualpha.providers.voice.IConversation import IConversation
from nerualpha.session.ISession import ISession
from nerualpha.providers.vonageAPI.IVonageAPI import IVonageAPI
from nerualpha.session.requestInterfaceForCallbacks import RequestInterfaceForCallbacks
from nerualpha.session.IFilter import IFilter
from nerualpha.providers.voice.contracts.transferMemberPayload import TransferMemberPayload
from nerualpha.providers.voice.contracts.sayStopPayload import SayStopPayload
from nerualpha.providers.voice.contracts.IPlayStreamBody import IPlayStreamBody
from nerualpha.providers.voice.contracts.playStreamPayload import PlayStreamPayload
from nerualpha.providers.voice.contracts.playStopPayload import PlayStopPayload
from nerualpha.providers.voice.contracts.reason import Reason
from nerualpha.providers.voice.contracts.deleteMemberPayload import DeleteMemberPayload
from nerualpha.providers.voice.contracts.sayTextPayload import SayTextPayload
from nerualpha.providers.voice.contracts.earmuffPayload import EarmuffPayload
from nerualpha.providers.voice.contracts.audioSettings import AudioSettings
from nerualpha.providers.voice.contracts.media import Media
from nerualpha.providers.voice.contracts.IChannel import IChannel
from nerualpha.providers.voice.contracts.channel import Channel
from nerualpha.providers.voice.contracts.IAcceptInboundCallEvent import IAcceptInboundCallEvent
from nerualpha.providers.voice.contracts.acceptInboundCallPayload import AcceptInboundCallPayload
from nerualpha.providers.voice.contracts.inviteMemberPayload import InviteMemberPayload
from nerualpha.providers.voice.contracts.mutePayload import MutePayload
from nerualpha.providers.voice.contracts.conversationPayloadWithCallback import ConversationPayloadWithCallback
from nerualpha.providers.voice.contracts.addUserPayload import AddUserPayload
from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.voice.contracts.ISayTextBody import ISayTextBody
from nerualpha.providers.voice.contracts.addUserResponse import AddUserResponse
from nerualpha.providers.voice.contracts.memberResponse import MemberResponse
from nerualpha.providers.voice.contracts.eventResponse import EventResponse
from nerualpha.providers.voice.contracts.playStreamResponseBody import PlayStreamResponseBody
from nerualpha.providers.voice.contracts.playStreamStopResponseBody import PlayStreamStopResponseBody
from nerualpha.providers.voice.contracts.earmuffResponseBody import EarmuffResponseBody
from nerualpha.providers.voice.contracts.muteResponseBody import MuteResponseBody
from nerualpha.providers.voice.contracts.audioSayResponseBody import AudioSayResponseBody
from nerualpha.providers.voice.contracts.audioSayStopResponseBody import AudioSayStopResponseBody

@dataclass
class Conversation(IConversation):
    baseUrl: str
    vonageAPI: IVonageAPI
    session: ISession
    name: str
    id: str
    provider: str = field(default = "vonage-voice")
    def __init__(self,id,session):
        self.id = id
        self.session = session
        self.vonageAPI = VonageAPI(self.session)
        self.baseUrl = "https://api.nexmo.com/v0.3"
    
    def acceptInboundCall(self,event):
        audioSettings = AudioSettings(True,False,False)
        media = Media(audioSettings,True)
        channel = Channel()
        channel.id = event.body.channel.id
        channel.type_ = event.body.channel.type_
        channel.to = event.body.channel.to
        channel.from_ = event.body.channel.from_
        payload = AcceptInboundCallPayload(event.body.user.id,event.from_,channel,media)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def inviteMember(self,name,channel):
        payload = InviteMemberPayload(name,channel)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def addUser(self,name):
        payload = AddUserPayload(name)
        url = f'{self.baseUrl}/users'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def transferMember(self,userId,legId):
        payload = TransferMemberPayload(userId,legId)
        url = f'{self.baseUrl}/conversations/{self.id}/members'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def deleteMember(self,memberId):
        reason = Reason("123","leaving conversation")
        payload = DeleteMemberPayload(reason)
        url = f'{self.baseUrl}/conversations/{self.id}/members/{memberId}'
        method = f'PATCH'
        return self.vonageAPI.invoke(url,method,payload)
    
    def sayText(self,body,to = None):
        if body.level is None:
            body.level = 1
        
        if body.loop is None:
            body.loop = 1
        
        if body.voice_name is None:
            body.voice_name = "Amy"
        
        if body.queue is None:
            body.queue = False
        
        if body.ssml is None:
            body.ssml = False
        
        payload = SayTextPayload(body,to)
        method = "POST"
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        return self.vonageAPI.invoke(url,method,payload)
    
    def sayStop(self,sayId,to = None):
        payload = SayStopPayload(sayId,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def playStream(self,body,to = None):
        if body.loop is None:
            body.loop = 1
        
        if body.level is None:
            body.level = 1
        
        payload = PlayStreamPayload(body,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def playStop(self,playId,to = None):
        payload = PlayStopPayload(playId,to)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def earmuff(self,enable,to,from_ = None):
        payload = EarmuffPayload(enable,to,from_)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def earmuffOn(self,to,from_ = None):
        return self.earmuff(True,to,from_)
    
    def earmuffOff(self,to,from_ = None):
        return self.earmuff(False,to,from_)
    
    def mute(self,enable,to,from_ = None):
        payload = MutePayload(enable,to,from_)
        url = f'{self.baseUrl}/conversations/{self.id}/events'
        method = "POST"
        return self.vonageAPI.invoke(url,method,payload)
    
    def muteOn(self,to,from_ = None):
        return self.mute(True,to,from_)
    
    def muteOff(self,to,from_ = None):
        return self.mute(False,to,from_)
    
    def listenForEvents(self,callback,filters):
        payload = ConversationPayloadWithCallback(self.session.wrapCallback(callback,filters),self.id)
        action = ActionPayload(self.provider,VoiceActions.ConversationSubscribeEvent,payload)
        return RequestInterfaceForCallbacks(self.session,action)
    
    def onConversationCreated(self,callback):
        filters = [Filter("type","contains",[CSEvents.ConversationCreated]),Filter("body.name","contains",[self.name])]
        return self.listenForEvents(callback,filters)
    
    def onSay(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSay]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlay(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlay]),Filter("conversation_id","contains",[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onSayStop(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSayStop]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlayStop(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlayStop]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onSayDone(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioSayDone]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onPlayDone(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioPlayDone]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onLegStatusUpdate(self,callback):
        filters = [Filter("type","contains",[CSEvents.LegStatusUpdate]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
    def onMemberJoined(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberJoined]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter(f'body.user.name',f'contains',[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onMemberInvited(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberInvited]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter("body.user.name","contains",[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onMemberLeft(self,callback,memberName = None):
        filters = [Filter("type","contains",[CSEvents.MemberLeft]),Filter(f'conversation_id',f'contains',[self.id])]
        if memberName is not None:
            filters.append(Filter("body.user.name","contains",[memberName]))
        
        return self.listenForEvents(callback,filters)
    
    def onDTMF(self,callback):
        filters = [Filter("type","contains",[CSEvents.AudioDTMF]),Filter(f'conversation_id',f'contains',[self.id])]
        return self.listenForEvents(callback,filters)
    
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
