from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Query._2012_10.Finder import SearchFilterField, SearchSortCriteria
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ObjectPropertyGroupInput(TcBaseObj):
    """
    A structure containing an internal property name, a list of PropertyGroupingValue  objects and a list of Business
    Objects.
    
    :var internalPropertyName: The internal name for the property used for grouping
    :var propertyValues: List of start and end property values for the internalPropertyName.
    :var objectList: List of business objects to be grouped. This is typically a subset of search results that need to
    be grouped.
    """
    internalPropertyName: str = ''
    propertyValues: List[PropertyGroupingValue] = ()
    objectList: List[BusinessObject] = ()


@dataclass
class ObjectsGroupedByProperty(TcBaseObj):
    """
    A structure containing an internal property name and a map of objects to the property group id. It also contains a
    list of unmatched objects which dont match any group.
    
    :var internalPropertyName: The internal name of the property.
    :var groupedObjectsMap: Map  (business object, list of strings) of selected business object and its associated
    grouping names.
    :var unmatchedObjectList: List of unmatched business objects.
    """
    internalPropertyName: str = ''
    groupedObjectsMap: ObjectPropertyGroupingMap = None
    unmatchedObjectList: List[BusinessObject] = ()


@dataclass
class ObjectsGroupedByPropertyResponse(TcBaseObj):
    """
    A structure containing list of ObjectPropertyGrouping objects and service data.
    
    :var groupedObjectsList: List of ObjectPropertyGrouping objects.
    :var serviceData: The service data.
    """
    groupedObjectsList: List[ObjectsGroupedByProperty] = ()
    serviceData: ServiceData = None


@dataclass
class PropertyGroupingValue(TcBaseObj):
    """
    A structure containing start and end values for a specific property.  The end value is used for range comparisons
    if populated
    
    :var propertyGroupID: Unique Identifier used by client to identify the group.
    :var startValue: String representation of the value for the property. For ranges, this is the start value for the
    range. If the client code is dealing with specific value types (int, double, etc.) the client code can use the
    appropriate client APIs to convert values to a string representation e.g Property::toFloatString,
    Property::toIntString, Property::toDateString, etc. On the server side, they can be converted back to the
    appropriate value types using the corresponding APIs e.g Property::parseFloat, Property::parseInt,
    Property::parseDate, etc.
    :var endValue: String representation of the end value for the property. This is optional and is populated only for
    ranges. It represents the end value of the range.See the startValue description for how the client and server code
    can convert from and to the specific value types.
    """
    propertyGroupID: str = ''
    startValue: str = ''
    endValue: str = ''


@dataclass
class SearchFilter2(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter"
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var stringDisplayValue: The display value for a string filter. This field is applicable only if the
    "searchFilterType" field is set to "StringFilter".
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
    :var selected: A flag that indicates if the filter was previously selected and used to filter the results. 
    :var startEndRange: The 'gap' used to generate the start and end values
    """
    searchFilterType: str = ''
    stringValue: str = ''
    stringDisplayValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class SearchInput2(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var providerName: The name of the search provider.  This is the RuntimeBusinessObject type name.
    :var searchCriteria: The criteria used to perform search (string/string). For example, for object set search, the
    search criteria are parentUid and object set source string.
    :var startIndex: The start index to return the search results
    :var maxToReturn: The maximum number of search results to return. If value is  zero, no search results are
    returned; however, other information such as total results found and filters details are returned.
    :var maxToLoad: The maximum number of search results to load
    :var searchFilterMap: The map (string,list of SearchFilter )containing the list of search filters for each search
    filter field.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response. The
    acceptable values are: "Alphabetical","Priority".
    :var attributesToInflate: A list of attributes to inflate.
    :var internalPropertyName: The internal name of the property used for grouping.
    """
    providerName: str = ''
    searchCriteria: StringMap2 = None
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: SearchFilterMap2 = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: str = ''
    attributesToInflate: List[str] = ()
    internalPropertyName: str = ''


@dataclass
class SearchResponse2(TcBaseObj):
    """
    A service response structure containing search results
    
    :var searchResults: The list of business objects obtained after performing a search. 
    :var totalFound: The total number of business objects found
    :var totalLoaded: The total number of business objects loaded
    :var searchFilterMap: The map (string,list of SearchFilter )containing the list of search filters for each search
    filter field
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var serviceData: The service data object.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which don't match any group.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap: SearchFilterMap2 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    serviceData: ServiceData = None
    objectsGroupedByProperty: ObjectsGroupedByProperty = None


"""
A map containing a list of propertyGroupID for each BusinessObject. For multi-valued properties, a single business object may be associated with multiple property group IDs.
"""
ObjectPropertyGroupingMap = Dict[BusinessObject, List[str]]


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap2 = Dict[str, List[SearchFilter2]]


"""
Map from string to string
"""
StringMap2 = Dict[str, str]
