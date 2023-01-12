from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0Client, Fnd0AbstractCommand, Fnd0UIConfigCollectionRel, Fnd0ClientScope
from tcsoa.gen.AWS2._2016_12.UiConfig import ClientInput, ScopeInput, CommandCollectionInfo
from tcsoa.gen.Internal.AWS2._2016_03.UiConfig import CommandContextInfo
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetUIConfigInput(TcBaseObj):
    """
    Contains input information required to retrieve UI configurations from the Teamcenter database.
    
    :var clientScopeURIs: A list of client scope URIs representing, for example location.sublocation in Active
    Workspace. (Fnd0ClientScope::fnd0ClientScopeURI). If empty, the UI Configuration for all client scopes are returned.
    :var scope: The scope of the desired UI configuration information. This includes the name of the scope (i.e. a
    user, group or role) and scope query parameter information.
    :var client: Client information including client name and hosting client name.
    :var commandContextInfo: A list of command context name value pairs, Supprted key/value pairs are :
    isHosted"="true|false", - if true , active workspace clinet is hosted in another application such as NX. If false,
    active workspace client is stand alone. "productContext"=productContextUid.
    """
    clientScopeURIs: List[str] = ()
    scope: ScopeInput = None
    client: ClientInput = None
    commandContextInfo: List[CommandContextInfo] = ()


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
    
    :var client: The client for which the configurations are applicable. It is to match the clientName in ClientInput
    SOA struture.
    :var columnConfigurations: A list of column configurations.
    :var commandConfigurations: A list of command configurations.
    """
    client: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    commandConfigurations: List[CommandConfigData] = ()


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the default sort direction.
    
    :var columnConfigId: The unique identifier of the column.
    :var sortDirection: How the columns are sorted. Valid values are Ascending and Descending.
    :var operationType: The operation that was used to finalize the columns to be returned back.
    Valid values are:  "Intersection", "Union" and "Configured".
    :var columns: Ordered list of column details.
    """
    columnConfigId: str = ''
    sortDirection: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class ColumnConfigData(TcBaseObj):
    """
    This structure returns information about the column configuration definitions for a scope, hosting client and
    client scope.
    
    :var scope: The scope for which the column data is applicable.
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
class ViewModelPropertyDescriptor(TcBaseObj):
    """
    Represents the property descriptor details for a ViewModelProperty.
    
    :var srcObjectTypeName: Type name of the source object on which the property is defined.
    :var propertyName: Name of the property.
    :var valueType: Indicates the value type for the property. Valid value types are: 
    1 - Char
    2 - Date
    3 - Double
    4 - Float
    5 - Integer
    6 - Boolean
    7 - Short Integer
    8 - String
    9 - Type Reference
    10 - UnTyped Reference
    11 - External Reference
    12 - Note
    13 - Typed Relation
    14 - UnTyped Relation
    :var isArray: Has value as true in case of array properties and value as false for single valued properties.
    :var propConstants: A map(string,string) consisting of propertyConstant name as key and  and value being the
    property constant value.
    :var displayName: Display name of the property.
    :var lovCategory: Indicates the LOV category, if the property is attached to LOV.
    :var lov: LOV object reference associated with the property.
    :var maxArraySize: Maximimum number of elements allowed in case of VLA properties.
    :var maxLength: Max allowed length for the property
    :var propertyType: Indicates the property type. Valid property types are: 
    1 - attribute. 
    2 - Reference Property. 
    3 - Relation Property. 
    4 - Compound Property. 
    5 - Runtime Property.
    6 - Operation input.
    """
    srcObjectTypeName: str = ''
    propertyName: str = ''
    valueType: int = 0
    isArray: bool = False
    propConstants: PropertyConstantsMap = None
    displayName: str = ''
    lovCategory: int = 0
    lov: BusinessObject = None
    maxArraySize: int = 0
    maxLength: int = 0
    propertyType: int = 0


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client and pixel width and the display name of the property.
    
    :var sortByFlag: If true, the column is used to sort the information displayed to the user; otherwise, not used.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var hiddenFlag: True if the column should be hidden on the client user interface.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var colDefSortDirection: How the columns are sorted. Valid values are: "Ascending" and "Descending". This value
    will be empty if the column is not marked for sorting.
    :var propDescriptor: List of ViewModelPropertyDescriptors required to render the object properties in AW client.
    :var columnSrcType: Valid Teamcenter type for which the column property has been defined
    """
    sortByFlag: bool = False
    pixelWidth: int = 0
    columnOrder: int = 0
    hiddenFlag: bool = False
    sortPriority: int = 0
    colDefSortDirection: str = ''
    propDescriptor: ViewModelPropertyDescriptor = None
    columnSrcType: str = ''


@dataclass
class CommandConfigData(TcBaseObj):
    """
    This structure returns information about the command configuration definitions for a client scope URI.
    
    :var scopeName: This structure returns information about the command configuration definitions for a client scope
    URI.
    :var hostingClient: The hosting Fnd0Client for which the command data is applicable.
    :var clientScope: The Fnd0ClientScope containing the list of command configurations.
    :var cmdCollections: A list of all top level and child command collections in the client scope.
    :var cmdCollectionIndex: A list of index values into cmdCollections list for top level command collections in the
    client scope.
    :var commands: A list of all Fnd0AbstractCommand objects accessible in the client scope.
    :var commandCollectionRels: A list of all Fnd0UIConfigCollectionRel objects that associate top level command
    collections with client scope.
    :var visibleCommands: A list of visible Fnd0AbstractCommand objects accessible in the client scope.
    """
    scopeName: str = ''
    hostingClient: Fnd0Client = None
    clientScope: Fnd0ClientScope = None
    cmdCollections: List[CommandCollectionInfo] = ()
    cmdCollectionIndex: List[int] = ()
    commands: List[Fnd0AbstractCommand] = ()
    commandCollectionRels: List[Fnd0UIConfigCollectionRel] = ()
    visibleCommands: List[Fnd0AbstractCommand] = ()


"""
Map to store the property constant name and value pair.
"""
PropertyConstantsMap = Dict[str, str]
