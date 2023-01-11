from __future__ import annotations

from tcsoa.gen.StructureManagement._2010_09.StructureVerification import AccountabilityCheckResult
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AccountabilityCheckResponse(TcBaseObj):
    """
    Contains all the results from the accountabilityCheck operation
    
    :var accountabilityCheckResults: A vector of accountability check results
    :var reachableTargets: A vector of reachable target lines
    :var serviceData: The service data
    :var sourceConfigContext: The source configuration context for an equivalent source object.
    :var targetConfigContext: The target configuration context for an equivalent target object.
    """
    accountabilityCheckResults: List[AccountabilityCheckResult] = ()
    reachableTargets: List[BusinessObject] = ()
    serviceData: ServiceData = None
    sourceConfigContext: BusinessObject = None
    targetConfigContext: BusinessObject = None
