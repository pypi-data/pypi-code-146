from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtendedProperties(TcBaseObj):
    """
    Extended metadata properties for an attribute.
    
    :var propName: An extended prop name.
    :var propValue: Extended prop values.
    """
    propName: str = ''
    propValue: List[str] = ()


@dataclass
class AttrDescriptor(TcBaseObj):
    """
    Structure containing map of class attribute descriptors.
    
    :var attrDescMap: Map of attribute descriptors.
    """
    attrDescMap: AttributeDescriptorMap = None


@dataclass
class AttributeValues(TcBaseObj):
    """
    Contains values for ico attributes and boolean to check whether attribute is valid.
    
    :var isAttrValid: Flag to indicate whethe the attribute is valid
    :var values: List of values for this attribute
    """
    isAttrValid: bool = False
    values: List[Value] = ()


@dataclass
class Value(TcBaseObj):
    """
    structure for each ico attribute value.
    
    :var attrValue: Value of the attribute
    :var unit: Unit of the attribute.
    :var locale: Locale for this attribute.
    """
    attrValue: str = ''
    unit: str = ''
    locale: str = ''


@dataclass
class ClassAttrDescriptor(TcBaseObj):
    """
    Structure representing Class attribute description.
    
    :var id: An attribute id.
    :var name: An attribute name.
    :var metricMinValue: An attribute metric min value.
    :var metricMaxValue: An attribute metric max value.
    :var nonMetricFormat: An attribute non metric format.
    :var nonMetricUnit: An attribute non metric unit.
    :var nonMetricDefaultValue: An attribute non metric default value.
    :var nonMetricMinValue: An attribute non metric min value.
    :var nonMetricMaxValue: An attribute non metric max value.
    :var extendedProps: Extended properties.
    :var shortName: An attribute shortName.
    :var description: An attribute description.
    :var annotation: An attribute annotation.
    :var arraySize: An attribute array size.
    :var options: An attribute options.
    :var metricFormat: An attribute metric format.
    :var metricUnit: An attribute metric unit.
    :var metricDefaultValue: An attribute metric default value.
    """
    id: int = 0
    name: str = ''
    metricMinValue: str = ''
    metricMaxValue: str = ''
    nonMetricFormat: int = 0
    nonMetricUnit: str = ''
    nonMetricDefaultValue: str = ''
    nonMetricMinValue: str = ''
    nonMetricMaxValue: str = ''
    extendedProps: List[ExtendedProperties] = ()
    shortName: str = ''
    description: str = ''
    annotation: str = ''
    arraySize: int = 0
    options: int = 0
    metricFormat: int = 0
    metricUnit: str = ''
    metricDefaultValue: str = ''


@dataclass
class ClassAttrInfo(TcBaseObj):
    """
    Structure containing classification object information.
    
    :var cid: Classification class Id.
    :var attrValuesMap: Class attributes map
    :var unitBase: Class unit system of measure.
    :var icoId: Reference of the classified 'WorkspaceObject' object. This can be a NULLTAG if it is a standalone ICO.
    :var wsoTag: The tag of classifying WSO.
    """
    cid: str = ''
    attrValuesMap: AttributeValuesMap = None
    unitBase: ClassUnitBase = None
    icoId: str = ''
    wsoTag: BusinessObject = None


@dataclass
class ClassificationInfoResponse(TcBaseObj):
    """
    Contains classification objects info returned by getClassificationObjectInfo() method.
    
    :var classificationObjectInfo: Map of classification objects and list of references to their class attributes.
    :var classAttributeDesc: Map of classification objects and list of references to their attribute descriptors.
    :var svcData: Any failures with classification object ID mapped to the error message in the 'ServiceData' list of
    partial errors.
    """
    classificationObjectInfo: ClassificationObjectInfoMap = None
    classAttributeDesc: ClassAttributeDescMap = None
    svcData: ServiceData = None


class ClassUnitBase(Enum):
    """
    Enumerates the list of value for class unit system.
    """
    CLS_METRIC = 'CLS_METRIC'
    CLS_NONMETRIC = 'CLS_NONMETRIC'
    CLS_BOTH = 'CLS_BOTH'


"""
Contains descriptor of an attribute.
"""
AttributeDescriptorMap = Dict[int, ClassAttrDescriptor]


"""
Contains attriute Id and corresponding value(s).

Structure elements:

- primary key - Attribute ID.
- values - Value structure for this attribute.


"""
AttributeValuesMap = Dict[int, AttributeValues]


"""
Contains class Id and corresponding attribute descriptor.
"""
ClassAttributeDescMap = Dict[str, AttrDescriptor]


"""
Contains classification object information.

Structure elements:

- primary key - Classification object (ICO) ID.
- values - Reference of the structure containing additional ICO properties


"""
ClassificationObjectInfoMap = Dict[str, ClassAttrInfo]
