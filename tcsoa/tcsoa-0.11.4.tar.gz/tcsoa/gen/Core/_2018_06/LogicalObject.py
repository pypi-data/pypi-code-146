from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetLogicalObjectInput2(TcBaseObj):
    """
    Holds the list of the root object instances and the logical type name to retrieve the matched logical object
    instances.
    
    :var rootObjects: A list of root object instances.
    :var loTypeName: Name of the logical object type for which the logical object instances are to be searched for. The
    logical object type name corresponds to the name of any subtype of Fnd0LogicalObject.
    """
    rootObjects: List[RootObject] = ()
    loTypeName: str = ''


@dataclass
class GetLogicalObjectOutput2(TcBaseObj):
    """
    Holds the list of the retrieved logical object instances and related classification objects. Size of
    logicalObjectsOutput is equal to the input rootObjects attribute of input structure GetLogicalObjectInput2.
    
    :var logicalObjectsOutput: A list of the retrieved logical object instances.
    """
    logicalObjectsOutput: List[LogicalObjectOutput2] = ()


@dataclass
class GetLogicalObjectResponse2(TcBaseObj):
    """
    Holds the list of the retrieved logical object along with classification object output response and partial errors.
    
    :var serviceData: Returned service data.
    :var loOutputs: A list of the retrieved logical object output response corresponding to a  logical object input.
    :var classificationObjectInfo: A map (string, classificationObjectInfo) of the ICO Ids and their class attribute
    info.
    """
    serviceData: ServiceData = None
    loOutputs: List[GetLogicalObjectOutput2] = ()
    classificationObjectInfo: ClassificationObjectInfoMap2 = None


@dataclass
class LogicalObjectInstance(TcBaseObj):
    """
    Holds the logical Object instance and its root and member's classification objects.
    
    :var loInstance: An instance of the Fnd0LogicalObject.
    :var memberClassificationObjects: Logical Object instance's root and member name and its classification object
    information.
    """
    loInstance: BusinessObject = None
    memberClassificationObjects: List[MemberClassificationObject2] = ()


@dataclass
class LogicalObjectOutput2(TcBaseObj):
    """
    This structure contains the logical object instance for a given root object given in input structure RootObject.
    
    :var root: An instance of the root Object. This is same object which is provided in input structure RootObject.
    :var logicalObjectInstances: A list of logical object instances. Only one logical object instance is returned for a
    given root object in the current implementation.
    """
    root: BusinessObject = None
    logicalObjectInstances: List[LogicalObjectInstance] = ()


@dataclass
class MemberClassificationObject2(TcBaseObj):
    """
    Contains member or root name and its classification object information.
    
    :var memberOrRootName: The internal name of the member or the root on the Logical Object Type.
    :var icoIDs: A list of ICO UIDs.
    """
    memberOrRootName: str = ''
    icoIDs: List[str] = ()


@dataclass
class AttributeValue2(TcBaseObj):
    """
    Structure for each classification object attribute value.
    
    :var attributeID: ID of the attribute.
    :var attributeName: Name of the attribute.
    :var attributeValues: The values of the attribute.
    :var unit: The unit of the attribute.
    """
    attributeID: int = 0
    attributeName: str = ''
    attributeValues: List[str] = ()
    unit: str = ''


@dataclass
class RootObject(TcBaseObj):
    """
    Holds the root object instance and its client id to retrieve the matched logical object instance.
    
    :var root: A root object instance. Persistent types are the only supported business objects for a root object.
    :var clientID: Client Id for the root object. This helps in uniqely mapping the input and output data.
    """
    root: BusinessObject = None
    clientID: str = ''


@dataclass
class ClassificationObjectInfo(TcBaseObj):
    """
    Structure containing classification object information.
    
    :var icoClassId: The classification class Id.
    :var icoID: The classification object Id.
    :var unitBase: A class unit system of measure.
    :var classifiedObjectUID: Classified WorkspaceObject object UID.
    :var icoAttributeValues: Attribute list of this classification object.
    :var icoClassName: The class name in which the ICO is classified.
    :var icoType: The type of the ICO. Possible values are:
    
    0 - default ICO,
    1 - generic and 
    2 - for a need ICO.
    
    Generic and Need type are added to support Piping and Instrumentation diagram application.
    Compared to default type, the visibility of these objects to the client is controlled by preferences
    (ICS_hidden_ico_types and ICS_support_generic_and_need).
    """
    icoClassId: str = ''
    icoID: str = ''
    unitBase: str = ''
    classifiedObjectUID: str = ''
    icoAttributeValues: List[AttributeValue2] = ()
    icoClassName: str = ''
    icoType: int = 0


"""
Contains classification object uid and its information.

&bull; Primary key : The classification object (ICO) UID uid. 
&bull; Value            : A reference of the structure containing additional ICO properties.
"""
ClassificationObjectInfoMap2 = Dict[str, ClassificationObjectInfo]
