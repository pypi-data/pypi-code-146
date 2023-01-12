from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import SavedSearch
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Awp0UpdateAdvancedSavedSearchInput(TcBaseObj):
    """
    Input structure for updateAdvancedSavedSearch operation.
    
    :var stringValueInputKeyValuePairs: A map (string, string) to hold string value nputs. Valid keys are followings:
    - "savedSearchUid" The uid of saved search to update.
    - "savedSearchName" The saved search name.
    - "clientId" This unique ID is used to identify return data elements and partial errors associated with this input
    structure.
    
    
    :var boolValueInputKeyValuePairs: A map (string, bool) to hold bool value inputs. Valid keys are followings:
    - "shareSavedSearch" Allow other users to view and execute the saved search. If true, other users can see and
    execute the saved search; otherwise not visible to other users. Only applicable for owning user.
    - "favorite" Favorite saved search of current user. If true, it&rsquo;s a favorite saved search of current user;
    otherwise a regular one.
    - "pinToHome" Pin to home for current user. If true, pin the saved search to home; otherwise not pin to home.
    - "override" If false and a SavedSearch object having same name owned by current user already exists, then partial
    error returned. If true and a SavedSearch object having same name owned by current user already exists then delete
    the existing SavedSearch object and create a new one. Only applicable for owning user.
    
    """
    stringValueInputKeyValuePairs: StringValueInputKeyValueMap = None
    boolValueInputKeyValuePairs: BoolValueInputKeyValueMap = None


@dataclass
class SavedSearchCriteria(TcBaseObj):
    """
    A strucuture represents a saved search critieria.
    
    :var criteriaName: Name of critiera. e.g. "fnd0CurrentLocationCode"
    :var criteriaValue: Value of criteria. e.g. "us"
    :var criteriaDisplayValue: Display value of critiera. e.g. "United States"
    """
    criteriaName: str = ''
    criteriaValue: str = ''
    criteriaDisplayValue: str = ''


@dataclass
class Awp0AdvancedSavedSearchResponse(TcBaseObj):
    """
    Contians a list of newly created saved searches and the service data containing partial errors if any.
    
    :var savedSearchList: A List of SavedSearch objects created or modified by a service operation.
    :var serviceData: Returned service data.
    """
    savedSearchList: List[SavedSearch] = ()
    serviceData: ServiceData = None


@dataclass
class Awp0CreateAdvancedSavedSearchInput(TcBaseObj):
    """
    Input structure for createAdvancedSavedSearch operation.
    
    :var stringValueInputKeyValuePairs: A map (string, string) to hold string value inputs, valid keys are followings:
    - "savedSearchName" The name of saved search.
    - "referencingSavedQuery" The saved query this saved search is created based off.
    - "targetFolder" The target Folder the saved search will be created in.
    - "clientId" This unique ID is used to identify return data elements and partial errors associated with this input
    structure.
    
    
    :var boolValueInputKeyValuePairs: A map (string, bool) to hold bool value inputs, valid keys are followings:
    - "shareSavedSearch" Allow other users to view and execute the saved search.  If true, other users can see and
    execute the saved search; otherwise not visible to other users.
    - "favorite" Favorite saved search of current user. If true, it&rsquo;s a favorite saved search of current user;
    otherwise a regular one.
    - "pinToHome" Pin to home for current user. Valid values are:If true, pin the saved search to home; otherwise not
    pin to home.
    - "override" Valid values are: True or False. If false and a SavedSearch object having same name owned by current
    user already exists, then partial error returned. If true and a SavedSearch object having same name owned by
    current user already exists then delete the existing SavedSearch object and create a new one.
    
    
    :var savedSearchCriteria: The search critiera (user inputs) used to create the saved search, which will be used
    when executing the saved search.
    """
    stringValueInputKeyValuePairs: StringValueInputKeyValueMap = None
    boolValueInputKeyValuePairs: BoolValueInputKeyValueMap = None
    savedSearchCriteria: List[SavedSearchCriteria] = ()


"""
Key value pair represents bool value input.
"""
BoolValueInputKeyValueMap = Dict[str, bool]


"""
Key value pair represents string value input.
"""
StringValueInputKeyValueMap = Dict[str, str]
