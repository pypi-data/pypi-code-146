from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MapSrchCriteriaToLinesInputInfo(TcBaseObj):
    """
    Input object for mapSrchCriteriaToLines action.
    
    :var criteria: Search criteria object which needs to be interpreted. The search criteria objects can be of type
    ApprSearchCriteria or its sub types.
    :var contexts: Represents the context under which the objects will be found. The valid type of this parameter is
    BOM line or its sub types.
    """
    criteria: BusinessObject = None
    contexts: List[BusinessObject] = ()


@dataclass
class MapSrchCriteriaToLinesResponse(TcBaseObj):
    """
    Response object for mapSrchCriteriaToLines action.
    
    :var output: Vector of type SrchCriteriaToLinesMap which contains the search criteria and BOMLines.
    :var serviceData: Contains general exceptions  if occurred during mapSrchCriteriaToLines action.
    """
    output: List[SrchCriteriaToLinesMap] = ()
    serviceData: ServiceData = None


@dataclass
class SaveOGLinesInSrchCriteriaInputInfo(TcBaseObj):
    """
    Input object for saveOGLinesInSrchCriteria action.
    
    :var selectedNodes: The BOM line occurrences from the Occurrence Group structure which are in the selected state..
    Valid values are Occurrence Group BOP lines or normal BOM lines.
    :var unselectedNodes: The BOM line occurrences from the Occurrence Group structure which are in the unselected
    state.. Valid values are Occurrence Group BOP lines or normal BOM lines.
    :var scopeAttribute: Tells whether to create scope search criteria object (Fnd0ApprSchCriteriaScpAttr) or select
    state search criteria object( ApprSearchCriteriaSlctState). Value True means an object of scope search criteria
    will be returned.
    """
    selectedNodes: List[BusinessObject] = ()
    unselectedNodes: List[BusinessObject] = ()
    scopeAttribute: bool = False


@dataclass
class SaveOGLinesInSrchCriteriaResponse(TcBaseObj):
    """
    Output response object for saveOGLinesInSrchCriteria action.
    
    :var srchCriterias: Vector of objects of ApprSearchCriteria (its appropreate sub types) created by this operation.
    :var serviceData: Contains general exceptions if occurred during creation of Search Criteria object.
    """
    srchCriterias: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class SrchCriteriaToLinesMap(TcBaseObj):
    """
    Structure created to maintain a relation between search criteria and BOMLines.
    
    :var srchCriteria: The interpreted search criteria.
    :var selectedNodes: Selected BOMlines which were stored in the search criteria.
    :var unselectedNodes: Unselected BOMlines which were stored in the search criteria.
    """
    srchCriteria: BusinessObject = None
    selectedNodes: List[BusinessObject] = ()
    unselectedNodes: List[BusinessObject] = ()
