from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOrResetUIColumnConfigInput(TcBaseObj):
    """
    Contains input information required to retrieve or reset UI column configurations from the Teamcenter database.
    
    :var scope: The scope value is used to apply the UI configurations for that scope. The valid values are :
    "Site" - Returns the configuration defined for the site. 
    "Group" - Returns the configuration defined for a specific Teamcenter Group.
    "Role" - Returns the configuration defined for a specific Teamcenter Role.
    "User" - Returns the configurations defined for a specific Teamcenter User.
    "LoginUser" - Returns the configurations defined for the current login user.
    :var scopeName: The name of a valid Teamcenter scope. Valid scopes are "Site", "Group", "Role", "User",
    "LoginUser". ScopeName should be empty when scope is set for "Site" or "LoginUser". For other scopes use as follows
    
    User    -   User name as per the user's profile
    Group  -   Valid group defined in Organization
    Role    -   Valid role defined in Organization
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property.
    
    Ex: The client name for Active Workspace is "AWClient".
    :var hostingClientName: Specifies the name of a hosting client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property. 
    
    For example, if client A is integrated with client B and the user can invoke client B commands from within client
    A, the input to getUiConfigs would specify client A as hosting client and client B as the client. If the caller
    wanted native commands for client A, client A would be specified as client and hosting client would be empty.
    :var resetColumnConfig: If True, it will reset the column configurations at the "LoginUser" scope. Reset action is
    valid only for "LoginUser" scope.
    :var columnConfigQueryInfos: List of column config query information. This has the client scope URI, type names and
    operation type to be used and query for the valid columns.
    :var businessObjects: List of business objects for which the additional properties found as new columns need to be
    loaded.
    """
    scope: str = ''
    scopeName: str = ''
    clientName: str = ''
    hostingClientName: str = ''
    resetColumnConfig: bool = False
    columnConfigQueryInfos: List[ColumnConfigQueryInfo] = ()
    businessObjects: List[BusinessObject] = ()


@dataclass
class GetOrResetUIColumnConfigResponse(TcBaseObj):
    """
    This structure returns information to the client about column configurations. The ServiceData contains information
    about errors encountered during processing.
    
    :var clientName: The client for which the configurations are applicable.
    :var columnConfigurations: List of column configurations data.
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    """
    clientName: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    serviceData: ServiceData = None


@dataclass
class GetVisibleCommandsInfo(TcBaseObj):
    """
    Contains input information required to retrieve the commands that are visible from the Teamcenter database.
    
    :var clientScopeURI: The client scope URI represents location.sublocation in Active Workspace. For example,
    Fnd0ClientScope::fnd0ClientScopeURI. If empty, the UI Configuration for all client scopes are returned.
    :var selectionInfo: List of objects selected by the user in the client.
    :var commandInfo: List of commands.
    :var commandContextInfo: List of command context name value pairs, for example: "isHosted"="true",
    "productContext"=productContextUid
    """
    clientScopeURI: str = ''
    selectionInfo: List[SelectionInfo] = ()
    commandInfo: List[CommandInfo] = ()
    commandContextInfo: List[CommandContextInfo] = ()


@dataclass
class GetVisibleCommandsResponse(TcBaseObj):
    """
    This structure returns information to the client about the commands that are visible. The ServiceData contains
    information about errors encountered during processing.
    
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    :var visibleCommandsInfo: List of visible commands.
    """
    serviceData: ServiceData = None
    visibleCommandsInfo: List[CommandInfo] = ()


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back.
    Valid values are:
    "Intersection", "Union" and "Configured"
    :var columns: Ordered list of column details. The columns will be listed in ascending order of priority.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SaveColumnConfigData(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definition information.
    
    :var scope: The scope value is used to apply the UI configurations for that scope. 
    The Valid values are :
    "LoginUser" - Returns the current configuration defined for the current login user. 
    "scopeName" should be empty when scope is set for LoginUser.
    Note: Other scope values "Site", "Group" and "Role" are not supported.
    :var scopeName: The name of a valid Teamcneter scope. For "Site" and "LoginUser" scope, this value should be empty.
    Note: Added this for future. To be used when code starts supporting saving of column configurations for "Site",
    "Group" and "Role" scopes.
    :var clientScopeURI: The unique name of the client scope containing configurations.
    :var columnConfigId: The unique identifier for the column configuration.
    :var columns: Ordered list of column information.
    """
    scope: str = ''
    scopeName: str = ''
    clientScopeURI: str = ''
    columnConfigId: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SelectionInfo(TcBaseObj):
    """
    This structure contains the list of objects selected by the user in the client.
    
    :var selectedObjects: The objects selected by the user in the client.
    :var parentSelectionIndex: Parent selection for the object. For example, for cut operation, it is the selected
    parent object.
    :var contextName: Optional context name, for example, for cut operation, it is the relation name between parent
    object and child object.
    """
    selectedObjects: List[BusinessObject] = ()
    parentSelectionIndex: int = 0
    contextName: str = ''


@dataclass
class ColumnConfigData(TcBaseObj):
    """
    This structure returns information about the column configuration definitions for a scope, hosting client and
    client scope.
    
    :var scope: The scope that is used to retrieve the UI configurations.
    :var scopeName: The scope name for which the column data is applicable.
    :var hostingClient: The name of hosting client for which the list of column configurations is applicable. This
    value must correspond to the value of the property fnd0ClientName for an Fnd0Client object in the Teamcenter
    database.
    :var clientScopeURI: The client scope for which the list of column configurations is applicable. This must match a
    value of fnd0ClientScopeURI which is the unique identifier of a client scope (Fnd0ClientScope).
    :var columnConfigurations: List of column configuration details.
    """
    scope: str = ''
    scopeName: str = ''
    hostingClient: str = ''
    clientScopeURI: str = ''
    columnConfigurations: List[ColumnConfig] = ()


@dataclass
class ColumnConfigQueryInfo(TcBaseObj):
    """
    This structure contains the client scope URI to be used and query for its associated column configurations. The
    type names and operation type are used to identify the final list of columns to be returned back.
    
    :var clientScopeURI: The unique name of the client scope containing column configurations.
    Ex: "Awp0SearchResults" for global search.
    :var operationType: The operation that needs to be applied to finalize the columns to be returned back.
    Valid values are:
    "Intersection" - Gets the intersection of the columns for the types passed in.
    "Union" - Gets all the columns of the types passed in.
    "Configured" - Gets all the columns defined for requested scope irrespective of types passed in. If it does not
    find any configuration at the specified scope it will search up in the order of scopes User, Role, Group and then
    Site. No need to pass type names if need to fetch all configured columns.
    :var typeNames: List of type names(internal names) for which the columns needs to be fetched. In search case these
    will the type names of the results found.
    :var columnsToExclude: List of columns which should be excluded from the final list being returned. The value
    provided should be in the format "typeName.propertyName" . Both type name and property name should be internal
    values. 
    Ex: ItemRevision.sequence_id , where '.' Is the delimiter
    """
    clientScopeURI: str = ''
    operationType: str = ''
    typeNames: List[str] = ()
    columnsToExclude: List[str] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be hidden and the column
    sort priority and direction.
    
    :var typeName: The business object type for the value displayed in the column.
    :var propertyName: The name of the property corresponding to the values displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: True if the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var sortDirection: How the columns are sorted. Valid values are: "Ascending" and "Descending". This value will be
    empty if the column is not marked for sorting.
    """
    typeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


@dataclass
class CommandContextInfo(TcBaseObj):
    """
    This structure contains the command context name and value
    
    :var contextName: Context Name which is to be used to evaluate visibility of the command
    :var contextValue: Context value that forms a valid pair with the contextName.
    """
    contextName: str = ''
    contextValue: str = ''


@dataclass
class CommandInfo(TcBaseObj):
    """
    This structure contains the Ids of command and command collection that are visible for the indicated client.
    
    :var commandCollectionId: The command collection Id.
    :var commandId: The command Id.
    """
    commandCollectionId: str = ''
    commandId: str = ''
