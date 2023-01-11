from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback
from nerualpha.providers.messages.contracts.IMessageContact import IMessageContact
from nerualpha.session.IWrappedCallback import IWrappedCallback


#interface
class IListenEventsPayload(IPayloadWithCallback):
    from_:IMessageContact
    to:IMessageContact
    callback:IWrappedCallback
