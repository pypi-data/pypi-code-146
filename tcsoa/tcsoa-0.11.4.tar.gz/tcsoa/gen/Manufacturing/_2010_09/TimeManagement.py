from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetActivityTimesResponse(TcBaseObj):
    """
    The response structure of the getActivityTimes operation.
    
    :var results: A vector of GetActivityTimesResult structures that holds for each root node the list of activity
    times indexed by category.
    :var serviceData: This is a common data structure that is used to return Teamcenter model data from a service
    request. This member also holds service exceptions.
    """
    results: List[GetActivityTimesResult] = ()
    serviceData: ServiceData = None


@dataclass
class GetActivityTimesResult(TcBaseObj):
    """
    A structure that contains for a specific root node passed to the getActivityTimes operation the map of accumulated
    activity times per category.
    
    :var rootNode: The root of the process or operation tree for which the activity times have been calculated.
    :var timePerCategoryMap: Contains the computed activity time for each category.
    """
    rootNode: BusinessObject = None
    timePerCategoryMap: ActivityTimePerCategoryMap = None


@dataclass
class CalculateCriticalPathResponseEx(TcBaseObj):
    """
    The response structure for the calculateCriticalPathEx operation. If it is not possible to compute the critical
    path for a specific root object, no entry will be added  to the results vector. Instead the serviceData member will
    contain an description of the failure cause.
    
    :var results: A list of CalculateCriticalPathResultEx structures for each path returned.
    :var serviceData: Contains a list of error descriptions if the path computation has failed.
    """
    results: List[CalculateCriticalPathResultEx] = ()
    serviceData: ServiceData = None


@dataclass
class CalculateCriticalPathResultEx(TcBaseObj):
    """
    A structure that represents a path returned by the computeCriticalPathEx operation.
    
    :var object: the root object for which this path was computed
    :var components: A list of components that make up the path. This includes also the connecting flows.
    :var duration: The total length of the path.
    """
    object: BusinessObject = None
    components: List[BusinessObject] = ()
    duration: float = 0.0


"""
A map that contains activity time values for different activity categories.
"""
ActivityTimePerCategoryMap = Dict[str, float]
