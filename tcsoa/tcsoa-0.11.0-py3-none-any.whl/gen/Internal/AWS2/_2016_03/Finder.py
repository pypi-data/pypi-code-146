from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetClassificationPropsResponse(TcBaseObj):
    """
    Holds the classification properties details returned by the getClassificationProps() operation.
    
    :var wsoClsPropDetailsMap: A map (string, ClsObjectDetails )of WorkspaceObject UID and the classification object
    details.
    :var clsAttrDetailsMap: A map  (int, ClsAttrDetails) of Classification attributes ID and its corresponding metadata.
    :var svcData: The Service Data.
    """
    wsoClsPropDetailsMap: WsoClsPropDetailsMap = None
    clsAttrDetailsMap: ClsAttrDetailsMap = None
    svcData: ServiceData = None


@dataclass
class ClsAttrDetails(TcBaseObj):
    """
    Structure describing classification attribute details.
    
    :var attributeId: The unique ID of the Classification attribute.
    :var attributeName: Name of the Classification attribute.
    """
    attributeId: int = 0
    attributeName: str = ''


@dataclass
class ClsAttrValueDetails(TcBaseObj):
    """
    Structure containing the attribute ID and corresponding value(s).
    
    :var attrId: The unique ID of an attribute.
    :var attrValue: List of the stored value(s) for the attrId.
    """
    attrId: int = 0
    attrValue: List[str] = ()


@dataclass
class ClsObjectDetails(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObjId: Alphanumeric ID of the Classification object, as defined for the object during its creation.
    :var clsObject: Reference of Classification object(icm0).
    :var unitSystem: Unit system of measure in which the Classification object is stored in.
    :var clsObjClassId: The unique ID of Classification class as defined for the object during its creation.
    :var clsObjClassName: Classification class Name.
    :var attributeValues: A list of ClsAttrValueDetails objects containing attribute IDs and their corresponding values
    for above classification object.
    """
    clsObjId: str = ''
    clsObject: BusinessObject = None
    unitSystem: str = ''
    clsObjClassId: str = ''
    clsObjClassName: str = ''
    attributeValues: List[ClsAttrValueDetails] = ()


@dataclass
class ObjectsGroupedByProperty(TcBaseObj):
    """
    A structure containing an internal property name and a map of objects to the property group id. It also contains a
    list of unmatched objects which don't match any group.
    
    :var internalPropertyName: The internal name of the property used for grouping.
    :var groupedObjectsMap: Map (BusinessObject, list of string) of business object and its associated grouping.
    :var unmatchedObjectList: List of unmatched business objects.
    """
    internalPropertyName: str = ''
    groupedObjectsMap: ObjectPropertyGroupingMap = None
    unmatchedObjectList: List[BusinessObject] = ()


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back.
    Supported values are:
    "Intersection", "Union" and "Configured".
    :var columns: List of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SaveColumnConfigData(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definitions information.
    
    :var scope: The scope value is used to apply the UI configurations for that scope.  Supported values are :
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
    columns: List[ColumnDefInfo] = ()


@dataclass
class SearchFilter(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Supported values are "StringFilter", "DateFilter",
    "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
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
    , +1YEAR are acceptable values. 
    Note: Currently this value is not being used. This is added for future.
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
    A structure containing input search criteria.
    
    :var providerName: The name of the search provider. This is the RuntimeBusinessObject type name.
    :var searchCriteria: A map (string, string) used to perform the search. 
    For full text search, the key is "searchString", the value is  "*".
    For advanced search, the key can be
    "queryID" ,
    "quickSearchAttributeValue",
    "searchID",
    "typeOfSearch", "QUICK_SEARCH" or "ADVANCED_SEARCH", the value is unique identifier.
    :var startIndex: The start index to return the search results.
    :var maxToReturn: The maximum number of search results to return.If zero, no search results are returned; however,
    other information such as total results found and filters details are returned.
    :var maxToLoad: The maximum number of search results to load.
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field. The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". e.g WorkspaceObject.object_type, the value in the map is the value of the search filter.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response.
    Supported values are: "Alphabetical","Priority".
    :var attributesToInflate: A list of attributes to inflate (extract the details).
    :var internalPropertyName: The internal name of the property used for grouping.
    """
    providerName: str = ''
    searchCriteria: StringMap = None
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: SearchFilterMap = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: str = ''
    attributesToInflate: List[str] = ()
    internalPropertyName: str = ''


@dataclass
class SearchResponse(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var searchResults: List of business objects obtained after performing a search.
    :var totalFound: Total number of business objects found.
    :var totalLoaded: Total number of business objects loaded.
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field based on the search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var endIndex:  Cursor end position for the results returned so far.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap: SearchFilterMap = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig = None
    serviceData: ServiceData = None
    endIndex: int = 0


@dataclass
class SearchSortCriteria(TcBaseObj):
    """
    The criteria to use to sort the results.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be performed - 'ASC' or 'DESC'.
    """
    fieldName: str = ''
    sortDirection: SortDirection = None


@dataclass
class ColumnConfigInput(TcBaseObj):
    """
    Contains input information required to retrieve UI column configurations from the Teamcenter database.
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property. 
    For example: The client name for Active Workspace is "AWClient".
    :var hostingClientName: Specifies the name of a hosting client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property.
    
    For example: If client A is integrated with client B and the user can invoke client B commands from within client
    A, the input to getUiConfigs would specify client A as hosting client and client B as the client. If the caller
    wanted native commands for client A, client A would be specified as client and hosting client would be empty.
    :var clientScopeURI: The unique name of the client scope containing column configurations.
    For example: "Awp0SearchResults" is the client scope URI for search location.
    :var operationType: The operation that needs to be applied to finalize the columns to be returned back.
    Valid values are:
    "Intersection" - Gets the intersection of the columns for the types found in search results.
    "Union" - Gets all the columns for the types found in search results.
    "Configured" - Gets all the columns defined for requested scope irrespective of types passed in. If it does not
    find any configuration at the specified scope it will search up in the order of scopes User, Role, Group and Site.
    No need to pass type names if need to fetch all columns.
    :var columnsToExclude: List of columns which should be excluded from the final list being returned. The value
    provided should be in the format "TypeName.PropertyName". Both type name and property name should be internal
    values. 
    For example: ItemRevision.sequence_id, where '.' is the delimiter
    """
    clientName: str = ''
    hostingClientName: str = ''
    clientScopeURI: str = ''
    operationType: str = ''
    columnsToExclude: List[str] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be hidden and the column
    sort order.
    
    :var typeName: The business object type for the value displayed in the column. This can be any valid Teamcenter
    business object type.
    :var propertyName: The property name for the value displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: If true, the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort.
    Sort priority value will be zero for columns not marked for sorting.
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    """
    typeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


class SortDirection(Enum):
    """
    An enumeration indicating whether the sorting needs to be performed in ascending or descending order.
    """
    ASC = 'ASC'
    DESC = 'DESC'


"""
A map containing a list of propertyGroupID for each BusinessObject. For multi-valued properties, a single business object may be associated with multiple property group IDs.
"""
ObjectPropertyGroupingMap = Dict[BusinessObject, List[str]]


"""
The list of Classification attribute Ids and their descriptor.
"""
ClsAttrDetailsMap = Dict[int, ClsAttrDetails]


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap = Dict[str, List[SearchFilter]]


"""
Map from string to string.
"""
StringMap = Dict[str, str]


"""
The map of workspace object(WSO) to its classification properties.

- Primary key : Reference of the classified workspace object(WorkspaceObject) that was used to get the classification properties.
- Values : Details of classification object references associated with the classified workspace object(WorkspaceObject) referenced in the primary key.


"""
WsoClsPropDetailsMap = Dict[str, ClsObjectDetails]
