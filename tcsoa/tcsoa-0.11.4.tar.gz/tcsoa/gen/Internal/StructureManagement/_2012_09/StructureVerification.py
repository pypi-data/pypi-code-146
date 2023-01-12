from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetValidCriteriaResponse(TcBaseObj):
    """
    Returns the vector of map of criteria names (This vector will be the same size as the inputScope vector). In
    addition any partial errors are returned in the serviceData member.
    
    :var criteriamap: The map of criteria name(string) and localized names (vector). Currently both the key and value
    are the same. The size of this vector matches the size of the inputScope vector.
    :var serviceData: serviceData to return any partial errors
    """
    criteriamap: List[CriteriaNamesMap] = ()
    serviceData: ServiceData = None


@dataclass
class ValidCriteriaInput(TcBaseObj):
    """
    Provides a set of input values to get the valid criteria
    
    :var sourcescope: Selected source tags to find out the valid critera for accountability check.
    :var targetscope: Selected target tags to find the valid criteria for accountability check.
    """
    sourcescope: List[BusinessObject] = ()
    targetscope: List[BusinessObject] = ()


"""
Map for criteria names. Key is the real name and value is localized name.
"""
CriteriaNamesMap = Dict[str, str]
