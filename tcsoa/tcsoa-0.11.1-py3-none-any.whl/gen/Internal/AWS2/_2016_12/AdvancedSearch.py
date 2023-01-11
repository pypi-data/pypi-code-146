from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awp0AdvancedQueryCriteria, Awp0AdvancedSearchInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AdvancedQueryCriteriaResponse(TcBaseObj):
    """
    Response structure for selected Query Criteria.
    
    :var serviceData: The Service Data.
    :var advancedQueryCriteria: The newly created Advanced Query Criteria business object.
    """
    serviceData: ServiceData = None
    advancedQueryCriteria: Awp0AdvancedQueryCriteria = None


@dataclass
class AdvancedSearchResponse(TcBaseObj):
    """
    Response structure for AdvancedSearch service.
    
    :var advancedSearchInput: The newly created AdvancedSearch Input business object.
    :var serviceData: The Service Data.
    """
    advancedSearchInput: Awp0AdvancedSearchInput = None
    serviceData: ServiceData = None
