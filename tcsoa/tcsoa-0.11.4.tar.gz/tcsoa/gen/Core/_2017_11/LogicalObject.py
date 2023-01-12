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
    
    :var propertyName: An extended property name.
    :var propertyValue: The extended property values.
    """
    propertyName: str = ''
    propertyValue: List[str] = ()


@dataclass
class GetLogicalObjectInput(TcBaseObj):
    """
    Holds the list of the root object instances and the logical type name to retrieve the matched logical object
    instances.
    
    :var rootObjects: A list of root object instances. Persistent types are the only supported business objects for a
    root object.
    :var loTypeName: Name of the logical object type for which the logical object instances are to be searched for. The
    logical object type name corresponds to the name of any subtype of Fnd0LogicalObject.
    """
    rootObjects: List[BusinessObject] = ()
    loTypeName: str = ''


@dataclass
class GetLogicalObjectOutput(TcBaseObj):
    """
    Holds the list of the retrieved logical object instances.
    
    :var logicalObjects: A list of the retrieved logical object instances.
    """
    logicalObjects: List[LogicalObjectOutput] = ()


@dataclass
class GetLogicalObjectResponse(TcBaseObj):
    """
    Holds the list of the retrieved logical object output response and partial errors.
    
    :var serviceData: Returned service data.
    :var loOutputs: A list of the retrieved logical object output response corresponding to a  logical object input.
    :var classificationAttributeDesc: A map of classification objects and a list of references to their attribute
    descriptors.
    :var classificationObjectInfo: A map of the ICO ids and their class attribute info.
    """
    serviceData: ServiceData = None
    loOutputs: List[GetLogicalObjectOutput] = ()
    classificationAttributeDesc: ClassificationAttributeDescMap = None
    classificationObjectInfo: ClassificationObjectInfoMap = None


@dataclass
class AttrDescriptor(TcBaseObj):
    """
    Structure containing map of class attribute descriptors.
    
    :var attributeDescMap: The map of the attribute descriptors.
    """
    attributeDescMap: AttributeDescriptorMap = None


@dataclass
class LogicalObjectOutput(TcBaseObj):
    """
    This structure contains the logical object instance and its related classification objects information.
    
    :var root: An instance of the root object.
    :var logicalObjectInstances: A list of logical object instances. Only one logical object instance is returned for a
    given root object in the current implementation.
    :var memberClassificationObjects: A list of  MemberClassificationObject objects.
    """
    root: BusinessObject = None
    logicalObjectInstances: List[BusinessObject] = ()
    memberClassificationObjects: List[MemberClassificationObject] = ()


@dataclass
class MemberClassificationObject(TcBaseObj):
    """
    Contains classification object information.
    
    :var memberOrRootName: The internal name of the member or the root.
    :var icoIDs: A list of ICO ids.
    """
    memberOrRootName: str = ''
    icoIDs: List[str] = ()


@dataclass
class AttributeValue(TcBaseObj):
    """
    Structure for each ICO attribute value.
    
    :var attrValue: The value of the attribute.
    :var unit: The unit of the attribute.
    :var locale: The locale for this attribute.
    """
    attrValue: str = ''
    unit: str = ''
    locale: str = ''


@dataclass
class AttributeValues(TcBaseObj):
    """
    Contains values for ICO attributes and a boolean to check whether attribute is valid.
    
    :var isAttributeValid: A flag to indicate whether the attribute is valid.
    :var values: A list of values for this attribute.
    """
    isAttributeValid: bool = False
    values: List[AttributeValue] = ()


@dataclass
class ClassAttrDescriptor(TcBaseObj):
    """
    Structure representing Class attribute description.
    
    :var id: An attribute id.
    :var name: An attribute name.
    :var metricMinValue: An attribute metric min value.
    :var metricMaxValue: An attribute metric max value.
    :var nonMetricFormat: An attribute non metric format.
    :var nonMetricUnit: An attribute non metric format.
    :var nonMetricDefaultValue: An attribute non metric default value.
    :var nonMetricMinValue: An attribute non metric min value.
    :var nonMetricMaxValue: An attribute non metric max value.
    :var extendedProps: The extended properties.
    :var shortName: An attribute short name.
    :var descripton: An attribute description.
    :var annotation: An attribute annotation.
    :var arraySize: An attribute array size.
    :var options: An attribute options.
    :var metricFormat: An attribute metric format.
    :var metricUnit: An attribute metric unit.
    :var metricDefaultValue: An attribute metric default value.
    """
    id: str = ''
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
    descripton: str = ''
    annotation: str = ''
    arraySize: int = 0
    options: int = 0
    metricFormat: int = 0
    metricUnit: str = ''
    metricDefaultValue: str = ''


@dataclass
class ClassAttributeInfo(TcBaseObj):
    """
    Structure containing classification object information.
    
    :var classId: The classification class Id.
    :var attributeValuesMap: The class attributes map.
    :var unitBase: A class unit system of measure.
    :var classifiedObject: Reference of the classified WorkspaceObject object. This can be a NULLTAG if it is a
    standalone ICO.
    """
    classId: str = ''
    attributeValuesMap: AttributeValuesMap = None
    unitBase: ClassUnitBase = None
    classifiedObject: BusinessObject = None


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
AttributeDescriptorMap = Dict[str, ClassAttrDescriptor]


"""
Contains attribute Id and corresponding value(s).

&bull;primary key :  The attribute ID. 
&bull;values :            A value structure for this attribute.
"""
AttributeValuesMap = Dict[str, AttributeValues]


"""
Contains class Id and corresponding attribute descriptor.
"""
ClassificationAttributeDescMap = Dict[str, AttrDescriptor]


"""
Contains classification object information.

&bull;primary key:  The classification object (ICO) ID. 
&bull;values:            A reference of the structure containing additional ICO properties.
"""
ClassificationObjectInfoMap = Dict[str, ClassAttributeInfo]
