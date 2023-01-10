from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, SearchSortCriteria, ObjectsGroupedByProperty
from tcsoa.gen.Internal.AWS2._2018_05.Finder import SearchCursor
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.AWS2._2017_12.Finder import SearchFilter4


@dataclass
class SaveColumnConfigData2(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definitions information.
    
    :var scope: The scope value is used to apply the UI configurations for that scope. Supported values are :
    "LoginUser" - Returns the current configuration defined for the current login user. 
    Note: Other scope values "Site", "Group" and "Role" are not supported.
    :var scopeName: The name of a valid Teamcenter scope.
    For example "Group" scope, scopeName can be "dba","Engineering". 
    For "LoginUser" scope, this value should be empty.
    :var clientScopeURI: The unique name of the client scope containing configurations.
    Supported values are: 
    "Awp0SearchResults" for global search
    "fnd0Inbox" for inbox
    "fnd0alltasks" for all inbox tasks
    "fnd0mytasks" for my inbox tasks
    "fnd0surrogatescope" for surrogate inbox tasks
    "Fnd0Report" for report
    "Awp0ObjectNavigation" for object navigation
    "Awp0AdvancedSearch" for advanced search
    :var columnConfigId: The unique identifier for the column configuration.
    Ex: "searchResultsColConfig" for search location.
    :var columns: Ordered list of column information.
    """
    scope: str = ''
    scopeName: str = ''
    clientScopeURI: str = ''
    columnConfigId: str = ''
    columns: List[ColumnDefInfo3] = ()


@dataclass
class ColumnConfig3(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back. Supported values are:
    "Intersection", "Union" and "Configured".
    :var columns: List of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo3] = ()


@dataclass
class SearchInput3(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var providerName: The name of the search provider. This is the RuntimeBusinessObject type name.
    :var searchCriteria: A map (string, string) used to perform the search. 
    For full text search, the key is "searchString", the value is "*".
    For advanced search, the key can be
    "queryID" ,
    "quickSearchAttributeValue",
    "searchID",
    "typeOfSearch", "QUICK_SEARCH" or "ADVANCED_SEARCH", the value is unique identifier.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response.
    Supported values are: "Alphabetical" and "Priority".
    :var attributesToInflate: A list of attributes to inflate (extract the details).
    :var internalPropertyName: The internal name of the property used for grouping.
    :var columnFilters: A list of filters to be applied on the columns.
    :var cursor: Cursor object used in the search.
    :var focusObjUid: Uid of the Object to focus to
    :var pagingType: The type of paging operation. Valid values are GetCurrentPage, GetNextPage, GetPreviousPage.
    :var startIndex: The start index to return the search results.
    :var maxToReturn: The maximum number of search results to return.If zero, no search results are returned; however,
    other information such as total results found and filters details are returned.
    :var maxToLoad: The maximum number of search results to load.
    :var searchFilterMap6: A map (string, list of SearchFilter4) containing the list of search filters for each search
    filter field.The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: WorkspaceObject.release_statuses, the value in the map is the value of the
    search filter.
    :var searchSortCriteria: The criteria to use to sort the results.
    """
    providerName: str = ''
    searchCriteria: StringMap3 = None
    searchFilterFieldSortType: str = ''
    attributesToInflate: List[str] = ()
    internalPropertyName: str = ''
    columnFilters: List[FilterCriteriaInput] = ()
    cursor: SearchCursor = None
    focusObjUid: str = ''
    pagingType: str = ''
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap6: SearchFilterMap6 = None
    searchSortCriteria: List[SearchSortCriteria] = ()


@dataclass
class SearchResponse6(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResultsJSON: Search results in JSON Format. With this, Client can directly bind the view model
    properties JSON to the view.
    :var totalFound: Total number of view model business objects found.
    :var additionalSearchInfoMap: A generic map (string/list of strings) that can be used to send additional search
    information to the consumer. 
    
    Supported key values are:
    searchTermsToHighlight - used to indicate which Search Terms need to be highlighted.
    :var cursor: Cursor for the results returned so far.
    :var searchFilterCategoriesUnpopulated: A list of empty search filter categories.
    :var totalLoaded: Total number of view model business objects loaded.
    :var searchFilterMap6: A map (string, list of SearchFilter4) containing the list of search filters for each search
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
    additionalSearchInfoMap: StringVectorMap2 = None
    cursor: SearchCursor = None
    searchFilterCategoriesUnpopulated: List[SearchFilterField] = ()
    totalLoaded: int = 0
    searchFilterMap6: SearchFilterMap6 = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig3 = None
    serviceData: ServiceData = None
    endIndex: int = 0


@dataclass
class ColumnDefInfo3(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be hidden and the column
    sort order, fliters applied on a column, filterDefinition and the datatype of the property.
    
    :var displayName: The display name for the value displayed in the column header.
    :var typeName: The business object type for the value displayed in the column. This can be any valid Teamcenter
    business object type.
    :var isFilteringEnabled: If true, column filtering is enabled on this column; otherwise, column filtering is not
    supported on this column.
    :var dataType: The data type of the property for the given column.
    :var isFrozen: If true, the table has columns frozen until this column; otherwise, this column is not frozen.
    :var propertyName: The property name for the value displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: If true, the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    :var filterValue: The filter criteria that is applied for current operation.
    :var filterDefinitionKey: This string that represents a custom filter definition which the clients can define in
    the client view model.
    """
    displayName: str = ''
    typeName: str = ''
    isFilteringEnabled: bool = False
    dataType: str = ''
    isFrozen: bool = False
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''
    filterValue: FilterCriteriaResponse = None
    filterDefinitionKey: str = ''


@dataclass
class FilterCriteriaInput(TcBaseObj):
    """
    A structure representing the input filter criteria for columns.
    
    :var columnName: The internal name of the property on which column filtering is applied.
    :var operation: This operation specifies the type of column filter operation applied. The supported operations are:
    "CONTAINS", "EQUAL", "GREATER THAN", "LESS THAN" and "BETWEEN".
    :var values: The filter values are the criteria entered by the user on the client. These are not a fixed set of
    values like operation.
    """
    columnName: str = ''
    operation: str = ''
    values: List[str] = ()


@dataclass
class FilterCriteriaResponse(TcBaseObj):
    """
    A response structure representing the column filter criteria.
    
    :var operation: This operation specifies the type of column filter operation applied. The supported operations are
    "CONTAINS", "EQUAL", "GREATER THAN", "LESS THAN" and "BETWEEN".
    :var values: These are the filter values saved in the database from the previous filter use case executed by the
    user.
    """
    operation: str = ''
    values: List[str] = ()


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap6 = Dict[str, List[SearchFilter4]]


"""
Map from string to string.
"""
StringMap3 = Dict[str, str]


"""
A map of string to list of strings.
"""
StringVectorMap2 = Dict[str, List[str]]
