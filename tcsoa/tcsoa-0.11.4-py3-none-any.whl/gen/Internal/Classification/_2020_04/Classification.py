from __future__ import annotations

from tcsoa.gen.Classification._2009_10.Classification import KeyLOVDefinition2, AttributeConfiguration
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Classification._2007_01.Classification import ClassificationProperty, TypedDocument
from enum import Enum
from tcsoa.gen.Internal.Classification._2017_05.Classification import FormatPropertiesNX
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtendedPropertyInfo(TcBaseObj):
    """
    Extended metadata properties for an attribute.
    
    :var propName: An extended property name.
    :var propValue: Extended property values.
    """
    propName: str = ''
    propValue: List[str] = ()


@dataclass
class FindClassificationInfoRequest(TcBaseObj):
    """
    Input for FindClassificationInfo operation.
    
    :var workspaceObjects: List of input WorkspaceObjects for which classification information is required.
    :var relationTypes: GRM relation types used to get classification object information.
    Possible values are -
    &bull;IMAN_classification
    &bull;Fnd0SourceClassification
    """
    workspaceObjects: List[BusinessObject] = ()
    relationTypes: List[str] = ()


@dataclass
class FindClassificationInfoResponse(TcBaseObj):
    """
    Holds the classification objects returned by the findClassificationInfo operation.
    
    :var classificationObjectsInfoMap: Map (BusinessObject, std::vector< ClassificationObjectInformation >) of
    WorkspaceObject to corresponding Classification Object details.
    :var classInfoMap: A map (string, ClassInformation) of Classification class or view ID and its corresponding
    definition.
    :var keylovInfoMap: A map (string ID, KeyLOVDefinition2) containing the used Classification KeyLOVs (stxt) and its
    definitions.
    :var serviceData: Any failures will be returned in the service data list of partial errors.
    """
    classificationObjectsInfoMap: ClassificationObjectsInfoMap = None
    classInfoMap: ClassInfoMap = None
    keylovInfoMap: KeylovInfoMap = None
    serviceData: ServiceData = None


@dataclass
class ClassAttributeInfo(TcBaseObj):
    """
    Structure representing class attribute details.
    
    :var id: Unique ID for this attribute.
    :var name: Display name of the attribute.
    :var dependencyAttribute: The dependency attribute property of this attribute.
    :var dependencyConfiguration: The dependency configuration property of this attribute.
    :var extendedProperties: A list of references to the ExtendedProperty structure holding the extended metadata
    properties of this attribute.
    :var configuredKeyLOV: KeyLOV (stxt) information based on dependency configuration of an attribute.
    :var shortName: Short name defined for this attribute.
    :var description: Description added for this attribute.
    :var metricFormat: The metric format of this attribute.
    :var nonMetricFormat: The nonmetric format of this attribute.
    :var annotation: Annotation information added to this attribute.
    :var attributeConfiguration: Additional configuration for this attribute.
    :var arraySize: Array size or the number of values for this attribute. 
    &bull;    If single valued (non-array), then arraySize = 1.
    &bull;    If multi valued (array), then arraySize >= 1 corresponding to the size of the array defined in the
    attribute definition.
    :var options: Attribute property flags represented as a single integer. To access individual property flags, a
    bitwise operation will be required by the client. Valid values are:
    &bull;     vla = 1 
    &bull;     external_vla = 2
    &bull;     mandatory = 4 
    &bull;     protected = 8 
    &bull;     unique = 16 
    &bull;     propagated = 32 
    &bull;     localValue = 64 
    &bull;     reference = 128 
    &bull;     auto_computed = 32768 
    &bull;     hidden = 32768 
    &bull;     localizable = 4194304
    """
    id: int = 0
    name: str = ''
    dependencyAttribute: str = ''
    dependencyConfiguration: str = ''
    extendedProperties: List[ExtendedPropertyInfo] = ()
    configuredKeyLOV: KeyLOVDefinition2 = None
    shortName: str = ''
    description: str = ''
    metricFormat: FormatPropertiesNX = None
    nonMetricFormat: FormatPropertiesNX = None
    annotation: str = ''
    attributeConfiguration: AttributeConfiguration = None
    arraySize: int = 0
    options: int = 0


@dataclass
class ClassInformation(TcBaseObj):
    """
    Properties of the given class.
    
    :var id: Unique ID of the class.
    :var parent: Class ID of the parent class.
    :var userData2: User data 2 added to this class.
    :var documents: List of attached Icons, Images and NamedRefs to this class.
    :var classAttributesInfo: Class attributes information.
    :var name: Display name of the class.
    :var shortName: Short name
    :var description: Class description
    :var unitSystem: Unit system of the class. See enum ClassUnitSystem for list of valid values.
    :var isAbstract: True value indicates that the class is abstract class, else storage class.
    :var isGroup: True value indicates that the class is a group.
    :var isAssembly: True value indicates that the class is an assembly.
    :var userData1: User data 2 added to this class.
    """
    id: str = ''
    parent: str = ''
    userData2: str = ''
    documents: List[TypedDocument] = ()
    classAttributesInfo: List[ClassAttributeInfo] = ()
    name: str = ''
    shortName: str = ''
    description: str = ''
    unitSystem: ClassUnitSystem = None
    isAbstract: bool = False
    isGroup: bool = False
    isAssembly: bool = False
    userData1: str = ''


@dataclass
class ClassificationObjectInformation(TcBaseObj):
    """
    Structure representing Classification Object details.
    
    :var clsObject: Reference of Classification object.
    :var clsObjId: Unique ID of the Classification object.
    :var classId: Unique ID of the Classification class where this object was created.
    :var unit: Unit system of measure in which the Classification object is stored in.
    :var properties: Array of Classification attributes references that store the properties of this Classification
    object.
    :var relations: References to list of relations.
    """
    clsObject: BusinessObject = None
    clsObjId: str = ''
    classId: str = ''
    unit: UnitSystemType = None
    properties: List[ClassificationProperty] = ()
    relations: List[BusinessObject] = ()


class ClassUnitSystem(Enum):
    """
    &bull;    METRIC_SYSTEM - Metric unit system of measure.
    &bull;    NON_METRIC_SYSTEM  - Non-metric unit system of measure. 
    &bull;    BOTH &ndash; Class supports both unit system.
    """
    METRIC_SYSTEM = 'METRIC_SYSTEM'
    NON_METRIC_SYSTEM = 'NON_METRIC_SYSTEM'
    BOTH = 'BOTH'


class UnitSystemType(Enum):
    """
    UNSPECIFIED_TYPE: No unit system of measure.
    METRIC_TYPE: Metric unit system of measure.
    NON_METRIC_TYPE: Non-metric unit system of measure.
    """
    UNSPECIFIED_TYPE = 'UNSPECIFIED_TYPE'
    METRIC_TYPE = 'METRIC_TYPE'
    NON_METRIC_TYPE = 'NON_METRIC_TYPE'


"""
The list of KeyLOV id and corresponding KeyLOV definition.
"""
KeylovInfoMap = Dict[str, KeyLOVDefinition2]


"""
The map of Classification Class or View ID and corresponding definition.
"""
ClassInfoMap = Dict[str, ClassInformation]


"""
Map of Workspace Object to the details of Classification Object.

&bull;Key - Workspace Object
&bull;Value - ClassificationObject structure representing Classification Object details.
"""
ClassificationObjectsInfoMap = Dict[BusinessObject, List[ClassificationObjectInformation]]
