from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AppearancePathInput(TcBaseObj):
    """
    Input parameter to the ComputeAppearancePath service: holds a parent object and a vector of child paths (relative
    to the object) that we would like to compute the AppearancePaths for.
    
    If the childPaths is an empty vector, the service will return all the values for all the children recursively.
    
    
    
    :var parentObject: The parent of the nodes that we would like to get the APN/ absOccUID. If the parent object does
    not have APN, it would be calculated as well. 
    :var childPaths: The paths to the children for which we would like to get the APN\ absOccUID values. The path is
    relative to the parent object.
    If this vector is empty, the return will include the value for all the children recursively. 
    """
    parentObject: BusinessObject = None
    childPaths: List[NodePath] = ()


@dataclass
class AppearancePathResult(TcBaseObj):
    """
    Holds the values of the apnUID and absOccUID properties for the relevant input
    
    :var absOccUID: The value of bl_absocc_uid_in_topline_context property
    :var apnUID: The value of bl_apn_uid_in_topline_context
    """
    absOccUID: str = ''
    apnUID: str = ''


@dataclass
class NodePath(TcBaseObj):
    """
    This struct holds the path to the node to which we would like to comppute the AppearancePath.
    The path is a vector CloneStableID property (bl_occurrence_uid)
    
    :var threadIDs: The path to the node for which we would like to compute the property values. The path is relative
    to the parent (starts from the parentObject).
    The path is given as a vector of strings which represent threadIDs (CloneStableID)
    """
    threadIDs: List[str] = ()


@dataclass
class ComputeAppearancePathResponse(TcBaseObj):
    """
    Results for ComputeAppearancePath service
    
    :var results: Data structure that holds the results
    :var serviceData: Holds all the modified BO and the errors
    """
    results: List[ComputeAppearancePathResult] = ()
    serviceData: ServiceData = None


@dataclass
class ComputeAppearancePathResult(TcBaseObj):
    """
    Holds the input parent object and the matching results for the childPaths 
    The result for childPaths[i] is in childResults[i].
    
    :var parentObject: The object that was given in the input
    :var childResults: The result matching each index in childPaths in the ComputeAppearancePathInput.
    The results holds values for APN and AbcOccID
    """
    parentObject: BusinessObject = None
    childResults: List[AppearancePathResult] = ()
