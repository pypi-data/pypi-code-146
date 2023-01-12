from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import UserSession
from dataclasses import dataclass


@dataclass
class GetAvailableWorkspacesResponse(TcBaseObj):
    """
    Response of getAvailableWorkspaces operation.
    
    :var workspacesViewModel: The list of workspace view model objects in JSON format which can be bound to declarative
    view.
    :var serviceData: The service data object.
    """
    workspacesViewModel: str = ''
    serviceData: ServiceData = None


@dataclass
class GetTableViewModelPropertiesIn(TcBaseObj):
    """
    Input for getTableViewModelProperties
    
    :var objectUids: The list of the object UIDs for which the Table ViewModel properties have to be fetched.
    :var requestPreference: Key value pair (string, list of string) passed to the GetTableViewModelPropRequestPref
    operation to control the behavior. Supported keys:
    1. "typesToInclude" : Internal type names  to be included along with types discovered during the operation.
    
    2. "supportsCardinality" value could be "true" or "false".
    :var columnConfigInput: Input to fetch the column configuration.
    """
    objectUids: List[str] = ()
    requestPreference: GetTableViewModelPropRequestPref = None
    columnConfigInput: ColumnConfigInput = None


@dataclass
class GetTableViewModelPropsOut(TcBaseObj):
    """
    Output containing the JSON string representation for the objects for which the properties were fetched and the
    column configuration data.
    
    :var viewModelPropertiesJsonString: JSON string that contains the view model properties, the schema of JSON string
    is defined in getDeclarativeStyleSheet2 service operation.
    :var columnConfig: The column configuration data.
    """
    viewModelPropertiesJsonString: str = ''
    columnConfig: ColumnConfig = None


@dataclass
class GetTableViewModelPropsResp(TcBaseObj):
    """
    GetTableViewModelProperties response
    
    :var output: The model objects with the dynamic compound properties inflated and the column configuration
    applicable for the input objects.
    :var serviceData: Service Data
    """
    output: GetTableViewModelPropsOut = None
    serviceData: ServiceData = None


@dataclass
class GetViewModelProps2Response(TcBaseObj):
    """
    Objects for which properties could be successfully retrieved are returned as JSON string. Any failures will be
    returned with the input object mapped to the error message in the ServiceData list of partial errors.
    
    :var viewModelPropertiesJsonString: JsonSON string that contains the view model properties, the schema of JSON
    string is defined in getDeclarativeStyleSheet2 service operation.
    :var serviceData: Service data
    """
    viewModelPropertiesJsonString: str = ''
    serviceData: ServiceData = None


@dataclass
class LoadViewModelForEditing2Response(TcBaseObj):
    """
    Response of LoadViewModelForEditing2 operation
    
    :var viewModelObjectsJsonStrings: Json strings that contain the ViewModelObject structures which provide
    information about the editable status of the properties passed in the input. This information can be used by client
    to show which properties as editable. The ViewModelObjectJsonString is also used in getDeclarativeStyleSheet2
    operation
    :var serviceData: Partial errors are returned in the Service Data. The following partial errors may be returned:
    302021: The input object is not modifiable.
    302022: The property is not modifiable. 
    302024. The traversal path of dynamic compound property has changed
    """
    viewModelObjectsJsonStrings: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ColumnConfig(TcBaseObj):
    """
    The column configuration data.
    
    :var columnConfigId: Column configuration ID.
    :var operationType: Operation type used for determining columns. Supported values are: "Union" and "Intersection".
    :var columns: List of available columns.
    :var typesForArrange: The valid Teamcenter types used for fetching the columns.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()
    typesForArrange: List[str] = ()


@dataclass
class TCSessionAndAnalyticsInfo(TcBaseObj):
    """
    - userSession The user session object
    - extraInfoOut Map of key/value pairs (string/string). Some/all/none of the following keys and values are returned,
    depending on what was passed in extraInfoIn:
    - TCServerVersion The version of the Teamcenter server.
    - hasProjects "true" or "false" depending on whether the user has projects
    - AWC_StartupPreferences This contains list of preferences to be retrieved at startup by the Active workspace
    client from the Teamcenter server.
    - AWC_Startuptypes List of types to be loaded at start up by the Active workspace client from the Teamcenter server.
    - DefaultDateFormat The default date format required.
    - AWServerVersion The version of the Active workspace
    - typeCacheLMD UTC formatted last modified date for Type cache Dataset.
    - WorkspaceId Workspace Id for current Active workspace user session.
    - AWC_PostLoginStages This preference represents list of post login stages in the sequence to be displayed in the
    Active worksapace after successful authentication.
    - analyticsData This contains an instance of AnalyticsData required to hold software analytics data for logged in
    user. 
    - serviceData The serviceData.
    
    
    
    :var userSession: The user session object
    :var extraInfoOut: extraInfoOut Map of key/value pairs (string/string). Some/all/none of the following keys and
    values are returned, depending on what was passed in extraInfoIn:
    - TCServerVersion The version of the Teamcenter server.
    - hasProjects "true" or "false" depending on whether the user has projects
    - AWC_StartupPreferences This contains list of preferences to be retrieved at startup by the Active workspace
    client from the Teamcenter server.
    - AWC_Startuptypes List of types to be loaded at start up by the Active workspace client from the Teamcenter server.
    - DefaultDateFormat The default date format required.
    - AWServerVersion The version of the Active workspace
    - typeCacheLMD UTC formatted last modified date for Type cache Dataset.
    - WorkspaceId Workspace Id for current Active workspace user session.
    - AWC_PostLoginStages This preference represents list of post login stages in the sequence to be displayed in the
    Active worksapace after successful authentication.
    
    
    :var analyticsData: This contains an instance of AnalyticsData required to hold software analytics data for logged
    in user.
    :var serviceData: The serviceData.
    """
    userSession: UserSession = None
    extraInfoOut: SessionExtraInfo = None
    analyticsData: AnalyticsData = None
    serviceData: ServiceData = None


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
    For example: ItemRevision.sequence_id, where '.' is the delimiter.
    """
    clientName: str = ''
    hostingClientName: str = ''
    clientScopeURI: str = ''
    operationType: str = ''
    columnsToExclude: List[str] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Column Definition
    
    :var displayName: The display name for the value displayed in the column header.
    :var associatedTypeName: The business object type for the value displayed in the column. This can be any valid
    Teamcenter business object type.
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
    displayName: str = ''
    associatedTypeName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    sortDirection: str = ''


@dataclass
class AnalyticsData(TcBaseObj):
    """
    This contains an instance of AnalyticsData required to hold software analytics data for logged in user.
    
    :var isDataCollectionEnabled: This value for preference TC_ProductExcellenceProgram to indicate the software
    analytics should be enabled or not.  If data collection is off then the server will not send any other information
    and an instance of AnalyticsData will be empty, this value is set to false.
    :var useInternalServer: Where the analytice data is logged:. If true, send analytics data to analytics internal
    server; otherwise, send analytics data to analytics cloud based server (AWS).
    :var burstTimeInterval: The time interval at which software analytics data will be sent to the SA server. This
    value is a recommendation since all clients cannot implement a burst interval other than zero.
    :var analyticsExtraInfo: Map of key\value pairs (string, string). These are optional fields sent by the server and
    will be sent to the analytics site as is. The intent is that these fields, if present, will be sent to the SA
    server retaining their name and value.
    """
    isDataCollectionEnabled: bool = False
    useInternalServer: bool = False
    burstTimeInterval: int = 0
    analyticsExtraInfo: AnalyticsExtraInfo = None


"""
Map of key\value pairs (string, string). These are optional fields returned to the client for the purpose of forwarding to the analytics site. There is no guarantee as to the contents or ordering of this map. The contents may vary across platforms or Teamcenter versions. The values in the map should NOT be interpreted by the client or used for client side logic since there is no guarantee on the content.
"""
AnalyticsExtraInfo = Dict[str, str]


"""
The map of (string, string) filter parameters. 
Following are the possible values.
1. Key "scope", Value could be "session" or "all". If the value is passed as "session", only the workspaces which match other filter parameters and apply to current user session (group role combination) will be returned. If it is passed as "all", all the workspaces in the system matching other filters will be returned regardless of existing user session.
2. Key "group", Value needs to be the group ID to which associated workspaces needs to be loaded. Key "group" is optional. If it is not present in operation input, all the workspaces matching other filters will be returned. 
3. Key "role", Value needs to be the role ID to which associated workspaces needs to be loaded. Key "role" is optional. If it is not present in operation input, all the workspaces matching other filters will be returned.
"""
FilterParams = Dict[str, str]


"""
Key value pair passed to the getTableViewModelProperties operation to control the behavior.
"""
GetTableViewModelPropRequestPref = Dict[str, List[str]]


"""
Map of key-value pairs. Returned value depends on what was passed in extraInfoIn:
TCServerVersion The version of the Teamcenter server.
hasProjects true or false depending on whether the user has projects
"""
SessionExtraInfo = Dict[str, str]


"""
String map
"""
StringMap8 = Dict[str, str]
