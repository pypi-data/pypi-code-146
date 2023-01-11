from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FlowInput(TcBaseObj):
    """
    FlowInput
    
    :var successor: The successor object of the flow object
    :var predecessor: The predecessor object of the flow.
    :var delay: The delay time for the successor.
    """
    successor: BusinessObject = None
    predecessor: BusinessObject = None
    delay: float = 0.0


@dataclass
class FlowResponse(TcBaseObj):
    """
    FlowResponse
    
    :var flowsResult: A vector of the new succesfully created flow objects.
    :var serviceData: serviceData
    """
    flowsResult: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class GetResolvedNodesFromLAResponse(TcBaseObj):
    """
    Response for getResolvedNodesFromLA SOA
    
    :var outResolvedNodes: All the resolved nodes of all objects
    :var serviceData: Service data object
    """
    outResolvedNodes: List[ResolvedNodesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class LogicalAssignmentAttribute(TcBaseObj):
    """
    Attribute representation
    
    :var name: Attribute name
    :var value: Attribute value
    """
    name: str = ''
    value: str = ''


@dataclass
class LogicalAssignmentData(TcBaseObj):
    """
    Parameters for editing Logical Assignment object
    
    :var laObj: Logical Assignment object to edit
    :var laAttributes: Attributes to set to the object
    """
    laObj: BusinessObject = None
    laAttributes: List[LogicalAssignmentAttribute] = ()


@dataclass
class LogicalAssignmentResolvedNodes(TcBaseObj):
    """
    Holds resolved nodes of each LA
    
    :var laObj: LA object
    :var resolvedNodes: Resolved nodes of LA object
    """
    laObj: BusinessObject = None
    resolvedNodes: List[BusinessObject] = ()


@dataclass
class ResolveData(TcBaseObj):
    """
    Data for object to resolve
    
    :var object: object to resolve
    :var laResolveType: what type of LAs to resolve (class name)
    :var recursive: if this flag is true, resolve all LAs of the above type of this object, all operations and
    processes under this object, all operations and processes under child processes and so on
    """
    object: BusinessObject = None
    laResolveType: str = ''
    recursive: bool = False


@dataclass
class ResolvedNodesInput(TcBaseObj):
    """
    Input for getResolvedNodesFromLA SOA
    
    :var parentObject: parent operation/process
    :var laObjects: vector of LA objects of this op/proc, for which we want resolved nodes
    """
    parentObject: BusinessObject = None
    laObjects: List[BusinessObject] = ()


@dataclass
class ResolvedNodesOutput(TcBaseObj):
    """
    Holds resolved nodes of the whole parent object
    
    :var parentObject: Parent object
    :var laResolvedNodes: Resolved nodes of all LA objects
    """
    parentObject: BusinessObject = None
    laResolvedNodes: List[LogicalAssignmentResolvedNodes] = ()


@dataclass
class CalculateCriticalPathResponse(TcBaseObj):
    """
    The response structure for the calculateCriticalPath operation.
    
    :var results: A list of CalculateCriticalPathResult structures for each path returned.
    :var serviceData: This is a common data strucuture used to return sets of
    Teamcenter Data Model object from a service request. This also holds services exceptions.
    """
    results: List[CalculateCriticalPathResult] = ()
    serviceData: ServiceData = None


@dataclass
class CalculateCriticalPathResult(TcBaseObj):
    """
    A structure that represents a path returned by the computeCriticalPath operation
    
    :var object: The root object for which this path was computed
    :var components: A list of components that make up the path. This includes the connecting flows.
    :var duration: The total duration of the path.
    """
    object: BusinessObject = None
    components: List[BusinessObject] = ()
    duration: float = 0.0
