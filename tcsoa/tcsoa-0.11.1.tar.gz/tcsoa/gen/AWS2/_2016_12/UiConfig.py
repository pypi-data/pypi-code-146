from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0Client, Fnd0AbstractCommand, Fnd0UIConfigCollectionRel, Fnd0CommandCollection, Fnd0ClientScope
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
    :var uiConfigInfo: List of configuration information including command and column information.
    """
    serviceData: ServiceData = None
    uiConfigInfo: List[ClientConfigurations] = ()


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
    :var hostingClientName: Specifies the name of a hosting Client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property. For example,
    if Client A is integrated with Client B and the user can invoke Client B commands from within Client A, the input
    to getUiConfigs would specify Client A as hosting Client and Client B as the Client. If the caller wanted native
    commands for Client A, Client A would be specified as Client and hosting Client would be empty.
    """
    clientName: str = ''
    hostingClientName: str = ''


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the default sort direction.
    
    :var columnConfigId: The unique identifier of the column.
    :var sortDirection: How the columns are sorted. Valid values are Ascending and Descending.
    :var columns: Ordered list of column details.
    """
    columnConfigId: str = ''
    sortDirection: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class ScopeInput(TcBaseObj):
    """
    Contains scope input information including scope name and scope query parameter.
    
    :var scopeName: The name of a scope. For Site and current login user, this value should be empty.
    :var scopeQueryParam: The query scope that is used to retrieve the UI configurations. Valid values are Site, Group,
    Role, User, LoginUser, and AvailableForLoginUser. Site returns the configuration defined for the site. Group
    returns the configuration defined for a specific Teamcenter Group. Role returns the configuration defined for a
    specific Teamcenter Role. User returns the configurations defined for a specific Teamcenter User. LoginUser returns
    the current configuration defined for the current login user. AvailableForLoginUser returns all the configurations
    available for the current login user. The value for scopeName should be empty when scopeQueryParam is set to:
    "Site", "LoginUser" or "AvailableForLoginUser".
    """
    scopeName: str = ''
    scopeQueryParam: str = ''


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
    
    :var typeName: The Business Object type for the value displayed in the column. This can be any valid Teamcenter
    business object type.
    :var propertyName: The property name for the value displayed in the column.
    :var sortByFlag: True if the column is used to sort the information displayed to the user.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between1 and 500.
    """
    typeName: str = ''
    propertyName: str = ''
    sortByFlag: bool = False
    pixelWidth: int = 0


@dataclass
class CommandCollectionInfo(TcBaseObj):
    """
    Contains a command collection and indexes to its children commands or command collections.
    
    :var childIsCollection: If true ,the child is a command collection; otherwise, the child is a command.
    :var childIsVisible: If true, command or collection is visible; otherwise, the command or collection is not visible.
    :var childConfigIndex: Index of the child in either the CommandConfigData:commands list or the
    CommandConfigData:cmdsCollections list. It is used by client to build the command hierarchy.
    :var commandCollection: Fnd0CommandCollection object.
    """
    childIsCollection: List[bool] = ()
    childIsVisible: List[bool] = ()
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
    :var commandCollectionRels: List of all commandCollectionRel objects that associate top level command collections
    with client scope.
    """
    scopeName: str = ''
    hostingClient: Fnd0Client = None
    clientScope: Fnd0ClientScope = None
    cmdCollections: List[CommandCollectionInfo] = ()
    cmdCollectionIndex: List[int] = ()
    commands: List[Fnd0AbstractCommand] = ()
    commandCollectionRels: List[Fnd0UIConfigCollectionRel] = ()
