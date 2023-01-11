from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.session.IPayloadWithCallback import IPayloadWithCallback


#interface
class IVapiAnswerCallBack(IPayloadWithCallback):
    pass
