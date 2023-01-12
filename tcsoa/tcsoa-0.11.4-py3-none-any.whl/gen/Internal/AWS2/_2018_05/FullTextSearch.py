from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2015_10.FullTextSearch import PropInfo, SearchFilter2
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Awp0ModifyFTSSavedSearchInput(TcBaseObj):
    """
    Input structure for modifySavedSearchProperties service operation.
    
    :var pinSearch: Should the saved-search object be pinned? 
    Supported values are:
    -1 = Do not pin or unpin the saved-search.
    0 = Unpin the saved-search.
    1 = Pin the saved-search.
    :var receiveNotification: Should user receive notification if saved-search results change? 
    Supported values are:
    -1 = Do not remove or set notification.
    0 = Remove notification.
    1 = Set Notification.
    :var shareSavedSearch: Should the saved search be available to all users. 
    The awp0is_global_shared property on Awp0FullTextSavedSearch object indicates if the search is shared or not. 
    -1 = Do not change the value of set awp0is_global_shared property on Awp0FullTextSavedSearch object. 
    0 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to false.
    1 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to true.
    :var searchFilterMap: A map of category internal names and list of filters in each category. (string/list of
    SearchFilter). Categories are defined as typeName.propertyName For example:e.g WorkspaceObject.object_type. They
    can be a Teamcenter core type/property name or classification type/property name. In some cases, it can also be a
    non-Teamcenter type/property name constructed just for the purpose of filtering on a category that may be a
    composite of other categories.
    :var propInfo: A list of PropInfo which contains information about the objects and the properties to set.
    :var chartInputParameters: A map (<string, string>) containing chart input parameters.
    NOTE: Supported keys are: ("chartOn" : the current charted on category)A map containing chart input parameters.
    
    Categories are defined as typeName.propertyName, they can be be a Teamcenter core type/property name or
    classification type/property name. In some cases, it can also be a non-Teamcenter type/property name constructed
    just for the purpose of filtering on a category that may be a composite of other categories.
    """
    pinSearch: int = 0
    receiveNotification: int = 0
    shareSavedSearch: int = 0
    searchFilterMap: SearchFilterMap3 = None
    propInfo: List[PropInfo] = ()
    chartInputParameters: ChartInputParameters = None


@dataclass
class Awp0CreateFTSSavedSearchInput(TcBaseObj):
    """
    Input structure for createFullTextSavedSearch service operation.
    
    :var pinSearch: Should the saved search object be pinned? 
    Supported values are:
    -1 = Do no pin or unpin the saved search.
    0 = Unpin the saved search.
    1 = Pin the saved search.
    :var receiveNotification: Should client receive notification if saved-search result changes? 
    Supported values are:
    -1 = Do no set or remove notification for the saved search.
    0 = Remove notification.
    1 = Set notification.
    :var shareSavedSearch: Should the saved search be available to all users? 
    The awp0is_global_shared property on Awp0FullTextSavedSearch object indicates if the search is shared or not. 
    -1 = Do not change the value of set awp0is_global_shared property on Awp0FullTextSavedSearch object. 
    0 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to false.
    1 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to true.
    :var savedSearchName: The saved search name. Alphanumeric and special characters are allowed.
    :var searchString: The search string. Alphanumeric and special characters are allowed.
    :var searchFilterMap: A map of category internal names and list of filters in each category. (string/list of
    SearchFilter). Categories are defined as typeName.propertyName For example:e.g WorkspaceObject.object_type. They
    can be a Teamcenter core type/property name or classification type/property name. In some cases, it can also be a
    non-Teamcenter type/property name constructed just for the purpose of filtering on a category that may be a
    composite of other categories.
    :var overwriteExistingSearch: If false and if a Awp0FullTextSavedSearch object already exists for the user having
    same name, then this operation should return a partial error. If true and if a Awp0FullTextSavedsearch object
    already exists for the user having same name then this operation deletes the existing.
    :var chartInputParameters: A map <string, string> containing chart input parameters. 
    NOTE: Supported keys are:
    - chartOn: The current charted on category internal name (format of the value: TypeName.propertyName).
    
    
    
    Categories are defined as typeName.propertyName For example:e.g WorkspaceObject.object_type. They can be a
    Teamcenter core type/property name or classification type/property name. In some cases, it can also be a
    non-Teamcenter type/property name constructed just for the purpose of filtering on a category that may be a
    composite of other categories.
    """
    pinSearch: int = 0
    receiveNotification: int = 0
    shareSavedSearch: int = 0
    savedSearchName: str = ''
    searchString: str = ''
    searchFilterMap: SearchFilterMap3 = None
    overwriteExistingSearch: bool = False
    chartInputParameters: ChartInputParameters = None


"""
A map <string, string> containing chart input parameters. 
NOTE: Supported keys are:

chartOn: The current charted on category internal name (format of the value: TypeName.propertyName)
"""
ChartInputParameters = Dict[str, str]


"""
A map of category internal names and list of filters in each category. (string/list of SearchFilter)
"""
SearchFilterMap3 = Dict[str, List[SearchFilter2]]
