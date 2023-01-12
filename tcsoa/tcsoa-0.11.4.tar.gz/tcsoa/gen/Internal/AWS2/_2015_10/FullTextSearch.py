from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0FullTextSavedSearch
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Awp0FullTextSavedSearchInputObject(TcBaseObj):
    """
    Input structure for createFullTextSavedSearch service operation.
    
    :var pinSearch: Should the saved search object be pinned? Supported values are:
    -1 = Do no pin or unpin the saved search.
    0 = Unpin the saved search
    1 = Pin the saved search
    :var receiveNotification: Should client receive notification if saved-search result changes? Supported values are:
    -1 = Do no set or remove notification for the saved search.
    0 = Remove notification.
    1 = Set notification.
    :var shareSavedSearch: Should the saved search be available to all users? The awp0is_global_shared property on
    Awp0FullTextSavedSearch object indicates if the search is shared or not.  
    -1 =  Do not change the value of set awp0is_global_shared property on Awp0FullTextSavedSearch object. 
    0 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to false
    1 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to true
    :var savedSearchName: The saved search name. Alphanumeric and special characters are allowed.
    :var searchString: The search string. Alphanumeric and special characters are allowed.
    :var searchFilterMap: A map of category internal names and list of filters in each category. (string/list of 
    SearchFilter).
    :var override: If false and if a Awp0FullTextSavedSearch object already exists for the user having same name, then
    this operation should return a partial error. If true and if a Awp0FullTextSavedsearch object already exists for
    the user having same name then this operation deletes the existing.
    """
    pinSearch: int = 0
    receiveNotification: int = 0
    shareSavedSearch: int = 0
    savedSearchName: str = ''
    searchString: str = ''
    searchFilterMap: SearchFilterMap2 = None
    override: bool = False


@dataclass
class Awp0FullTextSavedSearchInputObject2(TcBaseObj):
    """
    Input structure for modifySavedSearchProperties service operation.
    
    :var pinSearch: Should the saved-search object be pinned? Supported values are:
    -1 =  Do not pin or unpin the saved-search
    0 = Unpin the saved-search
    1 = Pin the saved-search
    :var receiveNotification: Should user receive notification if saved-search results change? Supported values are:
    -1 = Do not remove or set notification
    0 = Remove notification
    1 = Set Notification
    :var shareSavedSearch: Should the saved search be available to all users. The awp0is_global_shared property on
    Awp0FullTextSavedSearch object indicates if the search is shared or not.  
    -1 =  Do not change the value of set awp0is_global_shared property on Awp0FullTextSavedSearch object. 
    0 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to false
    1 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to true
    :var searchFilterMap: A map of category internal names and list of filters in each category. (string/list of
    SearchFilter).
    :var propInfo: A list of PropInfo which contains information about the objects and the properties to set.
    """
    pinSearch: int = 0
    receiveNotification: int = 0
    shareSavedSearch: int = 0
    searchFilterMap: SearchFilterMap2 = None
    propInfo: List[PropInfo] = ()


@dataclass
class Awp0FullTextSavedSearchResponse(TcBaseObj):
    """
    List of newly created saved searchesand the service data containing partial errors if any.
    
    :var savedSearchList: List of Awp0FullTextSavedSearch objects created or modified by this service operation.
    :var serviceData: Service data.
    """
    savedSearchList: List[Awp0FullTextSavedSearch] = ()
    serviceData: ServiceData = None


@dataclass
class NameValueStruct(TcBaseObj):
    """
    This structure holds property names and values for each property.
    
    :var name: Name of the property.
    :var values: Property values.
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class PropInfo(TcBaseObj):
    """
    This structure holds information about object & its timestamp and property information.
    
    :var object: Awp0FullTextSavedSearch object.
    :var properties: A list of property information.
    """
    object: BusinessObject = None
    properties: List[NameValueStruct] = ()


@dataclass
class SearchFilter2(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var endDateValue: The ending value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: A flag that indicates if the filter was previously selected and used to filter the search results.
    This field is populated on the service response and is ignored on the service input.
    :var startEndRange: The 'gap' used to generate the start and end values.
    """
    searchFilterType: SearchFilterType2 = None
    stringValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


class SearchFilterType2(Enum):
    """
    An enumeration for different types of search filters like string, date, numeric.
    """
    SearchStringFilter = 'SearchStringFilter'
    SearchDateFilter = 'SearchDateFilter'
    SearchNumericFilter = 'SearchNumericFilter'


"""
A map of category internal names and list of filters in each category. (string/list of  SearchFilter).
"""
SearchFilterMap2 = Dict[str, List[SearchFilter2]]
