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
    - - 1 => KeyLOV 
    - 0 => String 
    - 1 => Integer 
    - 2 => Real 
    - 3 => Date 
    - 4 => Time range.
    
    
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
    
    
    
    If formatType == 2 then Number of digits after the decimal point
    
    Note: This field will return 0 if not applicable. Only applicable if the selected formatType is 0 or 2.
    :var formatLength: Integer representing the length of the attribute. In case of a KeyLOV (stxt), this will contain
    the KeyLOV ID.
    """
    formatType: int = 0
    formatModifier1: int = 0
    formatModifier2: int = 0
    formatLength: int = 0


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
class ClassSearchCriteria(TcBaseObj):
    """
    A structure defining the search criteria used for searching classes from classification hierarchy.  Also allows
    sorting the results based on a predefined criterion.
    
    :var searchAttribute: Class attribute to be searched for. Valid values are all class properties like class Id,
    class Name etc.
    :var searchString: Query string to search the class attribute by.
    :var sortOption: Option to sort the returned results. Valid values are the class properties like class Id, class
    Name etc.
    """
    searchAttribute: int = 0
    searchString: str = ''
    sortOption: int = 0


@dataclass
class ClassificationObjectInfo(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: The found Classification object.
    :var workspaceObject: The WorkspaceObject (WSO) that is associated by this Classification object. If this is
    NULLTAG, then the found "clsObject" is a standalone classification object (ICO). Allowed WSO types will be defined
    by the preference 'ICS_allowable_types'.
    :var properties: List of properties containing, attribute Ids and their values.
    """
    clsObject: BusinessObject = None
    workspaceObject: WorkspaceObject = None
    properties: List[ClsProperty] = ()


@dataclass
class ClassificationObjects(TcBaseObj):
    """
    A structure representing list of classification objects information.
    
    :var clsObjects: A list of classification object's information.
    """
    clsObjects: List[ClassificationObjectInfo] = ()


@dataclass
class ClsPropValue(TcBaseObj):
    """
    Structure containing classification property value details.
    
    :var internalValue: Internal value stored into database.
    :var displayValue: Display value for a classification property. This will be same as that of internalValue for all
    classification attributes except keyLOV (stxt) attributes as they will have "entry key" as internalValue and "entry
    key entry value" or "entry value" as displayValue; based on the keyLOV configuration.
    """
    internalValue: str = ''
    displayValue: str = ''


@dataclass
class ClsProperty(TcBaseObj):
    """
    Structure representing Classification Property which holds attribute ids and their values.
    
    :var propertyId: The unique identifier of classification attribute or internal identifier for classification header
    properties like class Id, unit system etc.
    :var propertyName: The name of classification attribute or name of internal identifier for classification header
    properties like class Id, unit system etc.
    :var values: A list of values for this attribute.
    [Note: An array is required as an attribute can be single or multi-valued.]
    """
    propertyId: int = 0
    propertyName: str = ''
    values: List[ClsPropValue] = ()


@dataclass
class ExtendedProperties(TcBaseObj):
    """
    Structure representing classification attributes' extended metadata properties details.
    
    :var propName: Extended metadata property name.
    :var propValues: A list of extended metadata property values.
    """
    propName: str = ''
    propValues: List[ClsPropValue] = ()


@dataclass
class FindClassificationsResponse(TcBaseObj):
    """
    Structure representing the classification information returned by FindClassifications operation.
    
    :var clsObjectDefMap: A map (WorkspaceObject/ClassificationObjectInfo) of workspace objects to a list of
    Classification objects.
    :var keyLOVDefMap: A map (string/KeyLOVDefinition) of Classification KeyLOV IDs and its definitions pairs .
    :var clsAttrdefMap: A map (string/ClassAttributesDefinition) of Classification class or view IDs and its definition
    pairs .
    :var clsDefMap: A map (string/ClassDefinition) of Classification class or view IDs and its corresponding definition
    pairs.
    :var clsParentsMap: A map (string/ClassParents) of Classification classes or view IDs and its parents' definition
    pairs.
    :var clsChildrenMap: A map (string/ClassChildren) of Classification classes or view IDs and its children's
    definition pairs.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    clsObjectDefMap: ClsObjectsDefinitionMap = None
    keyLOVDefMap: KeyLOVDefinitionMap = None
    clsAttrdefMap: ClassAttributeDefinitionMap = None
    clsDefMap: ClassDefinitionMap = None
    clsParentsMap: ClassParentsMap = None
    clsChildrenMap: ClassChildrenMap = None
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
class ClassAttribute(TcBaseObj):
    """
    Structure representing class attribute details.
    
    :var attributeId: Classification attribute Id.
    :var metricFormat: Attribute format definition in metric unit system.
    :var nonMetricFormat: Attribute format definition in non-metric unit system.
    :var arraySize: Array size or the number of values for this attribute.
    - If single valued (nonarray), then arraySize = 1 
    - If multi valued (array), then arraySize >= 1 corresponding to the size of the array defined in the attribute
    definition.
    
    
    :var options: Attribute property flags represented as a single integer. To access individual property flags, a
    bitwise operation will be required by the client.Valid values are:
    - ATTR_vla          = (1 << 0) 
    - ATTR_external_vla = (1 << 1) 
    - ATTR_mandatory     = (1 << 2) 
    - ATTR_protected     = (1 << 3) 
    - ATTR_unique         = (1 << 4) 
    - ATTR_propagated     = (1 << 5) 
    - ATTR_localValue     = (1 << 6) 
    - ATTR_reference     = (1 << 7) 
    - ATTR_auto_computed = (1 << 15) 
    - ATTR_hidden         = (1 << 20) 
    - ATTR_localizable = ( 1 << 22 )
    
    
    :var extendedProperties: A list of classification class attributes' extended metadata properties.
    :var attributeProperties: A list of classification attributes' property values. These properties could be attribute
    Id, attribute Name, attribute shortName etc.
    """
    attributeId: int = 0
    metricFormat: FormatProperties = None
    nonMetricFormat: FormatProperties = None
    arraySize: int = 0
    options: int = 0
    extendedProperties: List[ExtendedProperties] = ()
    attributeProperties: List[ClsProperty] = ()


@dataclass
class KeyLOVDefinition(TcBaseObj):
    """
    Structure representing KeyLOV (stxt) definition.
    
    :var keyLOVOptions: KeyLOV (stxt) options to Show/Hide keys. Valid values are: 
    - 0 = Show key 
    - 1 = Hide key
    
    
    :var keyLOVEntries: List of KeyLOV (stxt) entries.
    :var owningSite: Owning Site (POM_imc) of this keyLOV (stxt) object.
    :var sharedSites: List of sites (POM_imc) where this KeyLOV (stxt) is shared using Multisite operations.
    :var keyLOVProperties: keyLOV (stxt) properties like keyLOV Id, name etc. details.
    """
    keyLOVOptions: int = 0
    keyLOVEntries: List[KeyLOVEntry] = ()
    owningSite: BusinessObject = None
    sharedSites: List[BusinessObject] = ()
    keyLOVProperties: List[ClsProperty] = ()


@dataclass
class KeyLOVEntry(TcBaseObj):
    """
    Structure representing KeyLOV (stxt) Entry.
    
    :var keyLOVkey: String representing a Key of a KeyLOV (stxt) entry.
    :var keyLOVValue: String representing a Value of the KeyLOV (stxt) entry.
    :var isDeprecated: Flag indicating whether this KeyLOV (stxt) entry is deprecated.
    If true, keyLOV entry is deprecated and can not be used for new classifications otherwise, it can be used for new
    classifications.
    """
    keyLOVkey: str = ''
    keyLOVValue: str = ''
    isDeprecated: bool = False


@dataclass
class ClassAttributesDefinition(TcBaseObj):
    """
    The structure containing list of Classification class attributes definition and configured KeyLOV (stxt) definition.
    
    :var classAttributes: The list of attributes defined for the classification class.
    :var configKeyLOVMap: A map (int/KeyLOVDefinition) of attribute ID and KeyLOV (stxt) definition pairs, based on
    dependency configuration of an attribute.
    """
    classAttributes: List[ClassAttribute] = ()
    configKeyLOVMap: ConfiguredKeyLOVDefinitionMap = None


@dataclass
class ClassChildren(TcBaseObj):
    """
    Structure representing classification class' children details.
    
    :var children: A list of class' children details.
    """
    children: List[ClassDefinition] = ()


@dataclass
class ClassDefinition(TcBaseObj):
    """
    Structure holding properties information about the given class.
    
    :var childCount: Number of child classes for this class.
    :var instanceCount: Total number of classification objects instantiated in this class or any of its descendants.
    :var viewCount: Number of Views defined for this class.
    :var options: Property describing classification class' flags represented as a single integer.
    To access individual property flags, a bitwise operation will be required by the client. Valid values are:
    - CLASS_falg_englishUnitBase = (1 << 0 )
    - CLASS_flag_isGroup          = (1 << 1)
    - CLASS_flag_unit_system_both = (1 << 2)
    - CLASS_flag_isStorrageClass  = (1 << 4)
    - CLASS_flag_isAssembly       = (1 << 5)
    
    
    :var documents: A list of attached Icons, Images and NamedRefs to this class.
    :var properties: A list of classification class properties like class Id, Name, ShortName etc. details.
    """
    childCount: int = 0
    instanceCount: int = 0
    viewCount: int = 0
    options: int = 0
    documents: List[ClassDocuments] = ()
    properties: List[ClsProperty] = ()


"""
The list of Classification Class or View ID and corresponding definition.
"""
ClassDefinitionMap = Dict[str, ClassDefinition]


"""
A map of classification class Id to a list of its parents.
"""
ClassParentsMap = Dict[str, ClassParents]


"""
Map of workspace object to a list of its classification objects. If an object is classified then map value will have all its classification's information. If object is not classified but system found standalone classification objects then the map values will have standalone classification object's information.
"""
ClsObjectsDefinitionMap = Dict[WorkspaceObject, ClassificationObjects]


"""
A list of attribute ID and corresponding configured KeyLOV (stxt) definition based on dependency configuration set on class attribute.
"""
ConfiguredKeyLOVDefinitionMap = Dict[int, KeyLOVDefinition]


"""
The list of KeyLOV (stxt) id and corresponding KeyLOV (stxt) definition.
"""
KeyLOVDefinitionMap = Dict[str, KeyLOVDefinition]


"""
The list of Classification Class or View ID and corresponding attributes definition.
"""
ClassAttributeDefinitionMap = Dict[str, ClassAttributesDefinition]


"""
A map of classification class Id to a list of its children.
"""
ClassChildrenMap = Dict[str, ClassChildren]
