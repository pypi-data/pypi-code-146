from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetLocalizedPropertiesInfo(TcBaseObj):
    """
    A structure of desired business objects, property names.
    
    :var inputObject: The desired business object to retrieved localized property values.
    :var propertyNames: A list of property name string.
    If propertyNames is an empty array, will get all displayable localizable properties.
    """
    inputObject: BusinessObject = None
    propertyNames: List[str] = ()


@dataclass
class GetLocalizedPropertiesInput(TcBaseObj):
    """
    The input structure for a list of business object info structure and a list of language locales.
    
    :var info: A list of desired business objects, property names to retrieve those properties in.
    :var locales: A list of language locale string: en_US , de_DE, zh_CN, etc.
    If locales is an empty array, will get all supported language from the list of Java-standard formatted name of
    languages that are supported by the system and specified in the BMIDE Global Constant Fnd0SelectedLocales.
    """
    info: List[GetLocalizedPropertiesInfo] = ()
    locales: List[str] = ()


@dataclass
class GetLocalizedPropertiesResponse(TcBaseObj):
    """
    The response structure for the getLocalizedProperties service operation.
    
    :var propertiesInfo: A list of response structure that holds business object, the property information with name,
    values, statuses and locale of the property.
    :var fullTranslationStatuses: A list of all the full translation statuses.
    :var serviceData: The service data object.
    """
    propertiesInfo: List[ObjectLocalizedPropertiesInfo] = ()
    fullTranslationStatuses: List[TranslationStatusInfo] = ()
    serviceData: ServiceData = None


@dataclass
class LocalizedPropertyNameValuesInfo(TcBaseObj):
    """
    A structure that holds property name and a list of LocalizedValuesInfo structure.
    
    :var propertyName: The property name string.
    :var propertyValues: A structure list that holds property values, locale and status information.
    """
    propertyName: str = ''
    propertyValues: List[LocalizedValuesInfo] = ()


@dataclass
class LocalizedValuesInfo(TcBaseObj):
    """
    A structure that holds property values, statuses and locale information.
    
    :var values: A list of property values.
    :var statuses: A list of the localization status.
    The status must be one of the following values:
    "TranslationStatusApproved","TranslationStatusPending","TranslationStatusInReview","TranslationStatusInvalid".
    :var locale: The name of the locale. For example: de_DE, zh_CN, etc.
    """
    values: List[str] = ()
    statuses: List[str] = ()
    locale: str = ''


@dataclass
class ObjectLocalizedPropertiesInfo(TcBaseObj):
    """
    The input structure for a list of business object, the property information with name, values, statuses and locale
    of the property.
    
    :var inputObject: The business object.
    :var propertyNameValues: A list of structure that holds property name and a list of LocalizedPropertyNameValuesInfo
    structure.
    """
    inputObject: BusinessObject = None
    propertyNameValues: List[LocalizedPropertyNameValuesInfo] = ()


@dataclass
class TranslationStatusInfo(TcBaseObj):
    """
    A struct that holds status from TranslationStatus enumeration, status display name and description.
    
    :var status: status value from TranslationStatus enumeration.
    :var displayName: Display name of the status.
    :var description: Description of the status.
    """
    status: TranslationStatus = None
    displayName: str = ''
    description: str = ''


class TranslationStatus(Enum):
    """
    TranslationStatus enumeration associated with the status.
    """
    Master = 'TranslationStatusMaster'
    Approved = 'TranslationStatusApproved'
    Pending = 'TranslationStatusPending'
    InReview = 'TranslationStatusInReview'
    Invalid = 'TranslationStatusInvalid'
