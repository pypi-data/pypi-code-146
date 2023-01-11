from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class CSEvents:
    AppKnocking = "app:knocking"
    AudioSay = "audio:say"
    AudioSayStop = "audio:say:stop"
    AudioSayDone = "audio:say:done"
    AudioPlay = "audio:play"
    AudioPlayStop = "audio:play:stop"
    AudioPlayDone = "audio:play:done"
    AudioDTMF = "audio:dtmf"
    EarmuffOn = "audio:earmuff:on"
    EarmuffOff = "audio:earmuff:off"
    MuteOn = "audio:mute:on"
    MuteOff = "audio:mute:off"
    LegStatusUpdate = "leg:status:update"
    MemberJoined = "member:joined"
    MemberInvited = "member:invited"
    MemberLeft = "member:left"
    ConversationCreated = "conversation:created"
