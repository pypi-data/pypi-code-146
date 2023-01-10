from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindClassificationObjectsResponse(TcBaseObj):
    """
    Holds the classfication objects returned by the 'findClassificationObjects()' method.
    
    :var icos: Map of classified WorkspaceObjects and their associated Classification objects.
    :var data: Any failure will be returned with WorkspaceObject ID mapped to the error message in the ServiceData list
    of partial errors.
    """
    icos: WsoIcoMap = None
    data: ServiceData = None


@dataclass
class FindClassifiedObjectsResponse(TcBaseObj):
    """
    Holds the classified objects returned by the  'getFindClassifiedObjects()' method.
    
    :var wsos: List of classified WorkspaceObjects found for the given list of Classification objects.
    :var data: Any failure will be returned with WorkspaceObject ID mapped to the error message in the ServiceData list
    of partial errors.
    """
    wsos: List[WorkspaceObject] = ()
    data: ServiceData = None


@dataclass
class GetAttributesForClassesResponse(TcBaseObj):
    """
    Contains a list of Child Classes found for the given Classes
    
    :var attributes: Map of Class IDs and the Class attributes found for each of those classes
    :var data: Any failure will be returned with Class ID mapped to the error message in the ServiceData list of
    partial errors.
    """
    attributes: StrVClsAttrMap = None
    data: ServiceData = None


@dataclass
class GetChildrenResponse(TcBaseObj):
    """
    Contains a list of Child Classes found for the given Classes
    
    :var children: Map of Child classes found for input Class IDs.
    :var data: Any failures with Class ID mapped to the error message are returned in the ServiceData list of partial
    errors.
    """
    children: StrVChildDefMap = None
    data: ServiceData = None


@dataclass
class GetClassDescriptionsResponse(TcBaseObj):
    """
    Contains a list of Child Classes found for the given Classes.
    
    :var descriptions: Map of Child classes found for input Class IDs.
    :var data: Internal errors encounterd during the operation are added to the partial errors.
    """
    descriptions: StrClsDescMap = None
    data: ServiceData = None


@dataclass
class GetClassificationObjectsResponse(TcBaseObj):
    """
    Holds the classification object details returned by the 'GetClassificationObjects()' operation.
    
    :var clsObjs:  TagClsObjMap map of input classification object to its details.
    :var data: Any failure will be returned with Classification Object ID mapped to the error message in the
    'ServiceData' list of partial errors.
    """
    clsObjs: TagClsObjMap = None
    data: ServiceData = None


@dataclass
class GetFileIdAttributes(TcBaseObj):
    """
    Contains a list of child classes found for the given classes.
    
    :var relation: Name of the relation for attachement.
    :var datasetType: Internal type of the attached Dataset object.
    :var namedRefs: List of named references.
    """
    relation: str = ''
    datasetType: str = ''
    namedRefs: List[str] = ()


@dataclass
class GetFileIdCriteria(TcBaseObj):
    """
    Contains a list of child classes found for a class in the classification hierarchy.
    
    :var wsos: List of associated 'WorkspaceObjects' to execute the search for File IDs.
    :var criteria: Reference to the search criterion.
    """
    wsos: List[WorkspaceObject] = ()
    criteria: GetFileIdAttributes = None


@dataclass
class GetFileIdsResponse(TcBaseObj):
    """
    Contains a list of child classes found for the given classes
    
    :var ids: References to map of WorkspaceObject objects and attached Document objects.
    :var data: Internal errors encounterd during the operation are added to the partial errors.
    """
    ids: ObjTicketMap = None
    data: ServiceData = None


@dataclass
class GetKeyLOVsResponse(TcBaseObj):
    """
    Holds the key-LOV returned by the 'getKeyLOVs()' method.
    
    :var keyLOVs: Map of Key-LOV definitions details.
    :var data: Any failure will be returned with the Key-LOV ID mapped to the error message in the 'ServiceData' list
    of partial errors.
    """
    keyLOVs: StrKeyLOVDefMap = None
    data: ServiceData = None


@dataclass
class GetParentsResponse(TcBaseObj):
    """
    Holds the parents returned by the 'getParents()'' 'method.
    
    :var parents: Map contains a list of parents for each of the input Class IDs
    :var data: Internal errors encounterd during the operation are added to the partial errors.
    """
    parents: StrParentVecMap = None
    data: ServiceData = None


@dataclass
class GetPartFamilyTemplatesResponse(TcBaseObj):
    """
    Holds the PartFamilyTemplates returned by the 'getPartFamilyTemplates()'' 'method.
    
    :var wsos: Map of part family templates found for input Class IDs.
    :var data: Failures mapped to the error message in the 'ServiceData' list of partial errors.
    """
    wsos: StringPOMRefVecMap = None
    data: ServiceData = None


@dataclass
class KeyLOVDefinition(TcBaseObj):
    """
    Structure representing KeyLOVDefinition
    
    :var name: Name of the Key-LOV.
    :var options: Key-LOV options to Show/Hide keys.
    Valid values are  
    - 0 = Show key
    - 1 = Hide key
    
    
    :var keyValuePairs: Map of the Key-Value pairs.
    """
    name: str = ''
    options: int = 0
    keyValuePairs: StrStrMap = None


@dataclass
class AttributeFormat(TcBaseObj):
    """
    Structure representing format details of an attribute
    
    :var formatType: Integer representing the attribute type, which could be one of the following
    - - 1 => KeyLOV
    - 0 => String
    - 1 => Integer
    - 2 => Real
    - 3 => Date
    - 4 => Time range
    
    
    :var formatModifier1: Integer to indicate whether the attribute is configured for one of the following - 
    - 0 - Force positive number
    - 1 - Accept and display either + or -
    - 2 - Accept + or - but display - sign only
    
    
    Note: This field will return 0 if not applicable. Only applicable if the selected formatType is 1 or 2
    :var formatModifier2: Integer to indicate additional information about the selected formatType from one of the
    following : 
    If formatType = 0 then:
    - 0 = Print characters in upper and lower case
    - 1 = Print all characters in upper case
    - 2 = Print all characters in lower case
    
    
    If formatType = 2 then Number of digits after the decimal point
    
    Note: This field will return 0 if not applicable. Only applicable if the selected formatType is 0 or 2
    :var formatLength: Integer representing the length of the attribute. In case of a Key-LOV, this will contain the
    Key-LOV ID.
    """
    formatType: int = 0
    formatModifier1: int = 0
    formatModifier2: int = 0
    formatLength: int = 0


@dataclass
class SearchAttribute(TcBaseObj):
    """
    Structure SearchAttribute holds the attribute id and expression for attribute search
    
    :var attributeId: Alphanumeric attribute ID of the attribute used in this search.
    :var query: Query expression for this attribute e.g. >= 20.00. Supported Operators are: 
    - Equals - "="
    - Less than - "<"
    - Greater than - ">" 
    - Greater than or equal to - ">="
    - Less than or equal to - "<=",
    - OR - "|"
    - AND - "&"
    
    """
    attributeId: int = 0
    query: str = ''


@dataclass
class SearchByInstanceIdResponse(TcBaseObj):
    """
    Holds the Instance identifier returned by the 'getSearchByInstanceId'() method.
    
    :var clsObjTags: Retrieved classification objects.
    :var data: Any failure will be returned with classification object IDs mapped to the error message in the
    'ServiceData' list of partial errors.
    """
    clsObjTags: StrTagVecMap = None
    data: ServiceData = None


@dataclass
class SearchClassAttributes(TcBaseObj):
    """
    SearchClassAttributes holds classIds and expressions to search class attributes
    
    :var classIds: List of class IDs to perform search
    :var searchAttributes: List of references to the search attributes in these classes.
    :var searchOption: Unused parameter for this operation.
    """
    classIds: List[str] = ()
    searchAttributes: List[SearchAttribute] = ()
    searchOption: int = 0


@dataclass
class SearchForClassesCriteria(TcBaseObj):
    """
    Searches for classes based on the specified class attribute. Also allows sorting the results based on a predefined
    criterion. Search criteria must be specified and cannot be empty.
    
    :var searchAttribute: Class attribute to be searched for. Valid values are as defined in enum
    'ClassSearchAttribute'.
    :var searchString: Query string to search the class attribute by.
    :var sortOption: Option to sort the returned results. Valid values are as defined in enum 'ClassSortOption'.
    """
    searchAttribute: ClassSearchAttribute = None
    searchString: str = ''
    sortOption: ClassSortOption = None


@dataclass
class SearchForClassesResponse(TcBaseObj):
    """
    Returns a 'SearchForClassesResponse' structure containing:
    - Retrieved classes in the 'ServiceData' list of plain objects
    - Any failures with class ID mapped to the error message in the 'ServiceData' list of partial errors.
    
    
    
    :var classes: Map of search criteria index and the classes found for each of those searches.
    :var data: Internal errors encounterd during the operation are added to the partial errors
    """
    classes: IntClassDefVecMap = None
    data: ServiceData = None


@dataclass
class SearchResponse(TcBaseObj):
    """
    SearchResponse holds the response of search details
    
    :var clsObjTags: Map of the input query strings and references to the retrieved objects.
    :var data: Any failure will be returned mapped to the error message in the 'ServiceData' list of partial errors.
    """
    clsObjTags: StrTagVecMap = None
    data: ServiceData = None


@dataclass
class TypedDocument(TcBaseObj):
    """
    Structure holding the attached Icon, Image or NamedRef or this child class.
    
    :var documentType: Contains type of document attached. Valid values are:
    - icon
    - image
    - NamedRef
    
    
    :var ticket: Ticket identifier for the attached file
    :var originalFileName: File name for this attachment.
    """
    documentType: str = ''
    ticket: str = ''
    originalFileName: str = ''


@dataclass
class UpdateClassificationObjectsResponse(TcBaseObj):
    """
    UpdateClassificationObjectsResponse
    
    :var clsObjs: List of updated Classification objects.
    :var data: Any failure will be returned with Classification object ID mapped to the error message in the
    'ServiceData' list of partial errors.
    """
    clsObjs: List[ClassificationObject] = ()
    data: ServiceData = None


@dataclass
class ChildDef(TcBaseObj):
    """
    Structure representing Child Definition
    
    :var id: Child class ID.
    :var type: Type of Class. Valid values are -
    - Group                 = (1 << 0)
    - Class                  = (1 << 1)
    - View                   = (1 << 2)
    - Storage class     = (1 << 4)
    
    
    :var name: Name of the child class
    :var description: Description of the child class
    :var childCount: Number of children underneath this child class.
    :var instanceCount: Number of instances of classification objects in this child class and its descendents.
    :var viewCount: Number of views for this child class.
    :var documents: List of references to the 'TypedDocument' structure containing Documents attached to this child
    class.
    """
    id: str = ''
    type: str = ''
    name: str = ''
    description: str = ''
    childCount: int = 0
    instanceCount: int = 0
    viewCount: int = 0
    documents: List[TypedDocument] = ()


@dataclass
class ClassAttribute(TcBaseObj):
    """
    Contains a list of Child Classes found for the given Classes
    
    :var id: Integer ID for this attribute
    :var name: Name for this attribute
    :var description: Description added for this attribute.
    :var arraySize: Array size or the number of values for this attribute
    - If single valued (non array), then 'arraySize' = 1
    - If multi valued (array), then 'arraySize' >= 1 corresponding to the size of the array defined in the attribute
    definition.
    
    
    :var options: Attribute property flags represented as a single integer.
    To access individual property flags, a bitwise operations will be required by the client.
    Valid values are:
    - ATTR_vla                      = (1 << 0)
    - ATTR_external_vla      = (1 << 1)
    - ATTR_mandatory         = (1 << 2)
    - ATTR_protected             = (1 << 3)
    - ATTR_unique                 = (1 << 4)
    - ATTR_propagated         = (1 << 5)
    - ATTR_localValue             = (1 << 6)
    - ATTR_reference             = (1 << 7)
    - ATTR_auto_computed = (1 << 15)
    - ATTR_hidden                = (1 << 20)
    - ATTR_localizable        = (1 
    
    
    :var preConfig: Preconfiguration attached to the attribute.
    :var config: Base configuration attached to the attribute
    :var postConfig: Post configuration attached to the attribute.
    Configurations could be any combinations of the following individual configurations:
    - multifield
    - horizontal
    - vertical
    - separator
    - arrow
    - button
    - wide
    - mandatory flag
    - protected flag
    - unique flag
    
    
    :var shortName: Short name defined for this attribute
    :var annotation: Annotation information added to this attribute
    :var format: References the 'FormatProperties' structure defining the metric format of this attribute.
    :var altFormat: References the FormatProperties structure defining the nonmetric format of this attribute.
    :var unitName: Unit display name associated with this attribute in this unit system.Note: Only applicable to
    numerical formats of attributes.
    :var defaultValue: Default value of this Class attribute. This can be an empty string indicating no default value.
    :var minValue: Minimum value constraint of this Class attribute. This can be an empty string indicating no minimum
    value constraint.
    Note: Only applicable to numerical formats of attributes.
    :var maxValue: Maximum value contraint of this Class attribute. This can be an empty string indicating no maximum
    value constraint.
    Note: Only applicable to numerical formats of attributes.
    """
    id: int = 0
    name: str = ''
    description: str = ''
    arraySize: int = 0
    options: int = 0
    preConfig: str = ''
    config: str = ''
    postConfig: str = ''
    shortName: str = ''
    annotation: str = ''
    format: AttributeFormat = None
    altFormat: AttributeFormat = None
    unitName: str = ''
    defaultValue: str = ''
    minValue: str = ''
    maxValue: str = ''


@dataclass
class ClassDef(TcBaseObj):
    """
    Properties of the given class.
    
    :var id: Class ID
    :var parent: Class ID of the parent class.
    :var instanceCount: Total number of classification objects instantiated in this class or any of its descendents
    :var viewCount: Number of 'Views' defined for this class
    :var documents: List of attached 'Icons', 'Images' and 'NamedRefs' to this class
    :var name: Class name
    :var shortName: Short name
    :var description: Class description
    :var unitBase: Unit system of the class. See enum 'UnitBase' for list of valid values
    :var options: Class options as specified in the enum 'ClassFlags' below
    :var userData1: User data 1 added to this class
    :var userData2: User data 2 added to this class
    :var childCount: Number of child classes for this class
    """
    id: str = ''
    parent: str = ''
    instanceCount: int = 0
    viewCount: int = 0
    documents: List[TypedDocument] = ()
    name: str = ''
    shortName: str = ''
    description: str = ''
    unitBase: UnitBase = None
    options: ClassFlags = None
    userData1: str = ''
    userData2: str = ''
    childCount: int = 0


@dataclass
class ClassFlags(TcBaseObj):
    """
    Contains a list of child classes found for the given classes.
    
    :var isValid: - True value indicates that the class is a valid class. The option is for future use and currently is
    set by default to true internally.
    
    
    :var isAbstract: True value indicates that the class is abstract class, else storage class.
    :var isGroup: True value indicates that the class is a group.
    :var isAssembly: True value indicates that the class is an assembly.
    """
    isValid: bool = False
    isAbstract: bool = False
    isGroup: bool = False
    isAssembly: bool = False


@dataclass
class ClassificationObject(TcBaseObj):
    """
    Structure representing Classification Object details
    
    :var clsObjTag: Reference of Classification object.
    :var instanceId: Alphanumeric ID of the Classification object.
    :var classId: Unique Alphanumeric ID of the Classification class where this object was created.
    :var unitBase: Unit system of measure in which the Classification object is stored in.
    :var wsoId: Reference of the WorkspaceObject (WSO) that is associated by this Classification object. This can be
    empty. Allowed WSO types will be defined by the preference 'ICS_allowable_types'.
    
    :var properties: Array of Classification attributes references that store the properties of this Classification
    object.
    """
    clsObjTag: BusinessObject = None
    instanceId: str = ''
    classId: str = ''
    unitBase: UnitBase = None
    wsoId: WorkspaceObject = None
    properties: List[ClassificationProperty] = ()


@dataclass
class ClassificationProperty(TcBaseObj):
    """
    Structure representing Classification Property which holds attribute ids  and their values
    
    :var attributeId: Holds the unique identifier of an attribute.
    :var values: Holds a array of values for this attribute in the context of a Classification object.
    [Note: An array is required as an attribute can be single or multi-valued.]
    
    """
    attributeId: int = 0
    values: List[ClassificationPropertyValue] = ()


@dataclass
class ClassificationPropertyValue(TcBaseObj):
    """
    Holds the 'DB value' and  an optional 'Display value' of a property
    
    :var dbValue: Value of the Classification attribute as stored in the database.
    :var displayValue: Value of the Classification attribute as  it should displayed in the client. 
    [ For example, If the attribute is a Key-LOV then the Key is stored as the 'dbValue', while the 'displayValue' can
    be configured to be either of the following based on the Key-Value pairs in the Key-LOV definition: 
    - "Value" only.
    - Concatenated "Key" and "Value". ]
    
    """
    dbValue: str = ''
    displayValue: str = ''


@dataclass
class CreateClassificationObjectsResponse(TcBaseObj):
    """
    Holds the classification objects returned by the 'getCreateClassificationObjects()' method.
    
    :var clsObjs: List of created Classification objects.
    :var data: Any failure will be returned with Classification object ID mapped to the error message in the
    ServiceData list of partial errors.
    """
    clsObjs: List[ClassificationObject] = ()
    data: ServiceData = None


class ClassSearchAttribute(Enum):
    """
    Enumerates the class attributes available for searching.
    
    :var CSA_CLASSID: The ID of the Classification class.
    :var CSA_CLASSNAME: The name of the Classification class.
    :var CSA_CLASSTYPE: The type of the Classification class.
    :var CSA_SHORTNAME: The short name of the Classification class.
    :var CSA_GROUPID: The group ID of the Classification class.
    :var CSA_USERDATA1: User data 1 added to the class.
    :var CSA_USERDATA2: User data 2 added to the class.
    :var CSA_ATTRID: The attribute id of the Classification class.
    :var CSA_ATTRNAME: The attribute name of the Classification class.
    """
    CSA_CLASSID = 'CSA_CLASSID'
    CSA_CLASSNAME = 'CSA_CLASSNAME'
    CSA_CLASSTYPE = 'CSA_CLASSTYPE'
    CSA_SHORTNAME = 'CSA_SHORTNAME'
    CSA_GROUPID = 'CSA_GROUPID'
    CSA_USERDATA1 = 'CSA_USERDATA1'
    CSA_USERDATA2 = 'CSA_USERDATA2'
    CSA_ATTRID = 'CSA_ATTRID'
    CSA_ATTRNAME = 'CSA_ATTRNAME'


class ClassSortOption(Enum):
    """
    Enumerates the sort options available for listing the search results.
    
    :var CSO_CLASSID: The ID of the Classification class.
    :var CSO_CLASSNAME: The name of the Classification class.
    :var CSO_CLASSTYPE: The type of the Classification class.
    :var CSO_SHORTNAME: The short name of the Classification class.
    :var CSO_GROUPID: The group ID of the Classification class.
    :var CSO_USERDATA1: User data 1 added to the class.
    :var CSO_USERDATA2: User data 2 added to the class.
    :var CSO_ATTRID: The attribute ID of the Classification class.
    :var CSO_ATTRNAME: The attribute name of the Classification class.
    """
    CSO_CLASSID = 'CSO_CLASSID'
    CSO_CLASSNAME = 'CSO_CLASSNAME'
    CSO_CLASSTYPE = 'CSO_CLASSTYPE'
    CSO_SHORTNAME = 'CSO_SHORTNAME'
    CSO_GROUPID = 'CSO_GROUPID'
    CSO_USERDATA1 = 'CSO_USERDATA1'
    CSO_USERDATA2 = 'CSO_USERDATA2'
    CSO_ATTRID = 'CSO_ATTRID'
    CSO_ATTRNAME = 'CSO_ATTRNAME'


class UnitBase(Enum):
    """
    UNSPECIFIED Both or no unit system of measure.
    METRIC Metric unit system of measure.
    ENGLISH Non-metric unit system of measure.
    """
    UNSPECIFIED = 'UNSPECIFIED'
    METRIC = 'METRIC'
    ENGLISH = 'ENGLISH'


"""
Map of search criteria index and the classes found for each of those searches
"""
IntClassDefVecMap = Dict[int, List[ClassDef]]


"""
References to map of WorkspaceObject objects and attached Document objects.
"""
ObjTicketMap = Dict[WorkspaceObject, List[TypedDocument]]


"""
Map of Class IDs and their respective child Class IDs
"""
StrClsDescMap = Dict[str, ClassDef]


"""
Structure elements:

- keyLOVs - Map of Key-LOV definitions details.
- data     - Any failure will be returned with the Key-LOV ID mapped to the error message in the 'ServiceData' list of partial errors.


"""
StrKeyLOVDefMap = Dict[str, KeyLOVDefinition]


"""
Map contains a list of parents Class IDs for each of the input Class ID.
"""
StrParentVecMap = Dict[str, List[str]]


"""
Structure elements:

- primary key - String representing a key of a Key-LOV entry. 
- value - String representing a value  of the Key-LOV  entry.


"""
StrStrMap = Dict[str, str]


"""
Maps the query string and the resulting Objects (identified by a tag)

Structure elements:

- primary key - Input query string used for this search.
- values - References of the objects found for this query string.


"""
StrTagVecMap = Dict[str, List[BusinessObject]]


"""
Map of Class IDs and their respective child Class IDs. For every Class ID, there will be a list of Child Class IDs.
"""
StrVChildDefMap = Dict[str, List[ChildDef]]


"""
Contains a list of Child Classes found for the given Classes.

Structure elements:

- Primary key : Alpha-numeric Class ID for which class attributes are being asked for.
- Values : List of references to ClassAttribute structures.


"""
StrVClsAttrMap = Dict[str, List[ClassAttribute]]


"""
Structure elements:

- primary key - Class IDs.
- values - List of the retreived part family template references


"""
StringPOMRefVecMap = Dict[str, List[WorkspaceObject]]


"""
Map of Classification Object tag to the details of Classification Object.


- Key - Classification Object tag.
- Value - ClassificationObject structure representing Classification Object details.


"""
TagClsObjMap = Dict[BusinessObject, ClassificationObject]


"""
- primary key : Reference of the classified WorkspaceObject  that was used to find the classification objects.
- Values : List of Classification object references associated with the classified WorksoaceObject referenced in the primary key


"""
WsoIcoMap = Dict[WorkspaceObject, List[BusinessObject]]
