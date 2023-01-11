from __future__ import annotations

from tcsoa.gen.Classification._2009_10.Classification import ClassAttribute2, KeyLOVDefinition2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Classification._2007_01.Classification import ClassDef
from typing import Dict


@dataclass
class GetClassDefinitionsResponse(TcBaseObj):
    """
    Holds the values returned by getClassDefinitions operation.
    
    :var classDefinitionMap: A map of Classification class or view ID and its corresponding definition pairs
    (string/ClassDef).
    :var classAttributesDefinitionMap: A map of Classification class or view ID and its definition pairs
    (string/ClassAttributesDefinition).
    :var keyLOVDefinitionMap: A map containing the used Classification KeyLOVs and its definitions (string
    ID/KeyLOVDefinition2).
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    classDefinitionMap: ClassDefinitionMap = None
    classAttributesDefinitionMap: ClassAttributesDefinitionMap = None
    keyLOVDefinitionMap: KeyLOVDefinitionMap = None
    serviceData: ServiceData = None


@dataclass
class ClassAttribute3(TcBaseObj):
    """
    The structure representing class attributes.
    
    :var classAttributeProperty: A structure representing Class attribute details.
    :var dependencyAttribute: The dependency attribute property of this attribute.
    :var dependencyConfiguration: The dependency configuration property of this attribute.
    """
    classAttributeProperty: ClassAttribute2 = None
    dependencyAttribute: str = ''
    dependencyConfiguration: str = ''


@dataclass
class ClassAttributesDefinition(TcBaseObj):
    """
    The structure containing list of Classification class attributes definition and configured KeyLOV (Stxt) definition.
    
    :var attributeDefinitionMap: A map of attribute ID and attribute definition pairs (int/ClassAttribute3).
    :var configuredKeyLOVDefinitionMap: A map of attribute ID and KeyLOV definition pairs (int/KeyLOVDefinition2),
    based on dependency configuration of an attribute.
    """
    attributeDefinitionMap: AttributeDefinitionMap = None
    configuredKeyLOVDefinitionMap: ConfiguredKeyLOVDefinitionMap = None


"""
The list of Classification attributes ID and attributes property descriptor.
"""
AttributeDefinitionMap = Dict[int, ClassAttribute3]


"""
The list of KeyLOV (Stxt) id and corresponding KeyLOV (Stxt) definition.
"""
KeyLOVDefinitionMap = Dict[str, KeyLOVDefinition2]


"""
The list of Classification Class or View ID and corresponding attributes definition.
"""
ClassAttributesDefinitionMap = Dict[str, ClassAttributesDefinition]


"""
The list of Classification Class or View ID and corresponding definition.
"""
ClassDefinitionMap = Dict[str, ClassDef]


"""
The list of attribute ID and corresponding configured KeyLOV (Stxt) definition based on dependency configuration set on class attribute.
"""
ConfiguredKeyLOVDefinitionMap = Dict[int, KeyLOVDefinition2]
