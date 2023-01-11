from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PreferenceDefinition(TcBaseObj):
    """
    The PreferenceDefinition structure represents the definition for a preference
    in Teamcenter.
    
    :var preferenceName: Name of the preference.
    :var preferenceCategory: Category of the preference.
    :var preferenceDescription: Description of the preference.
    :var preferenceScope: Scope of the preference. It can be "USER", "ROLE", "GROUP" or "SITE".
    :var preferenceType: Type of the preference. It can be "STRING", "LOGICAL", "INTEGER", "DOUBLE" or "DATE".
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
class PreferenceInfo(TcBaseObj):
    """
    Holds the complete information about a preference: its definition is captured in the PreferenceDefinition
    structure, and its values in the list of Context structures. 
    
    
    :var preferenceDefinition: A structure holding the definition of the preference.
    :var contextInformation: A list of Context structures, each representing the values for a given context.
    """
    preferenceDefinition: PreferenceDefinition = None
    contextInformation: List[Context] = ()


@dataclass
class PreferencesInfo(TcBaseObj):
    """
    Contains a list of PreferenceInfo structures.
    
    :var prefsInfo: List of PreferenceInfo structure.
    """
    prefsInfo: List[PreferenceInfo] = ()


@dataclass
class PreferencesSetInput(TcBaseObj):
    """
    Input to be provided for setting preferences.
    
    :var preferenceScope: Location of the preference.
    :var inputPrefs: Preferences to be set.
    :var object: Object to which the preferences have to be assigned.
    This can be a User, Role or Group. If no value is specified, preferences are set for the current session based on
    the scope. 
    To be able to set preferences for the site, the user must be a system administrator.
    To be able to set preferences for a group or a role, the user must be group administrator or a system administrator.
    """
    preferenceScope: str = ''
    inputPrefs: PreferencesInfo = None
    object: BusinessObject = None


@dataclass
class Context(TcBaseObj):
    """
    Represents the preference context values.
    
    :var contextName: Context name for the values. 
    
    The default one is "Teamcenter". It can also be set to be used with NXManager, by setting the TC_Application
    environment variable to UGMAN. 
    
    :var value: List of values applicable for the context.
    """
    contextName: str = ''
    value: List[str] = ()
