from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class MessageActions:
    SubscribeInboundMessages = "subscribe-inbound-messages"
    SubscribeInboundEvents = "subscribe-inbound-events"
    UnsubscribeEvents = "unsubscribe-event"
