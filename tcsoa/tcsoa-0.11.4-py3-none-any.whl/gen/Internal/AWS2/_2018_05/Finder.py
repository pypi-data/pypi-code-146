from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2017_06.Finder import ColumnConfig2
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, SearchSortCriteria, ObjectsGroupedByProperty
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.AWS2._2017_12.Finder import SearchFilter4


@dataclass
class SearchCursor(TcBaseObj):
    """
    A structure containing cursor
    
    :var startIndex: Indicates the Cursor start position for the search result returned so far.
    :var endIndex: Indicates the Cursor end position for the search result returned so far
    :var startReached: If true, the first page of the results has been reached.
    :var endReached: If true, the last page of the results has been reached.
    """
    startIndex: int = 0
    endIndex: int = 0
    startReached: bool = False
    endReached: bool = False


@dataclass
class SearchInput2(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var providerName: The name of the search provider. This is the RuntimeBusinessObject type name.
    :var searchCriteria: A map (string, string) used to perform the search. For full text search, the key is
    "searchString", the value is "*". For advanced search, the key can be "queryID",  "quickSearchAttributeValue",
    "searchID", "typeOfSearch", "QUICK_SEARCH" or "ADVANCED_SEARCH", the value is the unique identifier.
    :var attributesToInflate: A list of attributes to inflate (extract the details).
    :var internalPropertyName: The internal name of the property used for grouping.
    :var cursor: Cursor object used in the search
    :var focusObjUid: Uid of the Object to focus to
    :var pagingType: The type of paging operation. Valid values are GetCurrentPage, GetNextPage, GetPreviousPage
    :var maxToReturn: The maximum number of search results to return. If zero, no search results are returned; however,
    other information such as total results found and filters details are returned.
    :var maxToLoad: The maximum number of search results to load.
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". e.g WorkspaceObject.release_statuses, the value in the map is the value of  the search
    filter.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response.
    Supported values are: "Alphabetical", "Priority".
    """
    providerName: str = ''
    searchCriteria: StringMap2 = None
    attributesToInflate: List[str] = ()
    internalPropertyName: str = ''
    cursor: SearchCursor = None
    focusObjUid: str = ''
    pagingType: str = ''
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: SearchFilterMap5 = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: str = ''


@dataclass
class SearchResponse5(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResultsJSON: Search results in JSON Format. With this, Client can directly bind the view model
    properties JSON to the view.
    :var totalFound: Total number of view model business objects found.
    :var cursor: Cursor for the results returned so far.
    :var searchFilterCategoriesUnpopulated: A list of empty search filter categories.
    :var totalLoaded: Total number of view model business objects loaded.
    :var searchFilterMap5: A map (string, list of Awp0::Soa::Internal::AWS2::_2017_12::Finder::SearchFilter34)
    containing the list of search filters for each search filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var objectsGroupedByProperty: The The structure, Awp0::Soa::Internal::AWS2::_2016_03::ObjectPropertyGroupingMap
    containing an internal property name and a map of objects to the property group id. It also contains a list of
    unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var additionalSearchInfoMap: A generic map (string/list of strings) that can be used to send additional search
    information to the consumer. 
    
    Supported key values are:
    searchTermsToHighlight - used to indicate which Search Terms need to be highlighted
    """
    searchResultsJSON: str = ''
    totalFound: int = 0
    cursor: SearchCursor = None
    searchFilterCategoriesUnpopulated: List[SearchFilterField] = ()
    totalLoaded: int = 0
    searchFilterMap5: SearchFilterMap5 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig2 = None
    serviceData: ServiceData = None
    additionalSearchInfoMap: StringVectorMap = None


@dataclass
class FacetSearchInput(TcBaseObj):
    """
    The FacetSearchInput is based on existing structure SearchInput of performSearchViewModel3. It contains search
    criteria and search filter information.
    
    :var providerName: The name of the search provider. This is the RuntimeBusinessObject type name.
    :var searchCriteria: A map (string, string) used to perform the search. 
    For full text search, the key is "searchString", the value is input text. For example, ("searchString" : "*" | "?"
    | "string"). 
    
    For advanced search, the supported key/values are: 
    ("typeOfSearch" : "QUICK_SEARCH" or "ADVANCED_SEARCH");
    ("queryUID" :  UID to a WorkspaceObject);
    ("searchID" :  UID to a WorkspaceObject);
    ("quickSearchAttributeValue" : search string).
    
    For example, an advance search might be:
    "typeOfSearch" : "QUICK_SEARCH";
    "queryUID" :  "UID";
    "searchID" : "UID";
    "quickSearchAttributeValue": "*"
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: WorkspaceObject.object_type, the value in the map is the value of the search
    filter.
    :var startIndex: The start index to return the facet values. This value must be zero or positive. Error will be
    returned for a negative value.
    :var maxToReturn: The maximum number of facet values to return  This value must be positive i.e. greater than 0,
    else error will be returned.
    """
    providerName: str = ''
    searchCriteria: StringMap2 = None
    searchFilterMap: SearchFilterMap5 = None
    startIndex: int = 0
    maxToReturn: int = 0


@dataclass
class FacetSearchResponse(TcBaseObj):
    """
    A response structure containing facet values for the filter category in input searchFilterMap.
    
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: WorkspaceObject.object_type, the value in the map is the value of the search
    filter.
    :var hasMoreFacetValues: If true, client can make subsequent call for next set of facet values.
    :var endIndex: Cursor end position for the facet values returned so far. This value, 'endIndex' will be used as
    'startIndex' in FacetSearchInput for subsequent call.
    :var serviceData: The service data object.
    """
    searchFilterMap: SearchFilterMap5 = None
    hasMoreFacetValues: bool = False
    endIndex: int = 0
    serviceData: ServiceData = None


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap5 = Dict[str, List[SearchFilter4]]


"""
Map from string to string.
"""
StringMap2 = Dict[str, str]


"""
A map of string to list of strings
"""
StringVectorMap = Dict[str, List[str]]
