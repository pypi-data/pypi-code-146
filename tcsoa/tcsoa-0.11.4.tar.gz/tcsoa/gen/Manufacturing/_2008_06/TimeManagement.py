from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AllocatedTime(TcBaseObj):
    """
    Allocated Time structure for allocatedTimeRollUp operation
    
    :var roots: vector of Tags of the item element
    :var calculatedBy: The type of calculation for the allocated time algorythm.possible values:
    duration_time,simulated_time,estimated_time,best_available_time.
    """
    roots: List[BusinessObject] = ()
    calculatedBy: str = ''


@dataclass
class AllocatedTimeResponse(TcBaseObj):
    """
    Return structure for allocatedTimeRollUp operation
    
    :var results: MAp of each root and its allocated time result.
    :var serviceData: This is a common data strucuture used to return sets of
    Teamcenter Data Model object from a service request. This also
    holds services exceptions.
    """
    results: MapAllocatedTimeResults = None
    serviceData: ServiceData = None


@dataclass
class TimeAnalysisInputs(TcBaseObj):
    """
    Time Analysis Inputs structure for timeAnalysisRollup operation
    
    :var roots: vector of Tags of the item element
    :var runTimePropertiesToRecalc: The additional run time  properties need to be calculated for the time analysis
    such as total time and duration time
    """
    roots: List[BusinessObject] = ()
    runTimePropertiesToRecalc: List[str] = ()


@dataclass
class TimeAnalysisResult(TcBaseObj):
    """
    Time Analysis Results structure for timeAnalysisRollup operation
    
    :var object: the item element for the rollup.
    :var categoryResults: a map results of the activity total time for each category.
    :var mapRunTimeResult: a map results of the requested run time properties.
    """
    object: BusinessObject = None
    categoryResults: MapStringDouble = None
    mapRunTimeResult: MapStringDouble = None


@dataclass
class TimeAnalysisRollupResponse(TcBaseObj):
    """
    Return structure for timeAnalysisRollup operation
    
    :var results: vector of the TimeAnalysisResult.
    :var serviceData: This is a common data strucuture used to return sets of
    Teamcenter Data Model object from a service request. This also
    holds services exceptions.
    """
    results: List[TimeAnalysisResult] = ()
    serviceData: ServiceData = None


"""
MapAllocatedTimeResults
"""
MapAllocatedTimeResults = Dict[BusinessObject, float]


"""
MapStringDouble
"""
MapStringDouble = Dict[str, float]
