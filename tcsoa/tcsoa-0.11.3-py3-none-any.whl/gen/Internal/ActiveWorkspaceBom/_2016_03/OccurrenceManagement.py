from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Effectivity, Awb0SavedBookmark, Awb0Element, Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import SearchSortCriteria2, Criteria
from typing import Dict, List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.OccurrenceManagement import ProductInfoData
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReplaceElementResponse(TcBaseObj):
    """
    'ReplaceElementResponse' contains a list of 'replacable' Awb0Element if dry run is specified.
    
    :var replacableElements: List of Awb0Element which can be replaced with given 
    'replacement'.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: Contains the list of updated Awb0Element(s) in updated list and 
    partial error if any.
    :var reloadContent: Indicates if content should be reloaded. Set to true if input element is replaced with element
    of different type else false.
    """
    replacableElements: List[Awb0Element] = ()
    columnConfig: ColumnConfig = None
    serviceData: ServiceData = None
    reloadContent: bool = False


@dataclass
class ReplaceInput(TcBaseObj):
    """
    This structure contains 'replacement' to be set as underlying object of the list of 'elements'.
    
    :var elements: List of Awb0Element whose underlying object to be replaced 
    with 'replacement'.
    :var replacement: The BusinessObject to be replaced for input 'elements'. It can 
    be ItemRevision or GenericDesignElement.
    :var productContextInfo: The Awb0ProductContextInfo object containing configuration 
    information.
    :var requestPref: Map of preference names and values pairs 
    (string / list of string ). Allowed preference name is dryRun. Values can be any valid string. Preference names and
    values are case sensitive.
    :var columnConfigInput: The column config input criteria to get the effective column configurations.
    """
    elements: List[Awb0Element] = ()
    replacement: BusinessObject = None
    productContextInfo: Awb0ProductContextInfo = None
    requestPref: RequestPreference4 = None
    columnConfigInput: ColumnConfigInput = None


@dataclass
class SubsetInput2(TcBaseObj):
    """
    SubsetInput2 contains list of recipe and productInfo to fetch updated recipes and filters.
    
    :var productInfo: Awb0ProductContextInfo object containing the product with its configuration information. The
    product and configuration is used to fetch subset filters.
    :var recipe: List of Criteria as held by client, this is used to update filters which are currently applied.
    :var searchSortCriteria: A list of criterion to be used for sorting the filtered results.
    :var searchFilterFieldSortType: Type of sorting that needs to be performed on the search filters. Valid values are
    "Alphabetical", and "Priority".
    :var requestPref: Map of preference names and values pairs (string / list of string ). Allowed preference name is
    selectedFilter. Values can be any valid string. Preference names and values are case sensitive.
    """
    productInfo: Awb0ProductContextInfo = None
    recipe: List[Criteria] = ()
    searchSortCriteria: List[SearchSortCriteria2] = ()
    searchFilterFieldSortType: str = ''
    requestPref: RequestPreference3 = None


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI.  It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that  was used to finalize the columns to be returned back.
    Supported values are:
    "Intersection", "Union" and "Configured"
    :var columnsToExclude: List of  columns which should be excluded from the final list being returned. The value
    provided should be in the format "TypeName.PropertyName". Both type name and property name should be internal
    values. 
    For example: ItemRevision.sequence_id, where '.' is the delimiter
    :var elementTypesForArrange: List of element types.
    :var columns: Ordered list of column details.
    :var hasColumnsChanged: Indicates whether table display should be udpated.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columnsToExclude: List[str] = ()
    elementTypesForArrange: List[str] = ()
    columns: List[ColumnDefInfo] = ()
    hasColumnsChanged: bool = False


@dataclass
class ColumnConfigInput(TcBaseObj):
    """
    Contains input information required to retrieve UI column configurations from the Teamcenter database.
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database.  This value must match the value of fnd0ClientName property. 
    For example: The client name for Active Workspace is "AWClient"
    :var hostingClientName: Specifies the name of a hosting client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases.  This value must match a value of the fnd0ClientName property.  
    For example: If client A is integrated with client B and the user can invoke client B commands from within client
    A, the input would specify client A as hosting client and client B as the client. If the caller wanted native
    commands for client A, client A would be specified as client and hosting client would be empty.
    :var operationType: The operation that  needs to be applied to finalize the columns to be returned back.
    Supported values are:
    "Intersection" - Gets the intersection of the columns for the types found in search results.
    "Union" - Gets all the columns for the types found in search results.
    "Configured" - Gets all the columns defined for requested scope irrespective of types in the search results . If it
    does not find any configuration at the specified scope it will  search up in the order of scopes User, Role, Group
    and Site.
    :var fetchColumnConfig: Indicates whether column configuration to be fetched or not, this is for future use.
    """
    clientName: str = ''
    hostingClientName: str = ''
    operationType: str = ''
    fetchColumnConfig: bool = False


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be hidden and  the
    column sort order .
    
    :var typeName: The business object type for the value displayed in the column.  This can be any valid Teamcenter
    business object type.
    :var propertyName: The property name for the value displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: If true,  the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort.
    Sort priority value will be zero for columns not marked for sorting.
    :var sortDirection: How the columns are sorted.  Supported values are: "Ascending" and "Descending". This value
    will be empty if the column is not marked for sorting.
    """
    typeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


@dataclass
class AddToBookmarkInputData2(TcBaseObj):
    """
    The structure contains object to be added as child of input parentElement or productContext.
    
    :var productsToBeAdded: The products to be added to the Awb0AutoBookmark object associated with the input
    Awb0SavedBookmark object. The product can be of Item or ItemRevision type.
    :var bookmark: The Awb0SavedBookmark object. The products will be added to the Awb0AutoBookmark object associated
    with this object.
    :var columnConfigInput: The column config input criteria to get the effective column configurations.
    """
    productsToBeAdded: List[BusinessObject] = ()
    bookmark: Awb0SavedBookmark = None
    columnConfigInput: ColumnConfigInput = None


@dataclass
class EffectivityInput(TcBaseObj):
    """
    This structure contains 'effectivities' to be attached to the list of 'elements'.
    
    :var elements: List of Awb0Element for which effectivities to be added or 
    removed.
    :var effectivities: List of Effectivity objects which are added or removed  to/from  
    elements.
    :var addOrRemove: Indicates whether to add or remove Effectivity(s). When true, 
    Effectivity is added. Otherwise, Effectivity is removed.
    """
    elements: List[Awb0Element] = ()
    effectivities: List[Effectivity] = ()
    addOrRemove: bool = False


@dataclass
class AddToBookmarkResp2(TcBaseObj):
    """
    List of the ProductInfoData objects associated with the products that were added. The ServiceData has the modified
    Awb0SavedBookmark object.
    
    :var addedProductsInfo: The list of structures containing the information associated to the products added to the
    Awb0Autobookmark.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The ServiceData containing modified Awb0SavedBookmark and partial error if any.
    """
    addedProductsInfo: List[ProductInfoData] = ()
    columnConfig: ColumnConfig = None
    serviceData: ServiceData = None


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive.
"""
RequestPreference3 = Dict[str, List[str]]


"""
The map which can have a key and value pair, used to specify the mode of replace operation. The key and value are case sensitive.
"""
RequestPreference4 = Dict[str, List[str]]
