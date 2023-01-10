from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0StaticTable, POM_object
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NameValueStruct1(TcBaseObj):
    """
    This structure contains property name and value pairs for each property.
    
    :var name: Name of the property
    :var values: Values of the property
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class PostEventObjectProperties(TcBaseObj):
    """
    The 'PostEventObjectProperties' structure represents required parameters to post event on primaryObject when event
    eventTypeName occurs.
    
    :var clientId: A unique identifier supplied by the caller. This ID is used to identify return PostEventOutput and
    partial errors assocaited with this input structure. This is optional, provide empty String for null or optional
    value i.e. new String[0].
    :var primaryObject: The Business Object on which the event has occurred. This is a required parameter.
    :var secondaryObject: Secondary object should be passed when an event involves two objects, primaryObject and
    secondaryObject and writing the secondaryObject details conveys complete Audit information. Example, attaching
    license to Item. This is optional, provide null value for optional value.
    :var propertyCount: The propertyCount is the count of properties that user wants to be written  to Audit log. If
    the propertyCount is 0 the propertyNames and propertyValues will be ignored and treated as NULL values. This is
    optional and default value is 0.
    :var propertyNames: The propertyNames is the list of property names to be written to audit log. The total number of
    properties to write depends on the propertyCount value. This is optional, provide empty String for null or optional
    value i.e. new String[0].
    :var propertyValues: The propertyValues is the list of property values to be written to audit log for each of the
    propertyNames. The total number of properties to write depends on the propertyCount and propertyNames value. Any of
    these values if not specified will treat propertyValues as NULL.  This is optional, provide empty String for null
    or optional value i.e. new String[0].
    :var errorCode: Specify error code when failure of an event is to be recorded in audit log. This is optional and
    default value is 0.
    :var errorMessage: Specify error message when failure of an event is to be recorded in audit log. This is optional,
    you should provide empty String object for null or optional value i.e. new String[0].
    """
    clientId: str = ''
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    propertyCount: int = 0
    propertyNames: List[str] = ()
    propertyValues: List[str] = ()
    errorCode: int = 0
    errorMessage: str = ''


@dataclass
class PostEventOutput(TcBaseObj):
    """
    The 'PostEventOutput' structure represents the output success or failure for each of the
    'PostEventObjectProperties' structure in ifailError  for the assocaited clientId.
    
    :var clientId: Client unique identifier which is passed back for tracking the operation status.
    :var ifailError: The error code, if any. Packaged in the custom output response.
    """
    clientId: str = ''
    ifailError: int = 0


@dataclass
class PostEventResponse(TcBaseObj):
    """
    The 'PostEventResponse' structure represents the output returning a vector of 'PostEventOutput'  with partial
    errors wrapped in serviceData, if any.
    
    :var output: A vector of 'PostEventOutput' structures packaged in custom response. Success is defined by the return
    of the ifailError for post event on each of the primaryObject.
    :var serviceData: Partial failures will be returned in the Service Data for each failed processing. Error
    encountered while processing post event on element in the set is reported as partial errors and processing
    continues for the remaining elements in the input set.
    """
    output: List[PostEventOutput] = ()
    serviceData: ServiceData = None


@dataclass
class PropInfo(TcBaseObj):
    """
    This structure holds information about Teamcenter object & its timestamp and list of property name/value pair
    information.
    
    :var object: business object
    :var vecNameVal: Vector of property information
    :var timestamp: Timestamp of the object when object was exported to clients.
    """
    object: BusinessObject = None
    vecNameVal: List[NameValueStruct1] = ()
    timestamp: datetime = None


@dataclass
class RowData(TcBaseObj):
    """
    Row Data
    
    :var clientId: clientId
    :var rowObject: Row Object
    :var rowType: RowType
    :var rowAttrValueMap: Row Attribute Value Pair Map
    """
    clientId: str = ''
    rowObject: POM_object = None
    rowType: str = ''
    rowAttrValueMap: RowAttrValueMap = None


@dataclass
class SetPropertyResponse(TcBaseObj):
    """
    response structure for setProperties operation. It returns the information about overwritten objects.
    
    :var data: This is the service data. It contains the updated objects and their properties.
    :var objPropMap: Additional information to be communicated to client such as objects and props those are
    overwritten. This map can be empty if no overwritten object found or with QUERY option is not an input to the
    service operation.
    """
    data: ServiceData = None
    objPropMap: ObjectPropMap = None


@dataclass
class StaticTableDataResponse(TcBaseObj):
    """
    StaticTableDataResponse
    
    :var clientId: A unique string supplied by caller.
    This ID is used to identify return data elements and partial errors associated with this input structure. 
    
    :var serviceData: The Service Data.
    """
    clientId: str = ''
    serviceData: ServiceData = None


@dataclass
class StaticTableInfo(TcBaseObj):
    """
    Static Table Info
    
    :var tableType: type of table created/updated e.g. TableProperties
    :var tableObject: Fnd0StaticTable object
    """
    tableType: str = ''
    tableObject: Fnd0StaticTable = None


@dataclass
class VerifyExtensionInfo(TcBaseObj):
    """
    The required information in which to validate an extension exists on an operation for a specific type.
    
    :var typeName: The name of the type in which to check the operations.
    :var operationName: The name of the operation in which to check for the containing extension.
    :var extensionName: The name of the extension to check.
    :var extensionType: The extension type to check: 0=All, 1=PreCondition, 2=PreAction, 3=PostAction, 4=BaseAction
    """
    typeName: str = ''
    operationName: str = ''
    extensionName: str = ''
    extensionType: int = 0


@dataclass
class VerifyExtensionResponse(TcBaseObj):
    """
    The result of the Verify Extension method.
    
    :var output: Returns True if extension exists otherwise False.
    :var serviceData: This data structure provides service data for associated information.
    """
    output: List[bool] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateStaticTableDataResponse(TcBaseObj):
    """
    Contains Creation or updation response for Static table.
    
    :var serviceData: SOA Service Data.
    :var staticTableObject: StaticTable Object
    """
    serviceData: ServiceData = None
    staticTableObject: Fnd0StaticTable = None


@dataclass
class EventObject(TcBaseObj):
    """
    The 'EventObject' structure represents required parameter to get event type names for the businessObject.
    
    :var clientId: A unique identifier supplied by the caller. This ID is client's way of identifying event list.  This
    is a required parameter. If nothing is to be passed to clientId; assign an empty String object. Assigning NULL to
    clientId is not allowed.
    :var businessObject: The Business Object for which the valid Auditable and Subscribable event type list is to be
    retrieved. This is a required parameter.
    """
    clientId: str = ''
    businessObject: BusinessObject = None


@dataclass
class EventTypesOutput(TcBaseObj):
    """
    The 'EventTypesOutput' structure represents the outputs, auditableEvents and subscribableEvents, which are vectors
    of auditable event type names and subscribable event type names.
    
    :var clientId: Client unique identifier which is passed back for tracking the operation status.
    :var auditableEvents: The list of Auditable event type names.
    :var subscribableEvents: The list of Subscribable event type names
    """
    clientId: str = ''
    auditableEvents: List[str] = ()
    subscribableEvents: List[str] = ()


@dataclass
class EventTypesResponse(TcBaseObj):
    """
    The 'EventTypesResponse' structure represents the output response returning  a vector  of 'EventTypesOutput' with
    partial errors wrapped in  serviceData, if any.
    
    :var output: A vector of 'EventTypesOutput' structures packaged in custom response. Success is defined by the
    return of the 'ifailError' for getEventTypes on each of the 'businessObject'.
    :var serviceData: Partial failures will be returned in the ServiceDate for each failed processing. Error
    encountered while processing post event on element in the set is reported as partial errors and processing
    continues for the remaining elements in the input set.
    """
    output: List[EventTypesOutput] = ()
    serviceData: ServiceData = None


"""
This map has information about object and its properties.
"""
ObjectPropMap = Dict[BusinessObject, List[str]]


"""
A map of row attribute value pair. Value is vector to support typed reference attributes.
"""
RowAttrValueMap = Dict[str, List[str]]
