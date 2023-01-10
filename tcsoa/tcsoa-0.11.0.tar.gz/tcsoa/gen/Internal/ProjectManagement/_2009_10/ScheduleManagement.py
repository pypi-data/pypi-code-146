from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.ProjectManagement._2009_10.ScheduleManagement import ScheduleModifyContainer, GenericAttributesContainer
from tcsoa.gen.Internal.ProjectManagement._2008_06.ScheduleManagement import ScheduleModifyContainer, GenericAttributesContainer
from typing import List
from tcsoa.gen.Internal.ProjectManagement._2007_06.ScheduleManagement import StringValContainer
from tcsoa.gen.Internal.ProjectManagement._2007_01.ScheduleManagement import StringValueContainer
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class KeyValuePair(TcBaseObj):
    """
    Simple key value pair struture
    
    :var key: the integer key - the parameterized index
    :var value: the string value - the parameterized value
    """
    key: int = 0
    value: str = ''


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
class TranslationDataRequest(TcBaseObj):
    """
    Contain list of request structs
    
    :var genericContainers: List of generic containers
    :var scheduleModifyContainer: list Schedule modify container (there should always be only one of
    scheduleModifyContainer in the request. It was made into a vector in order to make the bounds 0 or more)
    """
    genericContainers: List[GenericAttributesContainer] = ()
    scheduleModifyContainer: List[ScheduleModifyContainer] = ()


@dataclass
class TranslationDataSchedule(TcBaseObj):
    """
    Contain list of POM objects
    
    :var dataObjects: List of POM objects
    """
    dataObjects: List[BusinessObject] = ()


@dataclass
class TranslationModelClass(TcBaseObj):
    """
    Model Class
    
    :var attribute: attribute meta data
    :var name: class name
    :var parentClassName: parent class name
    """
    attribute: List[StringValueContainer] = ()
    name: str = ''
    parentClassName: str = ''


@dataclass
class TranslationModelMetaData(TcBaseObj):
    """
    Schedule Schema
    
    :var modelClass: model class
    """
    modelClass: List[TranslationModelClass] = ()


@dataclass
class TranslationPreferences(TcBaseObj):
    """
    Contain preferences for the translation;
    SiteTimeZone,
    Default_Base_Calendar_Preference, 
    DefaultActualToSystemDate,
    SM_SCHEDULING_ENGINE_DATE,
    SM_View_CriticalPath.
    These preferences can have one of the types;
    TC_preference_all = 0;
    TC_preference_user = 1;
    TC_preference_role = 2;
    TC_preference_group = 3;
    TC_preference_site = 4;
    
    :var preferences: list of preferences
    """
    preferences: List[StringValContainer] = ()


@dataclass
class TranslationSchedules(TcBaseObj):
    """
    Contain list of ScheduleData structures
    
    :var translationDataSchedule: list of TranslationDataSchedule structures
    """
    translationDataSchedule: List[TranslationDataSchedule] = ()


@dataclass
class TranslatorException(TcBaseObj):
    """
    A structure containing translator exception IDs
    
    :var objectUid: the Uid of the object
    :var operation: The operation that genrated the exception.
    The type is suppose to be Teamcenter::Soa::ProjectManagement::_2009_10::ScheduleManagement::TranslatorOperation
    but this is generating error in SOA build (error published type being used in un-published type)
    :var errorNumber: the translator error number
    :var errorSeverity: The severity of the error from the translator; 
    information = 1; 
    warning =     2;
    error   =     3;         
    user_error =  4;
    :var errorString: the translator error string
    :var parameterValues: values for a parameterized error message
    """
    objectUid: str = ''
    operation: int = 0
    errorNumber: int = 0
    errorSeverity: int = 0
    errorString: str = ''
    parameterValues: List[KeyValuePair] = ()


@dataclass
class TranslatorResponseContainer(TcBaseObj):
    """
    Generic response structure
    
    :var translatorResponseContainerSub: list of sub translator response containers
    """
    translatorResponseContainerSub: List[TranslatorResponseContainerSub] = ()


@dataclass
class TranslatorResponseContainerSub(TcBaseObj):
    """
    A structure made up _0806 GenericAttributeContainers and TranslatorExceptions
    
    :var scheduleUid: the schedule uid
    :var genericAttributesContainer: list of GenericAttributeContainer structures
    :var translatorExceptions: list of translator exceptions
    """
    scheduleUid: str = ''
    genericAttributesContainer: List[GenericAttributesContainer] = ()
    translatorExceptions: List[TranslatorException] = ()


@dataclass
class TranslatorResponseScheduleModifyContainer(TcBaseObj):
    """
    Schedule modify response structure
    
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
