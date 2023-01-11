from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0CommandCollection, Fnd0Client, Fnd0AbstractCommand, Fnd0ClientScope
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetUIConfigInput(TcBaseObj):
    """
    Contains input information requiredto retrieve UI configurations from the Teamcenter database.
    
    :var clientScopeURIs: List of client scope URIs representing, for example location.sublocation in Active Workspace.
    (Fnd0ClientScope::fnd0ClientScopeURI). If empty, the UI Configuration for all client scopes are returned.
    :var scope: The scope of the desired UI configuration information. This includes the name of the scope (i.e. a
    user, group or role) and scope query parameter information.
    :var client: Client information including client name and hosting client name.
    """
    clientScopeURIs: List[str] = ()
    scope: ScopeInput = None
    client: ClientInput = None


@dataclass
class GetUIConfigResponse(TcBaseObj):
    """
    This structure returns information to the client about column configuration and command applicability. The
    ServiceData contains information about errors encountered during processing.
    
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    :var uiConfigInfo: List of configuration information including command and column information
    """
    serviceData: ServiceData = None
    uiConfigInfo: List[ClientConfigurations] = ()


@dataclass
class SaveColumnConfigData(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definition information.
    
    :var scope: The scope for which the column data is applicable.  This includes the name of the scope (i.e. a user,
    group or role) and the save scope parameter information.
    :var clientScopeURI: The unique name of the client scope containing configurations.
    :var columnConfigId: The identifier for the column configuration.
    :var sortDirection: Sort order for the columns. Valid values are Ascending and Descending.
    :var columns: Ordered list of column information.
    """
    scope: SaveScopeInput = None
    clientScopeURI: str = ''
    columnConfigId: str = ''
    sortDirection: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SaveCommandCollectionInfo(TcBaseObj):
    """
    This structure contains information to save for a command collection.
    
    :var collectionId: Unique identifier of the command collection.
    :var configInfo: Configuration changes for the command collection.
    """
    collectionId: str = ''
    configInfo: List[SaveCommandConfigInfo] = ()


@dataclass
class SaveCommandConfigData(TcBaseObj):
    """
    This structure contains information about the command configuration definitions for a client scope URI.
    
    :var scopes: List of scope names for which the command configuration for which the changes are application.  If the
    site scope should be changed scopeName should be empty.
    :var saveCommandCollectionInfo: List of command collections changes.  Each change in this will be applied to each
    scope specified in the scope names list.
    """
    scopes: List[SaveScopeInput] = ()
    saveCommandCollectionInfo: List[SaveCommandCollectionInfo] = ()


@dataclass
class SaveCommandConfigInfo(TcBaseObj):
    """
    Configuration information which indicates if a command or command collection is being hidden or unhidden.
    
    :var isCollection: True if id is the id of a command collection.  False if id is a command.
    :var id: The unique identifier of a command or command collection.
    :var hidden: True if the command or command collection should be hidden.
    """
    isCollection: bool = False
    id: str = ''
    hidden: bool = False


@dataclass
class SaveScopeInput(TcBaseObj):
    """
    SaveScopeInput structure contains information including scope name and details about scope applicability.  The
    value in scopeName should be empty if the value in param refers to Site or LoginUser.
    
    :var scopeName: The name of a valid Teamcenter scope.
    :var saveScopeParam: The save scope that is used to apply some types of UI configurations. Valid values
    are:Site-Save configuration to the Teamcenter site. The scope name should be empty. Group-Save the configuration
    for a Teamcenter Group. Role-Save the configuration for a Teamcenter Role. User-Save the configuration for a
    Teamcenter User. LoginUser-Save the configuration for the current login user. The scope name should be empty.
    """
    scopeName: str = ''
    saveScopeParam: str = ''


@dataclass
class SaveUiConfigurations(TcBaseObj):
    """
    Contains two lists; one specifying column configuration information to save and the other specifying command
    configuraiton information to save.
    
    :var columnConfigurations: List of column configuration information.
    :var commandConfigurations: List of command configuration data.
    """
    columnConfigurations: List[SaveColumnConfigData] = ()
    commandConfigurations: List[SaveCommandConfigData] = ()


@dataclass
class ScopeInput(TcBaseObj):
    """
    Contains scope input information including scope name and scope query param.
    
    :var scopeName: The name of a scope.  For Site and current login user, this value should be empty.
    :var scopeQueryParam: The query scope that is used to retrieve the UI configurations.  Valid values are Site,
    Group, Role, User, LoginUser, and AvailableForLoginUser. Site returns the configuration defined for the site. Group
    returns the configuration defined for a specific Teamcenter Group. Role returns the configuration defined for a
    specific Teamcenter Role. User returns the configurations defined for a specific Teamcenter User. LoginUser returns
    the current configuration defined for the current login user. AvailableForLoginUser returns all the configurations
    available for the current login user.   scopeName should be empty when scopeQueryParam is set for Site, LoginUser
    or AvailableForLoginUser.
    """
    scopeName: str = ''
    scopeQueryParam: str = ''


@dataclass
class ClientConfigurations(TcBaseObj):
    """
    This structure contains command and column configuration data for the indicated client.
    
    :var client: The client for which the configurations are applicable.
    :var columnConfigurations: List of column configurations.
    :var commandConfigurations: List of command configurations.
    """
    client: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    commandConfigurations: List[CommandConfigData] = ()


@dataclass
class ClientInput(TcBaseObj):
    """
    Specifies client input information including client name and hosting client name.
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property.
    :var hostingClientName: Specifies the name of a hosting client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property. For example,
    if client A is integrated with client B and the user can invoke client B commands from within client A, the input
    to getUiConfigs would specify client A as hosting client and client B as the client. If the caller wanted native
    commands for client A, client A would be specified as client and hosting client would be empty.
    """
    clientName: str = ''
    hostingClientName: str = ''


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information , and default sort direction.
    
    :var columnConfigId: The unique identifier of the column.
    :var sortDirection: How the columns are sorted.  Valid values are Ascending or Descending.
    :var columns: Ordered list of column details.
    """
    columnConfigId: str = ''
    sortDirection: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class ColumnConfigData(TcBaseObj):
    """
    This structure returns information about the column configuration definitions for a scope, hosting client and
    client scope.
    
    :var scope: The scope for which the column data is applicable.
    :var hostingClient: The name of hosting client for which the list of column configurations is applicable. This
    value must correspond to the value of the property fnd0ClientName for an Fnd0Client object in the Teamcenter
    database.
    :var clientScopeURI: The client scope for which the list of column configurations is applicable. This must match a
    value of fnd0ClientScopeURI which is the unique identifier of a client scope (Fnd0ClientScope).
    :var columnConfigurations: List of column configuration details.
    """
    scope: str = ''
    hostingClient: str = ''
    clientScopeURI: str = ''
    columnConfigurations: List[ColumnConfig] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client and pixel width.
    
    :var typeName: The Business Object type for the value displayed in the column.   This can be any valid Teamcenter
    business object type.
    :var propertyName: The property name for the value displayed in the column.
    :var sortByFlag: True if the column is used to sort the information displayed to the user.
    :var pixelWidth: The pixel width for the column.  Valid pixel widths are integer values between1 and 500.
    """
    typeName: str = ''
    propertyName: str = ''
    sortByFlag: bool = False
    pixelWidth: int = 0


@dataclass
class CommandCollectionInfo(TcBaseObj):
    """
    Contains a command collection and indexes to its children commands or command collections.
    
    :var childIsCollection: Flag indicating if the child is a command or a command collection.
    :var childConfigIndex: Index of the child in either the CommandConfigData:commands list or the
    CommandConfigData:cmdsCollections list.
    :var commandCollection: The Teamcenter command collection object.
    """
    childIsCollection: List[bool] = ()
    childConfigIndex: List[int] = ()
    commandCollection: Fnd0CommandCollection = None


@dataclass
class CommandConfigData(TcBaseObj):
    """
    This structure returns information about the command configuration definitions for a client scope URI.
    
    :var scopeName: The scope for which the command data is applicable.
    :var hostingClient: The hosting client for which the command data is applicable.
    :var clientScope: The client scope URI containing the list of command configurations.
    :var cmdCollections: List of all top level and child command collections in the client scope.
    :var cmdCollectionIndex: Index into cmdCollections list for top level command collections in the client scope.
    :var commands: List of all command children accessible in the client scope.
    """
    scopeName: str = ''
    hostingClient: Fnd0Client = None
    clientScope: Fnd0ClientScope = None
    cmdCollections: List[CommandCollectionInfo] = ()
    cmdCollectionIndex: List[int] = ()
    commands: List[Fnd0AbstractCommand] = ()
