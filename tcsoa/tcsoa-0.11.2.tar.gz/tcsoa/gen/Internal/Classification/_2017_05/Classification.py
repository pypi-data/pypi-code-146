from __future__ import annotations

from tcsoa.gen.Classification._2009_10.Classification import KeyLOVDefinition2, ExtendedProeprty, AttributeConfiguration
from tcsoa.gen.Classification._2007_01.Classification import ClassDef, AttributeFormat
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FormatPropertiesNX(TcBaseObj):
    """
    Structure representing format details
    
    :var format: The format definition for this attribute.
    :var unitDisplayName: Unit display name associated with this attribute in this unit system.
    :var unitID: Unit ID associated with this attribute in this unit system.
    :var nxUnitID: NX Unit ID associated with this attribute in this unit system.
    :var defaultValue: Default value of this Class attribute. This can be an empty string indicating no default value.
    :var minimumValue: Minimum value constraint of this Class attribute. This can be an empty string indicating no
    minimum value constraint.
    Note: Only applicable to numerical formats of attributes
    :var maximumValue: Maximum value constraint of this Class attribute. This can be an empty string indicating no
    maximum value constraint.
    Note: Only applicable to numerical formats of attributes
    """
    format: AttributeFormat = None
    unitDisplayName: str = ''
    unitID: str = ''
    nxUnitID: str = ''
    defaultValue: str = ''
    minimumValue: str = ''
    maximumValue: str = ''


@dataclass
class GetClassDefinitionsResponseNX(TcBaseObj):
    """
    Holds the values returned by getClassDefinitionsNX operation.
    
    :var classDefinitionMap: A map (string, ClassDef) of Classification class or view ID and its corresponding
    definition pairs.
    :var classAttributesMap: A map (string, ClassAttributesDefinitionNX) of Classification class or view ID and its
    corresponding class attributes.
    :var keylovDefintion: A map (string ID, KeyLOVDefinition2) containing the used Classification KeyLOVs and its
    definitions.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    classDefinitionMap: ClassDefinitionsNX = None
    classAttributesMap: ClassAttributesDefinitionMapNX = None
    keylovDefintion: KeylovDefinitionsNX = None
    serviceData: ServiceData = None


@dataclass
class ClassAttributeNX(TcBaseObj):
    """
    Structure representing class attribute details.
    
    :var id: ID for this attribute.
    :var name: Name for this attribute.
    :var dependencyAttribute: The dependency attribute property of this attribute.
    :var dependencyConfiguration: The dependency configuration property of this attribute.
    :var extendedProperties: A list of references to the ExtendedProeprty structure holding the extended metadata
    properties of this attribute.
    :var shortName: Short name defined for this attribute.
    :var description: Description added for this attribute.
    :var metricFormat: The metric format of this attribute.
    :var nonMetricFormat: The nonmetric format of this attribute.
    :var annotation: Annotation information added to this attribute.
    :var attributeConfiguration: Additional configuration for this attribute.
    :var arraySize: Array size or the number of values for this attribute. 
    - If single valued (non-array), then arraySize = 1.
    - If multi valued (array), then arraySize >= 1 corresponding to the size of the array defined in the attribute
    definition.
    
    
    :var options: Attribute property flags represented as a single integer. To access individual property flags, a
    bitwise operation will be required by the client. Valid values are:
    - ATTR_vla = (1 << 0) 
    - ATTR_external_vla = (1 << 1) 
    - ATTR_mandatory = (1 << 2) 
    - ATTR_protected = (1 << 3) 
    - ATTR_unique = (1 << 4) 
    - ATTR_propagated = (1 << 5) 
    - ATTR_localValue = (1 << 6) 
    - ATTR_reference = (1 << 7) 
    - ATTR_auto_computed = (1 << 15) 
    - ATTR_hidden = (1 << 20) 
    - ATTR_localizable = (1 << 22 )
    
    """
    id: int = 0
    name: str = ''
    dependencyAttribute: str = ''
    dependencyConfiguration: str = ''
    extendedProperties: List[ExtendedProeprty] = ()
    shortName: str = ''
    description: str = ''
    metricFormat: FormatPropertiesNX = None
    nonMetricFormat: FormatPropertiesNX = None
    annotation: str = ''
    attributeConfiguration: AttributeConfiguration = None
    arraySize: int = 0
    options: int = 0


@dataclass
class ClassAttributesDefinitionNX(TcBaseObj):
    """
    The structure containing list of Classification class attributes definition and configured KeyLOV (stxt) definition.
    
    :var classAttributes: The list of attributes defined for the classification class.
    :var configuredKeyLOVs: A map (int, KeyLOVDefinition2) of attribute ID and KeyLOV definition pairs, based on
    dependency configuration of an attribute.
    """
    classAttributes: List[ClassAttributeNX] = ()
    configuredKeyLOVs: ConfiguredKeyLOVDefinitionNX = None


"""
The list of KeyLOV (Stxt) id and corresponding KeyLOV (Stxt) definition.
"""
KeylovDefinitionsNX = Dict[str, KeyLOVDefinition2]


"""
The map of Classification Class or View ID and corresponding attributes definition.
"""
ClassAttributesDefinitionMapNX = Dict[str, ClassAttributesDefinitionNX]


"""
The map of Classification Class or View ID and corresponding definition.
"""
ClassDefinitionsNX = Dict[str, ClassDef]


"""
The list of attribute ID and corresponding configured KeyLOV (stxt) definition based on dependency configuration set on class attribute.
"""
ConfiguredKeyLOVDefinitionNX = Dict[int, KeyLOVDefinition2]
