from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AttributeFormat(TcBaseObj):
    """
    Structure representing format details of a classification attribute.
    
    :var formatType: Integer representing the attribute type, which could be one of the following:
    - - 1 = KeyLOV 
    - 0 = String 
    - 1 = Integer 
    - 2 = Real 
    - 3 = Date 
    - 4 = Time range
    - 5= Boolean
    
    
    :var formatModifier1: Integer to indicate whether the attribute is configured for one of the following - 
    - 0 - Force positive number. 
    - 1 - Accept and display either + or - 
    - 2 - Accept + or - but display - sign only.
    
    
    Note: This field will return 0 if not applicable. Only applicable if the selected formatType is 1 or 2.
    :var formatModifier2: Integer to indicate additional information about the selected formatType from one of the
    following : 
    If formatType = 0 then:
    - 0 = Print characters in upper and lower case.
    - 1 = Print all characters in upper case.
    - 2 = Print all characters in lower case.
    
    
    If formatType == 2 then:
    - Number of digits after the decimal point.
    
    
    
    Note: This field will return 0 if not applicable. Only applicable if the selected formatType is 0 or 2.
    :var formatLength: Integer representing the length of the attribute. In case of a KeyLOV (stxt), or
    Cst0KeyLOVDefintion if attribute belongs to a Classification Standard Taxonomy (CST) class, this will contain the
    KeyLOV ID.
    """
    formatType: int = 0
    formatModifier1: int = 0
    formatModifier2: int = 0
    formatLength: int = 0


@dataclass
class ClassDefinition(TcBaseObj):
    """
    The list of Classification Class or View ID / IRDIs and corresponding definition.
    
    :var childCount: Number of child classes for this class.
    :var instanceCount: Total number of classification objects instantiated in this class or any of its descendants.
    :var viewCount: Number of Views defined for this class.
    :var options: Property describing classification class' flags represented as a single integer
    To access individual property flags, a bitwise operation will be required by the client. Valid values are:
    - CLASS_falg_englishUnitBase = 1
    - CLASS_flag_isGroup = 2
    - CLASS_flag_unit_system_both = 4
    - CLASS_flag_isStorageClass = 8
    - CLASS_flag_isAssembly = 16
    
    
    :var documents: A list of attached Icons, Images and NamedRefs to this class.
    :var properties: A list of classification class properties containing property ids and their values.
    :var attributes: A list of class attributes owned by this class definition.
    """
    childCount: int = 0
    instanceCount: int = 0
    viewCount: int = 0
    options: int = 0
    documents: List[ClassDocuments] = ()
    properties: List[PropertyInfo] = ()
    attributes: List[ClassAttribute] = ()


@dataclass
class ClassDocuments(TcBaseObj):
    """
    Structure holding the attached Icon, Image or NamedRef or this child class.
    
    :var documentType: Contains type of document attached. Valid values are:
    - icon 
    - image 
    - NamedRef
    
    
    :var ticket: File ticket identifier for the attached file.
    :var originalFileName: File name for this attachment.
    """
    documentType: str = ''
    ticket: str = ''
    originalFileName: str = ''


@dataclass
class ClassParents(TcBaseObj):
    """
    Structure representing classification class' parents details.
    
    :var parents: A list of class parents' details.
    """
    parents: List[ClassDefinition] = ()


@dataclass
class ClassificationInfo(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var classificationObj: The Classification object. If this is NULLTAG; a new classification object will be created
    otherwise existing classification object represented by 'classificationObj' will be updated.
    :var workspaceObject: The WorkspaceObject that is associated by this Classification object. If this is NULLTAG,
    then a standalone classification object was created or updated, if the classificationObj is set. Supported WSO
    types are defined by preference: 'ICS_allowable_types'.
    :var properties: List of properties containing attribute Ids and their values.
    """
    classificationObj: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[ClassificationObjectProperty] = ()


@dataclass
class ClassificationObjectInfo(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: The found Classification object.
    :var workspaceObject: The WorkspaceObject (WSO) that is associated by this Classification object. If this is
    NULLTAG, then the found "'clsObject'" is a standalone classification object.
    :var properties: List of properties containing, attributes ids and their values.
    """
    clsObject: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[PropertyInfo] = ()


@dataclass
class ClassificationObjectProperty(TcBaseObj):
    """
    Structure representing Classification Property which holds attribute ids and their values.
    
    :var attributeId: The ID, or IRDI if the attribute belongs to a CST class, of the attribute. For traditional
    classification attribute IDs, this is an integer that is converted into a string. For cases in which the attribute
    represents the Class ID or Class Name, this is a string representation of the identifier of those properties. These
    identifiers include:
    - CLASS_ID
    - CLASS_NAME
    - CLASS_TYPE
    - UNIT_SYSTEM
    - ATTRIBUTE_DEPENDENCY_ATTRIBUTE
    - ATTRIBUTE_DEPENDENCY_CONFIG
    - ATTRIBUTE_NAME
    - ATTRIBUTE_ID
    - USER_DATA_1
    - USER_DATA_2
    - CLASS_SHORT_NAME
    - MODIFICATION_DATE
    
    
    :var values: A list of values for this attribute in the context of a Classification object.
    For regular properties it&rsquo;s just one value. In case of VLA (variable length array) properties each value has
    its own entry.
    """
    attributeId: str = ''
    values: List[str] = ()


@dataclass
class ClassificationObjects(TcBaseObj):
    """
    Structure representing the Classification Objects of a WorkspaceObject.
    
    :var clsObjects: The list of Classification Object information.
    """
    clsObjects: List[ClassificationObjectInfo] = ()


@dataclass
class FindClassificationInfoResponse(TcBaseObj):
    """
    Structure representing the classification information returned by FindClassificationInfo operation.
    
    :var clsObjectDefs: A map (WorkspaceObject, 'ClassificationObjects') of workspace objects to a list of
    Classification objects.
    :var keyLOVDescriptors: A map (string, 'KeyLOVDef') of Classification KeyLOV IDs/IRDIs and its definitions pairs.
    :var clsClassDescriptors: A map (string, 'ClassDefinition') of Classification classes or view IDs/IRDIs and its
    corresponding definition pairs. This map also contains class attribute information.
    :var classParents: A map (string, 'ClassParents') of Classification classes or view IDs/IRDIs and its parents'
    definition pairs.
    :var classChildren: A map (string, 'ClassChildren') of Classification classes or view IDs/IRDIs and its children's
    definition pairs.
    :var clsBlockDescriptors: A map (string, 'ClassDefinition') of Classification classes IRDIs and its corresponding
    definition pairs. This map also contains class attribute information. This map is only used for Classification
    Standard Taxonomy (CST) property block information. This map differs from 'clsClassDescriptors' as it contains the
    information for property blocks that belong to the returned classes.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    clsObjectDefs: ClassificationObjectsDefMap = None
    keyLOVDescriptors: KeyLOVDefMap = None
    clsClassDescriptors: ClassDefinitionMap = None
    classParents: ClassParentsMap = None
    classChildren: ClassChildrenMap = None
    clsBlockDescriptors: BlockDefinitionMap = None
    serviceData: ServiceData = None


@dataclass
class FormatProperties(TcBaseObj):
    """
    Structure representing format details.
    
    :var formatDefinition: Attribute format definition.
    :var unitName: Unit display name associated with this attribute in this unit system.
    :var defaultValue: Default value of this Class attribute. This can be an empty string indicating no default value.
    :var minimumValue: Minimum value constraint of this Class attribute. This can be an empty string indicating no
    minimum value constraint.
    Note: Only applicable to numerical formats of attributes.
    :var maximumValue: Maximum value constraint of this Class attribute. This can be an empty string indicating no
    maximum value constraint.
    Note: Only applicable to numerical formats of attributes.
    """
    formatDefinition: AttributeFormat = None
    unitName: str = ''
    defaultValue: str = ''
    minimumValue: str = ''
    maximumValue: str = ''


@dataclass
class KeyLOVDef(TcBaseObj):
    """
    Structure representing KeyLOV (stxt or Cst0KeyLOVDefinition) definition.
    
    :var keyLOVOptions: KeyLOV (stxt or Cst0KeyLOVDefinition) options to show/hide keys. Valid values are: 
    - 0 = Show key 
    - 1 = Hide key
    
    
    :var keyLOVEntries: A list of KeyLOV (stxt or Cst0KeyLOVDefinition) entries.
    :var owningSite: Owning Site (POM_imc) of this keyLOV (stxt or Cst0KeyLOVDefinition) object.
    :var shatedSites: A list of sites (POM_imc) where this KeyLOV (stxt or Cst0KeyLOVDefinition) is shared using
    Multisite operations.
    :var keyLOVProperties: keyLOV (stxt or Cst0KeyLOVDefinition) properties containing property ids and their values.
    """
    keyLOVOptions: int = 0
    keyLOVEntries: List[KeyLOVEntry] = ()
    owningSite: BusinessObject = None
    shatedSites: List[BusinessObject] = ()
    keyLOVProperties: List[PropertyInfo] = ()


@dataclass
class KeyLOVEntry(TcBaseObj):
    """
    Structure representing KeyLOV (stxt or Cst0KeyLOVDefinition) Entry.
    
    :var keyLOVkey: String representing a Key of a KeyLOV (stxt or Cst0KeyLOVDefinition) entry.
    :var keyLOVValue: String representing a Value of the KeyLOV (stxt or Cst0KeyLOVDefinition) entry.
    :var isDeprecated: Indicating whether this KeyLOV (stxt or Cst0KeyLOVDefinition) entry is deprecated.
    If true, keyLOV entry is deprecated and cannot be used for new classifications; otherwise, it can be used for new
    classifications.
    """
    keyLOVkey: str = ''
    keyLOVValue: str = ''
    isDeprecated: bool = False


@dataclass
class PropValue(TcBaseObj):
    """
    Structure containing classification property value details.
    
    :var internalValue: Internal value stored into database.
    :var displayValue: Display value for a classification property. This will be same as that of 'internalValue' for
    all classification attributes except keyLOV (stxt) attributes as they will have "entry key" as 'internalValue' and
    "entry key entry value" or "entry value" as 'displayValue'; based on the keyLOV configuration.
    """
    internalValue: str = ''
    displayValue: str = ''


@dataclass
class PropertyInfo(TcBaseObj):
    """
    Structure representing Classification Property which holds attribute ids and their values.
    
    :var propertyId: A string representing the type attribute Id of the attribute. This could also be one of the
    following strings, which are string representations of internal ids:
    - CLASS_ID
    - CLASS_TYPE
    - CLASS_NAME
    - UNIT_SYSTEM
    - ATTRIBUTE_DEPENDENCY_ATTRIBUTE
    - ATTRIBUTE_DEPENDENCY_CONFIG
    - ATTRIBUTE_NAME
    - ATTRIBUTE_ID
    - USER_DATA_1
    - USER_DATA_2
    - CLASS_SHORT_NAME
    - MODIFICATION_DATE
    
    
    :var propertyName: The name of classification attribute or name of internal identifier for classification header
    properties like class Id, unit system etc.
    :var values: A list of values for this attribute.
    """
    propertyId: str = ''
    propertyName: str = ''
    values: List[PropValue] = ()


@dataclass
class SaveClassificationObjectsResponse(TcBaseObj):
    """
    Holds the classification objects returned by the 'saveClassificationObjects' operation.
    
    :var classificationObjects: A list of created or updated Classification objects.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    classificationObjects: List[ClassificationObjectInfo] = ()
    serviceData: ServiceData = None


@dataclass
class SearchCriteria(TcBaseObj):
    """
    A structure defining the search criteria used for searching classes from classification hierarchy. Also allows
    sorting the results based on a predefined criterion.
    
    :var searchAttribute: Class attribute to be searched for. Valid values are:
    - CLASS_ID
    - CLASS_NAME
    
    
    :var searchString: Query string to search the class by.
    :var sortOption: Option to sort the returned results. Valid values are:
    - -600 : Class Id
    - -607 : Class Name
    
    """
    searchAttribute: str = ''
    searchString: str = ''
    sortOption: int = 0


@dataclass
class ClassAttribute(TcBaseObj):
    """
    Structure representing class attribute details.
    
    :var attributeId: Classification attribute Id/IRDI.
    :var metricFormat: Attribute format definition in metric unit system.
    :var nonMetricFormat: Attribute format definition in non-metric unit system.
    :var arraySize: Array size or the number of values for this attribute.
    - If single valued (nonarray), then arraySize = 0 
    - If limited multi valued (array), then arraySize > 0 corresponding to the size of the array defined in the
    attribute definition.
    - If unlimited multi valued (array), then arraySize = -1
    
    
    :var options: Attribute property flags represented as a single integer. To access individual property flags, a
    bitwise operation will be required by the client. Valid values are:
    - ATTR_vla = 1
    - ATTR_external_vla = 2 
    - ATTR_mandatory = 4
    - ATTR_protected = 8
    - ATTR_unique = 16
    - ATTR_propagated = 32
    - ATTR_localValue = 64 
    - ATTR_reference = 128
    - ATTR_auto_computed = 256
    - ATTR_hidden = 512
    - ATTR_localizable = 1024
    
    
    :var attributeProperties: A list of classification attributes' property values. These properties could be attribute
    Id, attribute Name, attribute shortName etc.
    :var attributeKeyLOVDef: Configured KeyLOV definition information for this attribute.
    """
    attributeId: str = ''
    metricFormat: FormatProperties = None
    nonMetricFormat: FormatProperties = None
    arraySize: int = 0
    options: int = 0
    attributeProperties: List[PropertyInfo] = ()
    attributeKeyLOVDef: KeyLOVDef = None


@dataclass
class ClassChildren(TcBaseObj):
    """
    Structure representing classification class' children details.
    
    :var children: A list of class' children details.
    """
    children: List[ClassDefinition] = ()


"""
The list of Classification Class or View ID / IRDIs and corresponding definition.
"""
ClassDefinitionMap = Dict[str, ClassDefinition]


"""
A map of classification class Id / IRDI to a list of its parents.
"""
ClassParentsMap = Dict[str, ClassParents]


"""
Map of workspace object to a list of its classification objects or standalone classification objects with a matching ID to that of the WSO. If an object is classified then map value will have all its classification's information. If object is not classified, but system found standalone classification objects, then the map values will have standalone classification object's information. In the case of a standalone classification, the standalone classification&rsquo;s WSO tag will be a NULLTAG.
"""
ClassificationObjectsDefMap = Dict[WorkspaceObject, ClassificationObjects]


"""
A map of classification class Id / IRDI to a list of block property class definitions. Used by Classification Standard Taxonomy (CST) when a class has block properties.
"""
BlockDefinitionMap = Dict[str, ClassDefinition]


"""
The list of KeyLOV ids and corresponding KeyLOV definition. KeyLOV id and definition will be stxt BO if the class is a from traditional classification, or from Cst0KeyLOVDefinition BO if it is from Classification Standard Taxonomy (CST).
"""
KeyLOVDefMap = Dict[str, KeyLOVDef]


"""
A map of classification class Id / IRDI to a list of its children.
"""
ClassChildrenMap = Dict[str, ClassChildren]
