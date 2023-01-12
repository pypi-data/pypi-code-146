from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, ColumnConfig, ObjectsGroupedByProperty
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchFilter2(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Supported values are "StringFilter", "DateFilter",
    "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var colorValue: The color of the Search Filter.
    :var stringDisplayValue: The display value for a string filter. This field is applicable only if the
    "searchFilterType" field is set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter"
    :var endDateValue: The ending value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter"
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the searchFilterType
    is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: A flag that indicates if the filter was previously selected and used to filter the results.
    :var startEndRange: The interval used to generate a range facets. E.g for Date range facets, +1DAY, +1WEEK, +1MONTH
    , +1YEAR are acceptable values.  Note: Currently this value is not being used. To be supported in the future.
    """
    searchFilterType: str = ''
    stringValue: str = ''
    colorValue: str = ''
    stringDisplayValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class SearchResponse2(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResults: List of business objects obtained after performing a search.
    :var totalFound: Total number of business objects found.
    :var totalLoaded: Total number of business objects loaded.
    :var searchFilterMap2: A map (string, list of SearchFilter2) containing the list of search filters for each search
    filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var endIndex: Cursor end position for the results returned so far. This value, 'endIndex', correlates with
    'startIndex' in SearchInput.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap2: SearchFilterMap2 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig = None
    serviceData: ServiceData = None
    endIndex: int = 0


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap2 = Dict[str, List[SearchFilter2]]
