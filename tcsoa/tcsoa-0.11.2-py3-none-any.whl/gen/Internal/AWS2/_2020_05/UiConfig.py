from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetNamedColumnConfigsResponse(TcBaseObj):
    """
    The response structure for the getNamedColumnConfigs service operation.
    
    :var namedColumnConfigsJSON: A JSON string containing the information about the named column configuration(s).
    :var serviceData: The service data object.
    """
    namedColumnConfigsJSON: str = ''
    serviceData: ServiceData = None


@dataclass
class NamedColumnConfigInput(TcBaseObj):
    """
    Contains input information required to retrieve UI named and un-named column configurations from the Teamcenter
    database.
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property. 
    For example: The client name for Active Workspace is "AWClient".
    :var clientScopeUri: The unique name of the client scope containing column configurations. 
    
    Example: "Awp0SearchResults" is the client scope URI for search
    :var columnConfigName: The name of the column configuration.
    
    Example: "Search Results" for search location.
    :var columnConfigId: The unique identifier for the column configuration.
    Ex: "searchResultsColConfig" for search location.
    :var columnsToExclude: List of columns which should be excluded from the final list being returned. The value
    provided should be in the format "TypeName.PropertyName". Both type name and property name should be internal
    values. 
    For example: ItemRevision.sequence_id, where '.' is the delimiter.
    """
    clientName: str = ''
    clientScopeUri: str = ''
    columnConfigName: str = ''
    columnConfigId: str = ''
    columnsToExclude: List[str] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
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
    :var filterDefinitionKey: The filter criteria that is applied for current operation.
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
    filterValue: FilterCriteria = None
    filterDefinitionKey: str = ''


@dataclass
class FilterCriteria(TcBaseObj):
    """
    A structure representing the column filter criteria.
    
    :var operation: This operation specifies the type of column filter operation applied. The supported operations are
    "CONTAINS", "EQUAL", "GREATER THAN", "LESS THAN" and "BETWEEN".
    :var values: A list of filter values saved in the database from the previous filter use case executed by the user.
    """
    operation: str = ''
    values: List[str] = ()


"""
Map from string to string.
"""
StringMap = Dict[str, str]
