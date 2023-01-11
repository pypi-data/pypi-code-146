from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SearchBOEInputInfo(TcBaseObj):
    """
    List of Plant BOP lines and a map of search criteria.
    
    :var inputScopes: A list of Business object representing Plant Bill of Process  (Plant BOP) lines.
    :var searchCriteria: A map (string, string) of search criteria. The key of the map is the criterion and its value
    is the information about that criterion.
    """
    inputScopes: List[BusinessObject] = ()
    searchCriteria: SearchCriteriaMap = None


@dataclass
class SearchBOEResponse(TcBaseObj):
    """
    The response contains a list of all the BOE objects which matches the search criteria. The following partial errors
    may be returned:
    (i) 253037: The Search criteria does not contain the closure rule name property.
    (ii) 253041: The given closure rule is invalid.
    (iii) 200181: This type of search is not supported.
    
    :var resultObjects: The list of the result BOE objects matched as per the criteria. The Bill of Equipment stations
    hold location information and contain the equipment required for manufacturing.
    :var serviceData: The Service Data.
    """
    resultObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


"""
A map (string, string) where key represents the type of search criterion and the value represents additional information to perform the search.
For ex.
1. Search using closure rule: the key is "Closure_Rule" and the value is the name of the closure rule "MFGProcessAreaConsumption".
2. Search using occurrence type: the key is "Valid_Occ_Type" and the value is "MEWorkarea".
"""
SearchCriteriaMap = Dict[str, str]
