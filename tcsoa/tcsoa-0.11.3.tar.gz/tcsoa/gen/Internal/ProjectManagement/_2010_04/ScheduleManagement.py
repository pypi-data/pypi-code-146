from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ProjectManagement._2008_06.ScheduleManagement import SubMasterMetaData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.ProjectManagement._2009_10.ScheduleManagement import TranslationModelClass, TranslationPreferences, TranslationDataRequest, TranslationSchedules
from dataclasses import dataclass


@dataclass
class TranslationDataContainer(TcBaseObj):
    """
    Internal data structure for moving POM objects between C/C++ and Java translator
    
    :var schedules: list of TranslationDataSchedule structure
    :var modelMetaData: Structure containing model classes
    :var preferences: list of string value containers of preferences
    :var requestData: request data
    """
    schedules: TranslationSchedules = None
    modelMetaData: TranslationModelMetaData = None
    preferences: TranslationPreferences = None
    requestData: TranslationDataRequest = None


@dataclass
class TranslationModelMetaData(TcBaseObj):
    """
    Schedule Schema
    
    :var modelClass: model class
    :var subMasterRelationship: Metadata containing relationship of sub-schedule to Master-Schedules
    """
    modelClass: List[TranslationModelClass] = ()
    subMasterRelationship: List[SubMasterMetaData] = ()
