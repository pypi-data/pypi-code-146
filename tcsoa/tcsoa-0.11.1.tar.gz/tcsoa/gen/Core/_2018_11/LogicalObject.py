from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Core._2018_06.LogicalObject import ClassificationObjectInfo, MemberClassificationObject2, RootObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetLogicalObjectInput3(TcBaseObj):
    """
    The structure holds:
    1.    A list of RootObject(s) structures which represents client id and root object instance pair.
    2.    A logical type name. 
    3.    A map containing the included logical object ID, or member ID and configuration context UID. 
    
    Above input data are used to retrieve the matched logical object instances and their configured included logical
    object instances.
    
    :var rootInstances: A list of root instance structures.
    :var loTypeName: Name of the logical object type for which the logical object instances are to be searched for. The
    logical object type name corresponds to the name of any subtype of Fnd0LogicalObject.
    :var loQueryNameValues: A map (string, string) of the Included Logical Object ID, or member ID and its
    Configuration Context UID.
    """
    rootInstances: List[RootObject] = ()
    loTypeName: str = ''
    loQueryNameValues: LOQueryNameValueMap = None


@dataclass
class GetLogicalObjectOutput3(TcBaseObj):
    """
    The structure holds the list of the retrieved logical object instances, related classification objects and included
    logical object instances.
    
    :var logicalObjectsOutput: A list of the retrieved logical object instances. The length of this member is equal to
    the length of the input rootInstances member of the input structure GetLogicalObjectInput3.
    """
    logicalObjectsOutput: List[LogicalObjectOutput3] = ()


@dataclass
class GetLogicalObjectResponse3(TcBaseObj):
    """
    The structure holds the list of the retrieved logical object instances along with classification object output
    response and partial errors.
    
    :var serviceData: Returned service data.
    :var loOutputs: A list of the retrieved logical object output response corresponding to a  logical object input.
    :var classificationObjectInfo: A map(string, ClassificationObjectInfo)  of the ICO IDs and their classification
    object info.
    """
    serviceData: ServiceData = None
    loOutputs: List[GetLogicalObjectOutput3] = ()
    classificationObjectInfo: ClassificationObjectInfoMap3 = None


@dataclass
class LogicalObjectInstance2(TcBaseObj):
    """
    The structure holds the logical object instance, its root, its members and its classification objects. The
    structure also holds the data for included logical object instances.
    
    :var loInstance: An instance of the Logical Object Type.
    :var memberClassificationObjects: A list of structures containing classification object data for the root or member
    of the Logical Object Type.
    :var includedLOInstances: The included Logical Object instances.
    """
    loInstance: BusinessObject = None
    memberClassificationObjects: List[MemberClassificationObject2] = ()
    includedLOInstances: IncludedLOInstanceMap = None


@dataclass
class LogicalObjectOutput3(TcBaseObj):
    """
    The structure contains the logical object instances for a given root object.
    
    :var root: An instance of the root object. This is same object which was provided in input RootObject structure.
    :var logicalObjectInstances: A list of logical object instances. Only one logical object instance is returned for a
    given root object in the current implementation.
    """
    root: BusinessObject = None
    logicalObjectInstances: List[LogicalObjectInstance2] = ()


"""
The map contains the included logical object ID as key and its LogicalObjectInstance2 structures as values.
"""
IncludedLOInstanceMap = Dict[str, List[LogicalObjectInstance2]]


"""
The map contains the included logical object ID, or member ID as key and Configuration Context UID as value.
"""
LOQueryNameValueMap = Dict[str, str]


"""
This structure contains the classification object ID as key and its ClassificationObjectInfo structure as values.
"""
ClassificationObjectInfoMap3 = Dict[str, ClassificationObjectInfo]
