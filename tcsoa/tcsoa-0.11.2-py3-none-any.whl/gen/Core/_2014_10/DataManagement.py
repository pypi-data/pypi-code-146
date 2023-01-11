from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2008_06.DataManagement import CreateInput
from tcsoa.gen.Core._2013_05.DataManagement import DeepCopyData
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateIdInput(TcBaseObj):
    """
    - createInput    Holds property-value information for creating objects.
    - propertyName    Name of the Business Object's Property for which the ID is generated.
    - quantity    Number of IDs to be generated.
    
    
    
    :var createInput: Holds property-value information for Item and its subtypes.
    :var propertyName: Name of the Business Object's Property for which the ID is generated.
    :var quantity: Number of IDs to be generated.
    """
    createInput: CreateInput = None
    propertyName: str = ''
    quantity: int = 0


@dataclass
class GenerateIdResponseStruct(TcBaseObj):
    """
    Structure for holding GenerateIdResponse for each CreateIdInput.
    
    :var generatedIDs: List of generated IDs.
    """
    generatedIDs: List[str] = ()


@dataclass
class GenerateIdsResponse(TcBaseObj):
    """
    - generateIdsOutput : Multiple lists of Generated IDs. Each list corresponds to the individual elements in
    GenerateIdInputs
    - serviceData : Holds error stacks
    
    
    
    :var generateIdsOutput: Multiple lists of Generated IDs. Each list corresponds to the individual elements in
    GenerateIdInputs.
    :var serviceData: Holds error stacks.
    """
    generateIdsOutput: List[GenerateIdResponseStruct] = ()
    serviceData: ServiceData = None


@dataclass
class GetDeepCopyDataResponse(TcBaseObj):
    """
    Structure that contains the DeepCopyData embedded within which is a recursive data structure. The DeepCopyData
    contains information about how the secondary objects (related and referenced objects) are to be copied (reference,
    copy as object, no copy).
    
    :var deepCopyInfoMap: A map of business objects and DeepCopyData (POM_object/DeepCopyData). Each business object
    from the method input will have a DeepCopyData in the map. The DeepCopyData object contains all the information
    about how the attached objects are to be copied (Copy as Object, Copy as Reference, NoCopy, etc.). DeepCopyData is
    a recursive data structure that contains the details for the attached objects at the next level.
    :var serviceData: Service data containing errors, etc. The plain object list of the Service data is populated with
    the target objects which are to be copied as part of the SaveAs/revise operation. If there is an error retrieving
    Business Object for the business object name corresponding to the target object, it is added to the error stack of
    the ServiceData as a partial error
    """
    deepCopyInfoMap: DeepCopyInfoMap = None
    serviceData: ServiceData = None


@dataclass
class GetPasteRelationsOutput2(TcBaseObj):
    """
    The struct data to be returned. This struct contains a clientId, a list of PasteRelationInfo2 instances, and a
    preferred index of relation in the list pasreRelInfo.
    
    :var clientId: Unique client identifier
    :var pasteRelInfo: A list of paste relations info to be returned
    :var indexOfPreferred: The zero-based index of the preferred paste relation in the list pasreRelInfo.
    
    """
    clientId: str = ''
    pasteRelInfo: List[PasteRelationsInfo2] = ()
    indexOfPreferred: int = 0


@dataclass
class GetPasteRelationsResponse2(TcBaseObj):
    """
    Response structure contains a list of GetPasteRelationsOutput2 and ServiceData
    
    :var outputs: A list of paste relation output.
    :var serviceData: 'Service Data' including partial errors that are mapped to the client id from the input. Created
    objects are also added to the created objects list in the 'Service Data'.
    """
    outputs: List[GetPasteRelationsOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class PasteRelationsInfo2(TcBaseObj):
    """
    This struct contains the internal name and display name of the relation as well as a flag indicating whether the
    relation will enable the children to be shown under the parent when expanded.
    
    :var pastRelName: The internal name of paste relation
    :var pastRelDisplayName: The displayname of paste relation
    :var isExpandable: If true, will enable the children to be shown under the parent when expanded.
    
    """
    pastRelName: str = ''
    pastRelDisplayName: str = ''
    isExpandable: bool = False


@dataclass
class SaveAsIn(TcBaseObj):
    """
    This structure holds information about the target object, a map of the property name as key and as a value carries
    a list of the corresponding values for that property name and the deep copy data of the objects attached to the
    target object.
    
    :var targetObject: The target business object.
    :var inputPropValues: A map of property name (as key) and property values (as value) in string format. Each value
    is a list of strings to support both single valued and multi valued properties of types. The calling client is
    responsible for converting the different property types (like integer, double, date, etc) to a string using the
    appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
    :var deepCopyDatas: DeepCopyData of the objects attached to the target object.
    """
    targetObject: BusinessObject = None
    inputPropValues: PropertyValuesMap = None
    deepCopyDatas: List[DeepCopyData] = ()


@dataclass
class ChildrenInputData(TcBaseObj):
    """
    This is the input structure which will be used by the AddChildren and RemoveChildren service operations.
    
    :var clientId: An unique string supplied by the caller. This Id is used by the response to identify the failed
    add/remove children.
    
    :var parentObj: A parent object to which the child objects would be added or removed.
    :var childrenObj: List of objects which are added or removed as children to parent object.
    :var propertyName: The name of  the property that relates  the child objects to the parent. 
    The property can be a relation property or reference property or empty.
    """
    clientId: str = ''
    parentObj: BusinessObject = None
    childrenObj: List[BusinessObject] = ()
    propertyName: str = ''


@dataclass
class DeepCopyData(TcBaseObj):
    """
    DeepCopyData stores the deep copy information that will be copied via saveAs or revise operation. It also stores
    the nested deep copy data at the next level. 
    
    :var attachedObject: The related object to be deep copied.
    :var propertyValuesMap: Map of DeepCopyData ( string, list of strings ). It can contain the following attributes:
    
    - isRequired If true, the copy action can not be modified. If false, the copy action can be changed different
    action by the user.
    - propertyName Name of relation type or reference property for which DeepCopy rule is configured.
    - copyAction DeepCopy action Supported values are as following: NoCopy, CopyAsReference, CopyAsObject or Select.
    - isTargetPrimary If true the target object is processed as primary, otherwise it is processed as a secondary
    object.
    - copy_relations If true, the custom properties on the source relation object are copied over to the newly-created
    relation. If false, custom properties are not copied.
    - secondaryIsDuplicated if true, the attached object already appears in deep copy data
    - propertyType If Relation, it represents Relation type property. If Reference, it represents Reference property.
    
    
    :var operationInputTypeName: Object type name of the operation being perfomed
    :var childDeepCopyData: List of DeepCopyData for the objects of the relation or reference property objects of the
    attached object.
    :var operationInputs: Map to provide input property names and values of attached object. These property values will
    be applied on copied object. Map of property name(key) and property values(values) (string, list of strings) in
    string format of attached object, to be set on copied object of attached object. The calling client is responsible
    for converting the different property types (int, float, date .etc) to a string using the appropriate toXXXString
    functions in the SOA client framework Property class.
    """
    attachedObject: BusinessObject = None
    propertyValuesMap: PropertyValuesMap = None
    operationInputTypeName: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    operationInputs: PropertyValuesMap = None


@dataclass
class DeepCopyDataInput(TcBaseObj):
    """
    Input structure for getDeepCopyData operation
    
    :var operation: This is the operation types such as SaveAs,Revise, etc.
    :var businessObject: object reference to get the deepcopydata
    """
    operation: str = ''
    businessObject: BusinessObject = None


"""
Map contains a list of pairs (BusinessObject whose type is POM_object or its subtype, list). For each pair, name is the business object and value holds deep copy data for the business object.
"""
DeepCopyInfoMap = Dict[BusinessObject, List[DeepCopyData]]


"""
This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
"""
PropertyValuesMap = Dict[str, List[str]]
