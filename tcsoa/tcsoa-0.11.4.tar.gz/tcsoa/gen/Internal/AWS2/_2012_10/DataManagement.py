from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0GatewayTileRel, Awp0Tile, UserSession
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetChildrenOutput(TcBaseObj):
    """
    GetChildrenOutput
    
    :var parentObject: parentObject
    :var children: children
    """
    parentObject: BusinessObject = None
    children: List[BusinessObject] = ()


@dataclass
class GetChildrenResponse(TcBaseObj):
    """
    GetChildrenResponse
    
    :var output: output
    :var serviceData: serviceData
    """
    output: List[GetChildrenOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetCurrentUserGatewayResponse(TcBaseObj):
    """
    Contains the Awp0Tile, Awp0GatewayTileRel and the group name in which the Awp0Tile belongs to. The 'tileGroupInfos'
    are ordered based on the 'awp0OrderNo' on the Awp0GatewayTileRel.  For example, the group with the lowest
    'awp0OrderNo' value on the Awp0GatewayTileRel appears first in the list.
    
    :var tileGroupInfos: Information about the Awp0Tile and its group.
    :var serviceData: Awp0Tile and Awp0GatewayTileRel objects are added to the 'ServiceData' list of plain objects.
    """
    tileGroupInfos: List[CurrentUserTileGroupInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetTCSessionInfoResponse(TcBaseObj):
    """
    Data structure representing the different current user's Teamcenter session information.
    
    :var userSession: The Teamcenter user's session information.
    :var serviceData: The service data.
    """
    userSession: UserSession = None
    serviceData: ServiceData = None


@dataclass
class HistoryInput(TcBaseObj):
    """
    The input structure to add objects to the history and/or remove objects from the history.
    
    :var objectsToAdd: The list of objects to add to the history; this list can be empty.
    :var objectsToRemove: The list of objects to remove from the history; this list can be empty.
    :var returnHistory: Flag indicating whether the objects in the history are to be returned.
    """
    objectsToAdd: List[BusinessObject] = ()
    objectsToRemove: List[BusinessObject] = ()
    returnHistory: bool = False


@dataclass
class HistoryResult(TcBaseObj):
    """
    The response structure containing the result after adding objects to the history and/or removing objects from the
    history.
    
    :var historyObjects: The list of objects contained in the history.
    :var serviceData: The service data object.
    """
    historyObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class LoadDataForEditingInfo(TcBaseObj):
    """
    Input structure of LoadDataForEditing SOA
    
    :var obj: Input object
    :var propertyNames: Property names
    :var isPessimisticLock: Flag indicating if object should be locked pessimisticly
    """
    obj: BusinessObject = None
    propertyNames: List[str] = ()
    isPessimisticLock: bool = False


@dataclass
class LoadDataForEditingOutput(TcBaseObj):
    """
    Output structure of LoadDataForEditing operation
    
    :var obj: Object to start edit or its dependent objects
    :var objLsds: Map of last save date of object or dependent objects
    """
    obj: BusinessObject = None
    objLsds: List[ObjectLsdInfo] = ()


@dataclass
class LoadDataForEditingResponse(TcBaseObj):
    """
    Response of LoadDataForEditing SOA
    
    :var outputs: Outputs
    :var serviceData: Service data
    """
    outputs: List[LoadDataForEditingOutput] = ()
    serviceData: ServiceData = None


@dataclass
class NameValueStruct(TcBaseObj):
    """
    This structure hold property name and vector of property values. This is a generic container that contains the
    property name as string and the value is the string representation of the property value.
    
    :var name: Property name string that needs to be modified.
    :var values: Property values string vector that will be used to update the input object with corresponding values.
    This vector contains string representation of the property value. The calling client is responsible for converting
    the different property types (int, float, date .etc) to a string using the appropriate toXXXString functions in the
    SOA client framework's Property class.
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class ObjectLsdInfo(TcBaseObj):
    """
    Structure containing the lsd information for an input Business object.
    
    :var obj: Input Business object that needs to be saved.
    :var lsd: 'Last Modified date' (lsd) information of an input Business object that will be used before saving the
    modified properties of that input object. This is used to check the last modified time at the point of save, to
    ensure the right changes are applied to that object and that it has not been changed since the edit was started.
    """
    obj: BusinessObject = None
    lsd: datetime = None


@dataclass
class SaveEditAndSubmitInfo(TcBaseObj):
    """
    Structure represents the parameters required to save the edits on the input objects and submit them to a workflow
    process.
    
    :var object: Object to save edit and submit to a workflow process.
    :var propertyNameValues: Property name and values structure that will contain all property names and corresponding
    string values that needs to be saved.
    :var objLsds: The LSD information for the object.
    :var isPessimisticLock: Flag indicating object is pessimistically locked or not. If value is true, then object is
    locked while startEdit(), else object is not locked in startEdit() operation.
    :var workflowData: The workflow information that the input object needs to submit to a workflow or not.Workflow
    information is stored in a name and value string map that can contain property name as string and value will be
    also be string representation. Supported properties are  submitToWorkflow, processName, processDescription,
    processTemplate, processAssignmentList. 
    submitToWorkflow-  Boolean Property to define that input object need to submit to workflow process or not. It can
    contain true or false as value.
    processName- Process name string. 
    processDescription- Process description string. 
    processTemplate- Name of the process template to be used to create new workflow process. 
    processAssignmentList- Name of the process assignment list to use while creating new workflow process.
    Note- If the above property submitToWorkflow contains true value and process template value is empty, thenworkflow
    process template to be used for workflow creation should be specified in the preference
    (<TypeName>_default_workflow_template) defined for the submitted obejct type.
    """
    object: BusinessObject = None
    propertyNameValues: List[NameValueStruct] = ()
    objLsds: List[ObjectLsdInfo] = ()
    isPessimisticLock: bool = False
    workflowData: PropertyValues = None


@dataclass
class SaveEditAndSubmitOutput(TcBaseObj):
    """
    Structure containing information about each input object and whether it was saved and submitted to workflow
    successfully or not.
    
    :var clientId: Input string to uniquely identify the input, used primarily for error handling and output mapping.
    :var workflowProcess: Workflow template object created for each input object that was submitted to workflow.
    """
    clientId: str = ''
    workflowProcess: BusinessObject = None


@dataclass
class SaveEditAndSubmitResponse(TcBaseObj):
    """
    Structure containing saveEditAndSubmit() operation response.
    
    :var output: A list of SaveEditAndSubmitOutput structures.
    :var serviceData: Objects updated after save operation are added to ServiceData&rsquo;s updated object list.  
    Workflow processes created, after input objects are submitted to workflow, are added to ServiceData&rsquo;s created
    object list. Partial errors are returned in the Service Data.
    """
    output: List[SaveEditAndSubmitOutput] = ()
    serviceData: ServiceData = None


@dataclass
class SaveEditInfo(TcBaseObj):
    """
    Input structure of saveEdit SOA
    
    :var obj: Object to save edit
    :var propertyNameValues: Property name and values
    :var objLsds: Lsd map
    :var isPessimisticLock: Flag indicating object is pessimisticly locked in loadDataForEditing
    """
    obj: BusinessObject = None
    propertyNameValues: List[NameValueStruct] = ()
    objLsds: List[ObjectLsdInfo] = ()
    isPessimisticLock: bool = False


@dataclass
class CurrentUserTileGroupInfo(TcBaseObj):
    """
    Contains the Awp0Tile, Awp0GatewayTileRel, and the group name in which the Awp0Tile belongs. The 'tileInfos' are
    ordered based on the 'awp0OrderNo' property on the Awp0GatewayTileRel object.
    
    :var tileGroupName: The group name of the Awp0Tile.
    :var tileInfos: List of Awp0Tiles in this group.
    """
    tileGroupName: str = ''
    tileInfos: List[CurrentUserTileInfo] = ()


@dataclass
class CurrentUserTileInfo(TcBaseObj):
    """
    Contains the Awp0Tile and Awp0GatewayTileRel object. The size of the Awp0Tile and the order number within the group
    can be retrieved by inflating 'awp0TileSize' and 'awp0OrderNo' property on the Awp0GatewayTileRel object.
    
    :var tile: The Awp0Tile to be displayed.
    :var tileRel: The Awp0GatewayTileRel associating the Awp0Tile and Awp0TileCollection.
    """
    tile: Awp0Tile = None
    tileRel: Awp0GatewayTileRel = None


"""
Map (string, vector<string>) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValues = Dict[str, List[str]]
