from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InternalContext(TcBaseObj):
    """
    The InternalContext structure represents the preference context values.
    
    :var contextName: Context name for the values.
    The default one is "Teamcenter". It can also be set to be used with NXManager, by setting the 'TC_Application'
    environment variable to UGMAN.
    
    :var value: List of values applicable for the context.
    """
    contextName: str = ''
    value: List[str] = ()


@dataclass
class InternalPreferenceDefinition(TcBaseObj):
    """
    Represents the definition for a preference.
    
    :var preferenceName: Name of the preference.
    :var preferenceCategory: Category of the preference.
    :var preferenceDescription: Description of the preference.
    :var preferenceScope: Scope of the preference.
    Valid values are "USER", "ROLE", "GROUP" or "SITE".
    :var preferenceType: Type of the preference.
    Valid values are "STRING", "LOGICAL", "INTEGER", "DOUBLE" or "DATE".
    :var isArray: Specifies if this preference takes multiple values.
    :var isDisabled: Specifies if this preference is enabled.
    """
    preferenceName: str = ''
    preferenceCategory: str = ''
    preferenceDescription: str = ''
    preferenceScope: str = ''
    preferenceType: str = ''
    isArray: bool = False
    isDisabled: bool = False


@dataclass
class InternalPreferenceInfo(TcBaseObj):
    """
    Contains the entire information about a preference: the definition is captured in the PreferenceDefinition
    structure and the values in the list of InternalContext structures.
    
    :var preferenceDefinition: The definition information.
    :var contextInformation: The contextual values.
    """
    preferenceDefinition: InternalPreferenceDefinition = None
    contextInformation: List[InternalContext] = ()


@dataclass
class InternalPreferencesInfo(TcBaseObj):
    """
    A list of InternalPreferenceInfo structures.
    
    :var prefsInfo: List of InternalPreferenceInfo structure.
    """
    prefsInfo: List[InternalPreferenceInfo] = ()


@dataclass
class PreferenceExportResponse(TcBaseObj):
    """
    The response received after an export operation.
    
    :var fileTicket: Ticket of the exported file present in the transient volume uploaded by the server.
    :var serviceData: Holds the list of errors during the operation.
    """
    fileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class PreferenceResponse(TcBaseObj):
    """
    Represents the preferences information.
    
    :var preferencesArray: List of preferences information, which contains preference definitions and values.
    :var serviceData: Holds the list of errors during the operation.
    """
    preferencesArray: List[InternalPreferencesInfo] = ()
    serviceData: ServiceData = None


@dataclass
class PreferencesDeleteInput(TcBaseObj):
    """
    The PreferencesDeleteInput structure represents the information about a preference that
    will be passed as input to the delete method.
    
    :var preferenceScope: Scope of the preference. Scope can be "USER", "ROLE", "GROUP" or "SITE".
    :var preferenceName: Name of the preference.
    :var object: Object to which the preferences have to be assigned. This can be
    a User, Role or Group. If no value is specified, preferences from the
    current session are considered based on the scope. To be able to delete
    preferences for the site, the user must be a DBA. To be able to delete
    preferences for the role and site, the user must be a GA or DBA.
    """
    preferenceScope: str = ''
    preferenceName: str = ''
    object: BusinessObject = None


@dataclass
class PreferencesExportInput(TcBaseObj):
    """
    The input required to export preferences.
    
    :var preferenceScope: Location (as seen from the current logged-in user) from where to export preferences.
    Valid values are "USER", "ROLE", "GROUP" or "SITE".
    :var categoryNames: List of category names which are to be considered by the operation.
    If no value is provided, the category filter is ignored and preferences from all categories are considered by the
    operation.
    """
    preferenceScope: str = ''
    categoryNames: List[str] = ()


@dataclass
class PreferencesImportInput(TcBaseObj):
    """
    Specifies the input to be considered for the import operation.
    
    :var preferenceScope: Location where to import the preferences. 
    Valid values are "USER", "ROLE", "GROUP" or "SITE".
    :var fileTicket: Ticket of the input XML file in the transient volume uploaded by the client.
    :var categoryNames: List of category names which are to be considered by the operation. If no value is provided,
    the category filter is ignored and preferences from all categories are considered by the operation.
    :var importAction: Specifies what to do when the preference already exists. Can be "SKIP", "OVERRIDE", or "MERGE".
    """
    preferenceScope: str = ''
    fileTicket: str = ''
    categoryNames: List[str] = ()
    importAction: str = ''
