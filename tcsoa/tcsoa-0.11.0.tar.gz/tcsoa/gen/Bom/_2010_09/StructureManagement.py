from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ObjectCoverageInput(TcBaseObj):
    """
    Structure contains input parameters for verifyObjectCoverageByRule operation
    
    :var contexts: scoped lines in the target window
    :var objectsToCheck: the list of lines,that will be checked against the supplied closure rule
    :var closureRule: the closure rule selected by the user
    :var depth: the traversal depth entered by the user
    :var otherStructure: context of another structure (can be window or any line in it)
    """
    contexts: List[BusinessObject] = ()
    objectsToCheck: List[BusinessObject] = ()
    closureRule: str = ''
    depth: int = 0
    otherStructure: BusinessObject = None


@dataclass
class ObjectCoverageResponse(TcBaseObj):
    """
    Structure contains output parameters for verifyObjectCoverageByRule operation
    
    :var covered: return vector (corresponds to the input objects vector) - with true or false
    :var serviceData: contains any errors received during the execution
    """
    covered: List[bool] = ()
    serviceData: ServiceData = None


@dataclass
class TraversedObjectsInput(TcBaseObj):
    """
    structure contains input parameters for getTraversedObjectsByRule operation
    
    :var scopeObjects: the scope lines selected by the user
    :var closureRule: the closure rule selected by the user
    :var depth: the traversal depth entered by the user
    :var otherStructure: target context (can be window or any line in it)
    """
    scopeObjects: List[BusinessObject] = ()
    closureRule: str = ''
    depth: int = 0
    otherStructure: BusinessObject = None


@dataclass
class TraversedObjectsResponse(TcBaseObj):
    """
    structure contains output parameters for getTraversedObjectsByRule operation
    
    :var resultObjects: return vector of the the auto-expanded/filtered lines
    :var serviceData: return errors if verifacation was failed or illegal
    """
    resultObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None
