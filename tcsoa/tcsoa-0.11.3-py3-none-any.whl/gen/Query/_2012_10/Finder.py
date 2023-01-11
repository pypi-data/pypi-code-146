from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchFilter(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter";.
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
    :var startEndRange: The 'gap' used to generate the start and end values
    """
    searchFilterType: SearchFilterType = None
    stringValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class SearchFilterField(TcBaseObj):
    """
    A structure containing details about a search filter field.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0


@dataclass
class SearchInput(TcBaseObj):
    """
    A structure containing input search criteria
    
    :var providerName: The name of the search provider.  This is the RuntimeBusinessObject type name.
    :var searchCriteria: The criteria used to perform search (string/string). For example, for object set search, the
    search criteria are parentUid and object set source string.
    :var startIndex: The start index to return the search results
    :var maxToReturn: The maximum number of search results to return
    :var maxToLoad: The maximum number of search results to load
    :var searchFilterMap: The map (string,list of SearchFilter) containing the list of search filters for each search
    filter field.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response. The
    acceptable values are: "Alphabetical","Priority".
    :var attributesToInflate: The list of attributes to inflate.
    """
    providerName: str = ''
    searchCriteria: StringMap = None
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: SearchFilterMap = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: SearchFilterFieldSortType = None
    attributesToInflate: List[str] = ()


@dataclass
class SearchResponse(TcBaseObj):
    """
    A service response structure containing search results.
    
    :var searchResults: The list of business objects obtained after performing a search.
    :var totalFound: The total number of business objects found.
    :var totalLoaded: The total number of business objects loaded.
    :var searchFilterMap: The map (string,list of SearchFilter) containing the list of search filters for each search
    filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var serviceData: The service data object.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap: SearchFilterMap = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    serviceData: ServiceData = None


@dataclass
class SearchSortCriteria(TcBaseObj):
    """
    The criteria to use to sort the results.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be perfomed - 'ASC' or 'DESC'.
    """
    fieldName: str = ''
    sortDirection: SortDirection = None


class SearchFilterFieldSortType(Enum):
    """
    An enumeration to determine how fields used in filters need to be sorted. The fields can be sorted alphabetically
    in ascending order or in priority order from highest to lowest.
    """
    Alphabetical = 'Alphabetical'
    Priority = 'Priority'


class SearchFilterType(Enum):
    """
    An enumeration for different types of search filters like string, date, numeric.
    """
    StringFilter = 'StringFilter'
    DateFilter = 'DateFilter'
    NumericFilter = 'NumericFilter'


class SortDirection(Enum):
    """
    An enumeration indicating whether the sorting needs to be performed in ascending or descending order.
    """
    ASC = 'ASC'
    DESC = 'DESC'


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap = Dict[str, List[SearchFilter]]


"""
Map from string to string
"""
StringMap = Dict[str, str]
