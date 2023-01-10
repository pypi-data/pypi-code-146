from __future__ import annotations

from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FullTranslationStatus(TcBaseObj):
    """
    Fully defines a translation status: its associated enumeration, display name and description.
    
    :var status: TranslationStatus associated with the status
    :var statusName: Display name of the status
    :var statusDescription: Description of the status
    """
    status: TranslationStatus = None
    statusName: str = ''
    statusDescription: str = ''


@dataclass
class Language(TcBaseObj):
    """
    Contains information about a language
    
    :var languageCode: The name of the desired locale. The valid locale name should be in the format as outlined in the
    Java Standard Language (i.e. en_US for English, United States).
    :var languageName: The localized language name
    """
    languageCode: str = ''
    languageName: str = ''


@dataclass
class LanguageResponse(TcBaseObj):
    """
    Information about the list of languages
    
    :var languageList: An ordered list of languages
    :var serviceData: Any partial errors that may occur when filling this request
    """
    languageList: List[Language] = ()
    serviceData: ServiceData = None


@dataclass
class TranslationStatusResponse(TcBaseObj):
    """
    Response associated to some LanguageInformation operation calls
    
    :var fullTranslationStatuses: List of all the full translation statuses
    :var serviceData: The 'ServiceData'.
    """
    fullTranslationStatuses: List[FullTranslationStatus] = ()
    serviceData: ServiceData = None


class TranslationStatus(Enum):
    """
    Defines the status of a translation: master language, approved, pending, in-review and invalid.
    """
    Master = 'TranslationStatusMaster'
    Approved = 'TranslationStatusApproved'
    Pending = 'TranslationStatusPending'
    InReview = 'TranslationStatusInReview'
    Invalid = 'TranslationStatusInvalid'
