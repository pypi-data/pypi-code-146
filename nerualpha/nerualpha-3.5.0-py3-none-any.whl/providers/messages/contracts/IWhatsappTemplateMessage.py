from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.providers.messages.contracts.IBaseMessage import IBaseMessage
from nerualpha.providers.messages.contracts.IWhatsapp import IWhatsapp
from nerualpha.providers.messages.contracts.IWhatsappTemplate import IWhatsappTemplate


#interface
class IWhatsappTemplateMessage(IBaseMessage):
    template:IWhatsappTemplate
    whatsapp:IWhatsapp
