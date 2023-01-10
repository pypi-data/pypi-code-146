from __future__ import annotations

from tcsoa.gen.Manufacturing._2014_12.StructureSearch import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindCPCResponse(TcBaseObj):
    """
    List of CPC objects found.
    
    :var foundCPCs: The list of MECollaborationContext objects.
    :var serviceData: The service data containing partial errors if any.
    """
    foundCPCs: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class FindEquivalentLinesIn(TcBaseObj):
    """
    Contains the details of an equivalence search input.
    
    :var sourceLines: The source BOMLine objects to start the equivalent search from.
    :var targetScopes: The BOMLine objects representing target scopes to search equivalents under.
    :var isSourceAScope: If true, sourceLines represent a list of scopes under which traversal will be performed.
    Otherwise, sourceLines are those lines that themselves will be searched for.
    :var sourceClosureRule: If isSourceAScope is true, this field is the closure rule name to traverse the source
    scopes.
    :var searchCriteria: The search criteria. Currently supported values: 1 - ID in Context (Top Level) only, 2 - ID in
    Context (Top Level) or Item ID and Absolute Transformation Matrix.
    :var additionalInfo: Additional input information; currently not used.
    """
    sourceLines: List[BusinessObject] = ()
    targetScopes: List[BusinessObject] = ()
    isSourceAScope: bool = False
    sourceClosureRule: str = ''
    searchCriteria: int = 0
    additionalInfo: AdditionalInfo = None


@dataclass
class FindEquivalentLinesResp(TcBaseObj):
    """
    Contains the details of the equivalence search results.
    
    :var equivalenceResults: A list of EquivalenceResult objects containing the equivalence relation between source
    BOMLine objects and their equivalent target BOMLine objects. The size of equivalenceResults list in this structure
    matches that of the searchInputs list.
    :var serviceData: The ServiceData containing partial errors.
    :var additionalInfo: Additional input information; currently not used.
    """
    equivalenceResults: List[EquivalenceResult] = ()
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class EquivalenceResult(TcBaseObj):
    """
    Contains the details of equivalence search result for a single FindEquivalentLinesIn object.
    
    :var equivalenceResults: A map from source BOMLine objects to their equivalent target BOMLine objects. The size of
    the map matches that of the sourceLines list in the FindEquivalentLinesIn structure.
    """
    equivalenceResults: ObjToObjVectorMap = None


"""
A map of BusinessObject to vector of BusinessObject instances.
"""
ObjToObjVectorMap = Dict[BusinessObject, List[BusinessObject]]
