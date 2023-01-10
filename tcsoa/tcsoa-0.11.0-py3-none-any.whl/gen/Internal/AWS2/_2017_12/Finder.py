from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2017_06.Finder import ColumnConfig2
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, ObjectsGroupedByProperty
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchFilter4(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Supported values are: "StringFilter", "DateFilter",
    "NumericFilter", "RadioFilter".
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
    :var selected: If true, the Search Filter was previously selected; otherwise, the Search Filter was not previously
    selected.
    :var startEndRange: The interval used to generate a range facets. For example: for Date range facets, +1DAY,
    +1WEEK, +1MONTH , +1YEAR are acceptable values. Note: Currently this value is not being used. To be supported in
    the future.
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
class SearchResponse4(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResultsJSON: Search results in JSON Format. With this, Client can directly bind the view model
    properties JSON to the view.
    :var totalFound: Total number of view model business objects found.
    :var totalLoaded: Total number of view model business objects loaded.
    :var searchFilterMap4: A map (string, list of SearchFilter3) containing the list of search filters for each search
    filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var endIndex: Cursor end position for the results returned so far. This value, 'endIndex', correlates with
    'startindex' in SearchInput.
    """
    searchResultsJSON: str = ''
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap4: SearchFilterMap4 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig2 = None
    serviceData: ServiceData = None
    endIndex: int = 0


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap4 = Dict[str, List[SearchFilter4]]
