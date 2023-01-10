from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ProjectManagement._2011_06.ScheduleManagement import ScheduleModifyContainer
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.ProjectManagement._2009_10.ScheduleManagement import TranslatorException
from dataclasses import dataclass


@dataclass
class TranslatorResponseScheduleModifyContainer(TcBaseObj):
    """
    Translator schedule modify response structure
    
    :var translatorResponseScheduleModifyContainerSub: list of sub translator schedule modify response containers
    """
    translatorResponseScheduleModifyContainerSub: List[TranslatorResponseScheduleModifyContainerSub] = ()


@dataclass
class TranslatorResponseScheduleModifyContainerSub(TcBaseObj):
    """
    structure used internally on the server side to share objects between C++ and Java
    
    :var scheduleUid: the schedule uid
    :var scheduleModifyContainer: list of schedule modify structures
    :var translatorExceptions: list of translator exceptions
    """
    scheduleUid: str = ''
    scheduleModifyContainer: List[ScheduleModifyContainer] = ()
    translatorExceptions: List[TranslatorException] = ()
