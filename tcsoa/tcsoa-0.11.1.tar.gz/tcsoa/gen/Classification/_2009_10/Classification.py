from __future__ import annotations

from tcsoa.gen.Classification._2007_01.Classification import ClassificationPropertyValue, AttributeFormat
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtendedProeprty(TcBaseObj):
    """
    This Structure represents extended metadata property.
    
    :var propertyName: Name of the extended metadata property associated to the given attribute.
    :var values: List of references to the 'ExtendedPropertyValues' structure holding actual values of the Extended
    metadata properties.
    """
    propertyName: str = ''
    values: List[ExtendedPropertyValues] = ()


@dataclass
class ExtendedPropertyValues(TcBaseObj):
    """
    This structure is used to hold extended metadata property values
    
    :var value: Values of the Extended metadata property associated to a Classification Attribute.
    """
    value: str = ''


@dataclass
class FormatProperties(TcBaseObj):
    """
    Structure representing format details
    
    :var format: References the 'AttributeFormat' structure holding the format definition for this attribute.
    :var unitName: Unit display name associated with this attribute in this unit system.
    :var defaultValue: Default value of this Class attribute. This can be an empty string indicating no default value.
    :var minimumValue: Minimum value constraint of this Class attribute. This can be an empty string indicating no
    minimum value constraint.
    Note: Only applicable to numerical formats of attributes
    :var maximumValue: Maximum value contraint of this Class attribute. This can be an empty string indicating no
    maximum value constraint.
    Note: Only applicable to numerical formats of attributes
    """
    format: AttributeFormat = None
    unitName: str = ''
    defaultValue: str = ''
    minimumValue: str = ''
    maximumValue: str = ''


@dataclass
class GetAttributesForClassesResponse2(TcBaseObj):
    """
    Holds the values returned by 'getAttributesForClass2()'
    
    :var attributes: Map of Class IDs and the Class attributes found for each of those classes.
    :var data: Any failure will be returned with Class ID mapped to the error message in the ServiceData list of
    partial errors.
    """
    attributes: StrVClsAttrMap2 = None
    data: ServiceData = None


@dataclass
class GetKeyLOVsResponse2(TcBaseObj):
    """
    Holds the keylovs returned by the' ''getKeyLOVs2()' method.
    
    :var keyLOVs: Map of KeyLOV definitions details.
    :var data: Any failure will be returned with Key-LOV ID mapped to the error message in the 'ServiceData' list of
    partial errors
    """
    keyLOVs: StrKeyLOVDefMap2 = None
    data: ServiceData = None


@dataclass
class KeyLOVDefinition2(TcBaseObj):
    """
    Structure representing KeyLOVDefinition
    
    :var id: Unique Key-LOV ID. This is a negative number.This can be found in the Key/ID field of a Key-LOV definition
    in the Key-LOV tab of Classification Administration.
    :var name: Name of the Key-LOV.
    :var keyLovtag: Unused parameter. Reserved for future use
    :var options: Key-LOV options to Show/Hide keys.Valid values are: 
    - 0 = Show key
    - 1 = Hide key
    
    
    :var keyLovEntries: List of Key-LOV entries.
    :var owningSite: Owning Site (POM_imc).
    :var sharedSites: List of sites (POM_imc) where this Key-LOV is to be shared using Multisite operations.
    """
    id: str = ''
    name: str = ''
    keyLovtag: BusinessObject = None
    options: int = 0
    keyLovEntries: List[KeyLOVEntry] = ()
    owningSite: BusinessObject = None
    sharedSites: List[BusinessObject] = ()


@dataclass
class KeyLOVEntry(TcBaseObj):
    """
    Structure representing KeyLOVEntry
    
    :var lovKey: String representing a Key of a Key-LOV entry.
    :var lovValue: String representing a Value  of the Key-LOV  entry.
    :var deprecatedSatus: Flag indicating whether this particular Key-LOV entry is deprecated or not.
    """
    lovKey: str = ''
    lovValue: str = ''
    deprecatedSatus: bool = False


@dataclass
class AttributeConfiguration(TcBaseObj):
    """
    Holds the configuration attached to an attibute
    
    :var preConfig: Preconfiguration attached to the attribute
    :var config: Base configuration attached to the attribute.
    :var postConfig: Post configuration attached to the attribute.Configurations could be any combinations of the
    following individual configurations:
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
    
    """
    preConfig: str = ''
    config: str = ''
    postConfig: str = ''


@dataclass
class AutoComputeAttribute(TcBaseObj):
    """
    Contains the attributes that are used for the auto compute operation.
    
    :var values: List of references to the 'ClassificationPropertyValue' structures that will hold the values (single
    or multiple values) for the Attribute represented by this 'AutoComputeAttribute'.
    :var unitName: Display unit name for this attribute.
    :var length: Length of an Attribute. This field will hold the number of values for this Attribute. 
    - For a single valued attribute, length = 1
    - For an array type of attribute, length = n [where n is the size of the array.]
    
    
    :var attributeProperties: Represents the Attribute property flags concatenated into a single Integer value.
    To access  individual flag, a bitwise operation will need to be performed by the Client.
    Valid values are as specified in the 'enum AutoComputeAttrPropertyFlags'.
    :var isModified: Flag to indicate whether the attribute referenced by this 'AutoComputerAttribute' structure is
    modified by the client. It is only used when 'AutoComputeAttribute' structure is used as an Input parameter to the
    'autoComputeAttributes' operation. This parameter is should not be used by clients when reading the
    'AutoComputeAttribute' structure as part of the  returned 'AutoComputeAttributesResponse'.
    """
    values: List[ClassificationPropertyValue] = ()
    unitName: str = ''
    length: int = 0
    attributeProperties: int = 0
    isModified: bool = False


@dataclass
class AutoComputeAttributesResponse(TcBaseObj):
    """
    Contains the attribute values for the corresponding autocomputed attributes after the autocompute operation is
    called. The structure element is a key,value pair of attribute IDs and their corresponding attribute properties.
    The attribute properties of type AutoComputeAttribute  contains the following information:
    - values : This structure element of type ClassificationPropertyValue holds the classification properties for the
    classification object
    - length : the number of attributes computed
    - unitName : the unit of measure for the attribute
    - attributeProperties : Properties of the attributes
    - isModified : Boolean value to check if attribute is modified
    
    
    
    :var autoComputedAttrs: Map containing references of the 'AutoComputeAttribute' structures with their respective
    attribute IDs.
    :var serviceData: Any failures with classification object ID mapped to the error message in the ServiceData list of
    partial errors.
    """
    autoComputedAttrs: AutoComputeAttributesMap = None
    serviceData: ServiceData = None


@dataclass
class ClassAttribute2(TcBaseObj):
    """
    Structure representing class attribute details.
    
    :var id: ID for this attribute.
    :var name: Name for this attribute.
    :var extendedProperties: List of references to the ExtendedProeprty structure holding the extended metadata
    properties of this attribute.
    :var shortName: Short name defined for this attribute.
    :var description: Description added for this attribute.
    :var metricFormat: References the 'FormatProperties' structure defining the metric format of this attribute.
    :var nonMetricFormat: References the 'FormatProperties' structure defining the nonmetric format of this attribute.
    :var annotation: Annotation information added to this attribute.
    :var attributeConfiguration: Reference the 'AttributeConfiguration' structure that defines any additional
    configuration for this attribute.
    :var arraySize: Array size or the number of values for this attribute.
    - If single valued (nonarray), then 'arraySize' = 1
    - If multi valued (array), then 'arraySize' >= 1 corresponding to the size of the array defined in the attribute
    definition.
    
    
    :var options: Attribute property flags represented as a single integer. To access individual property flags, a
    bitwise operation will be required by the client.Valid values are:
    - ATTR_vla                      = (1 << 0)
    - ATTR_external_vla      = (1 << 1)
    - ATTR_mandatory         = (1 << 2)
    - ATTR_protected             = (1 << 3)
    - ATTR_unique                 = (1 << 4)
    - ATTR_propagated         = (1 << 5)
    - ATTR_localValue             = (1 << 6)
    - ATTR_reference             = (1 << 7)
    - ATTR_auto_computed = (1 << 15)
    - ATTR_hidden                 = (1 << 20)
    - ATTR_localizable         = (1 
    
    """
    id: int = 0
    name: str = ''
    extendedProperties: List[ExtendedProeprty] = ()
    shortName: str = ''
    description: str = ''
    metricFormat: FormatProperties = None
    nonMetricFormat: FormatProperties = None
    annotation: str = ''
    attributeConfiguration: AttributeConfiguration = None
    arraySize: int = 0
    options: int = 0


"""
Structure elements:

- Primary key - Integer Attribute IDs for attributes. This will be provided as an input. 
- Values - References an AutoComputeAttribute structure  for the corresponding attribute ID in the primary key of this map.


"""
AutoComputeAttributesMap = Dict[int, AutoComputeAttribute]


"""
Map to store Key-LOV definitions details.Any failure will be returned with the Key-LOV ID mapped to the error message in the 'ServiceData' list of partial errors.
"""
StrKeyLOVDefMap2 = Dict[str, KeyLOVDefinition2]


"""
StrVClsAttrMap2
"""
StrVClsAttrMap2 = Dict[str, List[ClassAttribute2]]
