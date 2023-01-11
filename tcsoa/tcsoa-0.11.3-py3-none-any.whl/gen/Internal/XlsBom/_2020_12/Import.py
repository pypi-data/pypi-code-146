from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RevisionRule
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ParentChildrenInfo(TcBaseObj):
    """
    Parent and its children information.
    
    :var parentInfo: Information of parent node.
    :var chidrenInfo: Information of children nodes corresponding to parentInfo.
    """
    parentInfo: NodeInfo = None
    chidrenInfo: List[NodeInfo] = ()


@dataclass
class PropInfo(TcBaseObj):
    """
    The PropInfo structure contains the property related information that is mapped with Teamcenter property.
    
    :var propHeader: Name of the property used as column header in Excel sheet.
    :var realPropName: Real name of the property.
    :var realPropDisplayName: Real display name of the property.
    :var isRequired: True if it is a required property.
    """
    propHeader: str = ''
    realPropName: str = ''
    realPropDisplayName: str = ''
    isRequired: bool = False


@dataclass
class StructureInfoResp(TcBaseObj):
    """
    StructureInfoResp  contains the structure information for given Excel. This data structure contains column
    configuration information and cursor to be sent back to the subsequent calls.
    
    :var columnConfig: Column configuration.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var nodeInfos: Pagefull of the nodes that have been fetched.
    :var serviceData: Contains any errors that might have occurred as part of the service invocation.
    """
    columnConfig: ColumnConfig = None
    cursor: Cursor = None
    nodeInfos: List[NodeInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ColumnConfig(TcBaseObj):
    """
    The column configuration data.
    
    :var columnConfigId: Column configuration ID.
    :var operationType: Operation type used for determining columns.  Supported values are: "Union" and "Intersection".
    :var columns: A list of available columns.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Column Definition
    
    :var displayName: The display name for the value displayed in the column header.
    :var propertyName: The property name for the value displayed in the column.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    """
    displayName: str = ''
    propertyName: str = ''
    pixelWidth: int = 0


@dataclass
class Cursor(TcBaseObj):
    """
    Cursor is a cursor that is returned for use in subsequent call to retrieve the next page of nodes.
    
    :var startReached: If true, the first page of the results has been reached.
    :var endReached: If true, the last page of the results has been reached.
    :var startIndex: Indicates the Cursor start position for the result nodes returned so far.
    :var endIndex: Indicates the Cursor end position for the result nodes returned so far.
    :var pageSize: Indicates the maximum number of nodes that can be returned in one service call.
    """
    startReached: bool = False
    endReached: bool = False
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0


@dataclass
class ExcelImportInput(TcBaseObj):
    """
    ExcelImportInput provides file ticket and mapped property info to get back the structure information. It also
    contains cursor that represents point to which the results have to be fetched.
    
    :var transientFileWriteTicket: The write ticket of the Excel file to be imported to Teamcenter.
    :var propInfos: A list of property related information from the input Excel sheet that are mapped with Teamcenter
    Item, BOMLine properties.
    :var typePropInfos: A map (string, list of PropInfo) of object type to property related information to be retrieved
    for the types found in input Excel sheet.
    :var cursor: Cursor that represents point to which the results have been returned.
    """
    transientFileWriteTicket: str = ''
    propInfos: List[PropInfo] = ()
    typePropInfos: TypeMapInfo = None
    cursor: Cursor = None


@dataclass
class GroupName(TcBaseObj):
    """
    The GroupName structure contains the real and display name of the group.
    
    :var realName: Real name of the group.
    :var dispName: Display name of the group.
    :var isModifiable: True if the mapping group can be modified by logged in user.
    """
    realName: str = ''
    dispName: str = ''
    isModifiable: bool = False


@dataclass
class ImportExcelData(TcBaseObj):
    """
    The ImportExcelData structure contains all the data required to import a file to Teamcenter.
    
    :var selectedObject: Selected Object under which the product will be created. The supported types are: Folder,
    ItemRevision, and Awb0Element.
    :var transientFileWriteTicket: Write ticket of the Excel file to be imported toTeamcenter.
    :var mappingGroupData: A list of mapping groups to be consumed during the import.
    :var importOptions: A list of options to be used during the import. 
    Supported options are: 
    "ParseHeader" -  The header row in the Excel sheet is    parsed. 
    "RunInBackground" -  The excel file import runs in background mode and user will get a notification when complete.
    If omitted, after completion of import, the top line Revision of the created structure will be opened.
    :var propInfos: List of object types and property related information to be     retrieved for the types found in
    input Excel sheet. The list is used only when importOption is set to "ParseHeader".
    :var typePropInfos: A map (string, list of PropInfo) of object type to property related information to be retrieved
    for the types found in input Excel sheet.
    :var actionInfo: A map (string, string) of Excel row index to action. The map will be used to indicate an operation
    on each object. Operation is defined as the value of the map. Keys and values are case sensitive. Key contains the 
    Excel row index . Allowed values are: "Reference", "Overwrite", "Revise".     
    "Reference" - No updates to the existing Teamcenter data.                                      
    "Overwrite" - Updates the existing Teamcenter data with the input file.                               "Revise" -
    Existing data will be revised to latest revision in Teamcenter.
    """
    selectedObject: BusinessObject = None
    transientFileWriteTicket: str = ''
    mappingGroupData: MappingGroupData = None
    importOptions: List[str] = ()
    propInfos: List[PropInfo] = ()
    typePropInfos: TypeMapInfo = None
    actionInfo: ActionInfo = None


@dataclass
class ImportExcelResp(TcBaseObj):
    """
    The ImportExcelResp structure contains the list of objects of type ItemRevision.
    
    :var revObjects: A list of business objects of type ItemRevision.
    :var revisionRule: Working, Any Status RevisionRule which will be used to open imported object with Working, Any
    Status.
    :var requestPreference: The map which can have a key and value pair, used for import options. The key and value are
    case sensitive.
    :var serviceData: Service data.
    """
    revObjects: List[BusinessObject] = ()
    revisionRule: RevisionRule = None
    requestPreference: RequestPreference = None
    serviceData: ServiceData = None


@dataclass
class NodeInfo(TcBaseObj):
    """
    NodeInfo is the information about node.
    
    :var nodeId: Unique identifier (UID) of a node.
    :var displayName: Display name of a node.
    :var underlyingObjectType: Internal name of the underlying object a node presents.
    :var numberOfChildren: Number of children of the node.
    :var propNameValueMap: A map of property internal name as key and display value as map value.
    """
    nodeId: str = ''
    displayName: str = ''
    underlyingObjectType: str = ''
    numberOfChildren: int = 0
    propNameValueMap: PropNameValueMap = None


@dataclass
class MappingGroupData(TcBaseObj):
    """
    The MappingGroupData structure contains the real and display name of the mapping group along with the mapping
    information.
    
    :var groupName: It contains the real and display name of the group.
    :var actionName: Supported action: "CREATE", "UPDATE" or "DELETE".
    "CREATE" &ndash; A new Object will be created.
    "UPDATE" &ndash; Existing object will be updated.
    "DELETE" &ndash; Existing object will be deleted.
    :var mappingInfo: List of property related information.
    """
    groupName: GroupName = None
    actionName: str = ''
    mappingInfo: List[PropInfo] = ()


"""
A map (string, string) of Excel row index to action. The map will be used to indicate an operation on each object. Operation is defined as the value of the map. Keys and values are case sensitive. Key contains the  Excel row index . Allowed values are: "Reference", "Overwrite", "Revise".     
"Reference" - No updates to the existing Teamcenter data.                                      
"Overwrite" - Updates the existing Teamcenter data with the input file.                              
"Revise" - Existing data will be revised to latest revision in Teamcenter.
"""
ActionInfo = Dict[str, str]


"""
A map (string, list of PropInfo) of object type to property related information to be retrieved for the types found in input Excel sheet.
"""
TypeMapInfo = Dict[str, List[PropInfo]]


"""
PropNameValueMap is a map containing property display value for each property internal name.
"""
PropNameValueMap = Dict[str, str]


"""
The map which can have a key and value pair, used for import options. The key and value are case sensitive.
"""
RequestPreference = Dict[str, List[str]]
