from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FeatureAssignmentStruct(TcBaseObj):
    """
    This is a structure of manufacturing feature objects, its corresponding occurrence chain, operation to which
    manufacturing feature objects are assigned and the assignment type.
    
    :var featureObject: Manufacutring feature objects, can be WeldPoint or ArcWeld.
    :var occChain: Occurrence chain of the manufacturing feature object.
    :var operation: Operation under which manufacturing feature object is assigned.
    :var assignedType: The type assignment of the manufacturing feature object i.e."Assigned", "UnAssigned", or
    "Invalid".
    Assigned means manufacturing feature object is connected to some parts in sourceContexts, it was not present in the
    targetContexts but its connected part was consumed under it. It is now assigned under the targetContext. UnAssigned
    means if the cycleTime property of process station is considered and it is less than the weldTime property of
    manufacturing feature object, the manufacturing feature is not assigned under the targetContexts. Invalid means
    manfacturing feature was earlier connected to some items in sourceContexts but now its connected item is now not
    present under targetContexts.
    """
    featureObject: BusinessObject = None
    occChain: str = ''
    operation: BusinessObject = None
    assignedType: str = ''


@dataclass
class AutomaticMFGFeaturesAssignmentInputInfo(TcBaseObj):
    """
    List of source and target BOMLine objects and assignment related information to be considered for automatic
    allocation of manufacturing features.
    
    :var sourceContexts: List of BOMLine objects under which the manufacturing features to be assigned are present.
    :var targetContexts: The list of process station BOMLine objects in BOPWindow under which the manufacturing
    features will be assigned.
    :var considerCycleTime: If true, the cycle time of process station will be considered while assigment.
    :var matchType: The type of search to perform on the structure. Values may be "NotApplicableMatch", "FullMatch",
    "PartialMatch" or "NoMatch".
    """
    sourceContexts: List[BusinessObject] = ()
    targetContexts: List[BusinessObject] = ()
    considerCycleTime: bool = False
    matchType: str = ''


@dataclass
class AutomaticMFGFeaturesAssignmentResponse(TcBaseObj):
    """
    It is a response for automaticMFGFeaturesAssignment operation.
    
    :var assignmentList: Structure with member as Operation or Process and the list of FeatureAssignmentStruct objects.
    :var logFileTicket: Log file ticket to generate the reports.
    :var logFileName: The name of log file which contain the reports.
    :var serviceData: The ServiceData contains partial errors if any.
    """
    assignmentList: List[StationAssignmentStruct] = ()
    logFileTicket: str = ''
    logFileName: str = ''
    serviceData: ServiceData = None


@dataclass
class StationAssignmentStruct(TcBaseObj):
    """
    This structure contains the station and the list of FeatureAssignmentStruct objects.
    
    :var parentObject: Process station where Operation consuming manufacturing feature objects are assigned.
    :var featureAssignmentList: A list of objects containing information related to assignment of manufacturing feature
    object.
    """
    parentObject: BusinessObject = None
    featureAssignmentList: List[FeatureAssignmentStruct] = ()
