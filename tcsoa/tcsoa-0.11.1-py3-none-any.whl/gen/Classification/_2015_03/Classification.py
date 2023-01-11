from __future__ import annotations

from tcsoa.gen.Classification._2009_10.Classification import KeyLOVDefinition2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDependencyKeyLOVsResponse(TcBaseObj):
    """
    Holds the values returned by getKeyLOVsForDependentAttributes operation.
    
    :var dependencyKeyLOVs: A list containing attribute ID, key of to be selected entry from a KeyLOV and its KeyLOV
    definition for each to be changed attribute.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    dependencyKeyLOVs: List[DependencyKeyLOVDescriptor] = ()
    serviceData: ServiceData = None


@dataclass
class DependencyAttributeStruct(TcBaseObj):
    """
    The structure containing class ID, the changed attribute ID, its value and all other UI attribute IDs and
    corresponding values.
    
    :var classID: The unique ID of Classification class.
    :var selectedAttributeID: The unique ID of an attribute (from above class) whose UI value is changed.
    :var selectedValue: The user selected value of the attribute (key of the selected entry from the KeyLOV). This
    could be empty if the value has been deselected.
    :var attributeValues: A list of DependencyAttributeValue objects containing attribute IDs and their corresponding
    values for all other UI attributes from above class.
    """
    classID: str = ''
    selectedAttributeID: int = 0
    selectedValue: str = ''
    attributeValues: List[DependencyAttributeValue] = ()


@dataclass
class DependencyAttributeValue(TcBaseObj):
    """
    Structure containing the attribute ID and corresponding value. 
    
    :var attributeID: Unique ID of an attribute.
    :var value: The UI value for above attribute (the key of a KeyLOV entry in case of KeyLOV attribute).
    """
    attributeID: int = 0
    value: str = ''


@dataclass
class DependencyKeyLOVDescriptor(TcBaseObj):
    """
    Structure representing dependent attribute IDs and corresponding key-value pairs. 
    
    :var attributeID: The unique ID of the changed attribute.
    :var selectedKeys: A list of unique key of to be selected entry for this attribute (can be empty).
    :var keyLOVDefinition: The structure representing the configured KeyLOV definition for attribute.
    """
    attributeID: int = 0
    selectedKeys: List[str] = ()
    keyLOVDefinition: KeyLOVDefinition2 = None
