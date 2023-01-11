from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2015_10.DataManagement import DefaultRelationInfo
from typing import Dict, List
from tcsoa.gen.Internal.AWS2._2012_10.DataManagement import ObjectLsdInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDeclarativeStyleSheetResponse(TcBaseObj):
    """
    Response sent to client from the getDeclarativeStyleSheets operation.
    
    :var declarativeUIDefs: Declarative UI Style Sheet Output.
    :var serviceData: Service Data.
    """
    declarativeUIDefs: List[DeclarativeUIDef] = ()
    serviceData: ServiceData = None


@dataclass
class GetDefaultRelationIn(TcBaseObj):
    """
    Holds information of the primary and secondary object types.
    
    :var primaryType: String literal representing the type of primary object.
    :var secondaryType: String literal representing the type of secondary object.
    """
    primaryType: str = ''
    secondaryType: str = ''


@dataclass
class GetDefaultRelationInfo(TcBaseObj):
    """
    Contains information of primary and secondary type and default relation between them. In case default relation
    between primary and secondary type is not found, then the DefaultRelationInfo object will be empty.
    
    :var primaryType: String literal representing the type of primary object.
    :var secondaryType: String literal representing the type of secondary object.
    :var defaultRelation: Contains ImanType, internal name and display name information of default relation between
    primary and secondary type.
    """
    primaryType: str = ''
    secondaryType: str = ''
    defaultRelation: DefaultRelationInfo = None


@dataclass
class GetDefaultRelationResponse(TcBaseObj):
    """
    Response from getDefaultRelation operation.
    
    :var output: List of GetDefaultRelationInfo objects.
    :var serviceData: The SOA service data.
    """
    output: List[GetDefaultRelationInfo] = ()
    serviceData: ServiceData = None


@dataclass
class NameValue(TcBaseObj):
    """
    This structure hold property name and list of property values. This is a generic container that contains the
    property name as string and the value is the string representation of the property value.
    
    :var name: Property name string that needs to be modified.
    :var values: A list of property values that will be used to update the input object with corresponding values. This
    list contains string representation of property value. The calling client is responsible for converting the
    different property types (int, float, date .etc) to a string using the appropriate to XXXString functions in the
    SOA client framework's Property class.
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class PropertyNameValue(TcBaseObj):
    """
    Input Structure containing information about what properties are to be populated. 
    For normal (non-Table )Properties, user has to populate values. 
    For Table Properties, user has to fill the rowValues structure
    
    :var name: Property name that needs to be modified.
    :var values: Property values to update object with. This list contains string representation of the property value.
    The calling client is responsible for converting the different property types (int, float, date .etc) to a string
    using the appropriate toXXXString functions in the SOA client framework's Property class.
    :var rowValues: A list of child object structures. Child structures are populated in case the property contains a
    collection of sub objects. E.g. table properties. For other properties, the list needs to be empty.
    """
    name: str = ''
    values: List[str] = ()
    rowValues: List[RowData] = ()


@dataclass
class RowData(TcBaseObj):
    """
    A structure to hold child information associated with the main object.
    It contains uid of the child, NameValue type of row and its name value pairs for different properties.
    
    :var uid: The child object UID. If the UID is empty or a NULL UID, a new object is created with details as
    populated in nameValues.
    :var rowType: The subtype of Fnd0NameValue business object. Valid value can only be one from below mentioned list
    of values :
    Fnd0NameValueDate,
    Fnd0NameValueDouble,
    Fnd0NameValueInt,
    Fnd0NameValueLogical, 
    Fnd0NameValueString.
    :var nameValues: List of named property values to be saved. If UID is not blank then the properties populated in
    this structure will be updated. If UID is blank, then a new child object is created based on the name values input.
    """
    uid: str = ''
    rowType: str = ''
    nameValues: List[NameValue] = ()


@dataclass
class SaveEditAndSubmitInfo(TcBaseObj):
    """
    Structure represents the parameters required to save the edits on the input objects and submit them to a workflow
    process.
    
    :var tcobject: Teamcenter object (POM_object) to save edit and submit to a workflow process.
    :var propertyNameValues: Property name and values structure that will contain all property names and corresponding
    values that needs to be saved.
    :var objLsds: The last set date information for the object.
    :var isPessimisticLock: The flag to control whether this method call performs optimistic locking or not.
    If false, operation takes optimistic lock on the object. In optimistic locking the object is locked (based on the
    object last saved date) before performing the actual save and lock is released after save is complete.
    If true, object needs to be checked out before making any edits (pessimistic locking). The locking of object is
    done during loadDataForEditing operation.
    :var workflowData: The workflow information that the input object needs to submit to a workflow. Workflow
    information is stored in a name and value string map (string/list of strings). If workflowData map is empty,
    objects will not be submitted to any workflow.
    Supported keys:
    
    &bull; submitToWorkflow: Boolean Property to define that input object need to submit to workflow process or not. It
    can contain true or false as value. 
    &bull; processName: Process name string. 
    &bull; processDescription: Process description string. 
    &bull; processTemplate: Name of the process template to be used to create new workflow process. 
    &bull; processAssignmentList: Name of the process assignment list to use while creating new workflow process. 
    
    If property submitToWorkflow value is true and processTemplate value is empty, then workflow process template to be
    used for workflow creation should be specified in the preference (<TypeName>_default_workflow_template) defined for
    the submitted object type.
    """
    tcobject: BusinessObject = None
    propertyNameValues: List[PropertyNameValue] = ()
    objLsds: List[ObjectLsdInfo] = ()
    isPessimisticLock: bool = False
    workflowData: PropertyValues2 = None


@dataclass
class DeclarativeUIDef(TcBaseObj):
    """
    The declarative UI definition. Which can be used to define a particular part of web page with the support of
    declarative UI framework.
    
    :var view: The declarative view definition. It consists of HTML custom elements.
    :var viewModel: The view model of declarative UI in JSON format. It can be bound to declarative view.
    :var glueCodeJS: The piece of JavaScript code to glue the declarative view and view model. JavaScript functions can
    be defined in glue code and be referenced in the view model. The functions which are referenced will be called by
    declarative UI framework, and the return values are consumed to build up the view model.
    """
    view: str = ''
    viewModel: str = ''
    glueCodeJS: str = ''


"""
Map (string, list of strings) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValues2 = Dict[str, List[str]]
