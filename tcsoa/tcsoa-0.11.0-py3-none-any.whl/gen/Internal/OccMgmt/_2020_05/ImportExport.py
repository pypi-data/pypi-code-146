from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


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
    
    :var selectedObject: Selected Object under which the product will be created.
    :var transientFileWriteTicket: Write ticket of the Excel file to be imported to Teamcenter.
    :var mappingGroupData: A list of mapping groups to be consumed during the import.
    :var importOptions: A list of options to be used during the import.
    Supported options are: 
     "ParseHeader" -  The header row in the Excel sheet is    parsed. 
    "RunInBackground" -  The excel file import runs in background mode and user will get a notification when complete.
    If omitted, after completion of import, the top line Revision of the created structure will be opened.
    :var typePropInfos: List of object types and property related information to be retrieved for the types found in
    input Excel sheet. The list is used only when importOption is set to "ParseHeader".
    """
    selectedObject: BusinessObject = None
    transientFileWriteTicket: str = ''
    mappingGroupData: MappingGroupData = None
    importOptions: List[str] = ()
    typePropInfos: List[TypePropInfo] = ()


@dataclass
class ImportExcelResponse(TcBaseObj):
    """
    The ImportExcelResponse structure contains the list of objects of type ItemRevision.
    
    :var revObjects: A list of business objects of type ItemRevision.
    :var serviceData: Service data.
    """
    revObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class MappingGroupData(TcBaseObj):
    """
    The MappingGroupData structure contains the real and display name of the mapping group along with the mapping
    information.
    
    :var groupName: It contains the real and display name of the group.
    :var actionName: Supported action "CREATE", "UPDATE" or "DELETE".
    :var mappingInfo: List of property related information.
    """
    groupName: GroupName = None
    actionName: str = ''
    mappingInfo: List[PropInfo] = ()


@dataclass
class MappingGroupInput(TcBaseObj):
    """
    The MappingGroupInput structure contains all the mapping group names and mapping information.
    
    :var transientFileWriteTicket: The write ticket of the Excel file to be imported to Teamcenter.
    :var mappingGroupData: It contains the action name, group name, and mapping information.
    :var importOptions: List of options used during the import. Supported option: "ParseHeader" - The header row in the
    Excel sheet is parsed.
    """
    transientFileWriteTicket: str = ''
    mappingGroupData: MappingGroupData = None
    importOptions: List[str] = ()


@dataclass
class MappingGroupOutput(TcBaseObj):
    """
    The MappingGroupOutput structure contains the type and property related data that is parsed from the input Excel
    sheet.
    
    :var mappingGroups: List of mapping group related information.
    :var propInfos: List of property related information.
    :var typePropInfos: List of object types and property related information to be retrieved for the types found in
    input Excel sheet. The list is used only when importOption is set to "ParseHeader".
    """
    mappingGroups: List[GroupName] = ()
    propInfos: List[PropInfo] = ()
    typePropInfos: List[TypePropInfo] = ()


@dataclass
class MappingGroupResponse(TcBaseObj):
    """
    The MappingGroupResponse structure contains the list of MappingGroupOutput.
    
    :var mappingOutputs: List of mapping outputs.
    :var serviceData: Service data.
    """
    mappingOutputs: List[MappingGroupOutput] = ()
    serviceData: ServiceData = None


@dataclass
class PropInfo(TcBaseObj):
    """
    The PropInfo structure contains the property related information to be set.
    
    :var propHeader: Name of the property used as column header in Excel sheet.
    :var realPropName: Real name of the property.
    :var dispPropName: Display name of the property.
    :var isRequired: True if it is a required property.
    """
    propHeader: str = ''
    realPropName: str = ''
    dispPropName: str = ''
    isRequired: bool = False


@dataclass
class TypePropInfo(TcBaseObj):
    """
    The TypePropInfo structure is a container to hold the types and property related information.
    
    :var objectType: Valid subclass name of type Item objects to be created.
    :var dispTypeName: Display name of the object type.
    :var propInfos: List of property related information.
    """
    objectType: str = ''
    dispTypeName: str = ''
    propInfos: List[PropInfo] = ()
