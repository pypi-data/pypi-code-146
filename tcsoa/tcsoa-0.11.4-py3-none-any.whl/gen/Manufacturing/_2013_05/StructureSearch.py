from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindStudiesResponse(TcBaseObj):
    """
    The response data from the findStudies service operation.
    
    :var results: The found Mfg0BvrStudy objects for each inputNodes Mfg0BvrProcess or Mfg0BvrOperation
    :var serviceData: Service Data
    """
    results: List[FindStudiesResults] = ()
    serviceData: ServiceData = None


@dataclass
class FindStudiesResults(TcBaseObj):
    """
    A list of Mfg0BvrStudy objects
    
    :var listOfStudies: A list of Mfg0BvrStudy objects
    """
    listOfStudies: List[BusinessObject] = ()
