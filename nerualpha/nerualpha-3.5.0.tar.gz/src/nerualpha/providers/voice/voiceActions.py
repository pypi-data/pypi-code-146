from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class VoiceActions:
    ConversationSubscribeInboundCall = "conversation-subscribe-inbound-call"
    VapiSubscribeInboundCall = "vapi-subscribe-inbound-call"
    VapiSubscribeEvent = "vapi-subscribe-event"
    ConversationSubscribeEvent = "conversation-subscribe-event"
