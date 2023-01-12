from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AccCheckInput(TcBaseObj):
    """
    This structure provides a set of input values for accountabilityCheck operation.
    
    :var sourceTags: the source BOM lines
    :var targetTags: the target BOM lines
    :var option: options of search
    :var srcCtxtLineTag: the possible source context line
    :var tarCtxtLineTag: the possible target context line
    :var matchType: represents user choice in the color display
    """
    sourceTags: List[BusinessObject] = ()
    targetTags: List[BusinessObject] = ()
    option: int = 0
    srcCtxtLineTag: BusinessObject = None
    tarCtxtLineTag: BusinessObject = None
    matchType: int = 0


@dataclass
class AccountabilityCheckResponse(TcBaseObj):
    """
    This structure provides response of the call
    
    :var resultSourceTarget: Accountabilty Check result
    :var serviceData: Partial errors
    """
    resultSourceTarget: List[AccountabilityCheckResult] = ()
    serviceData: ServiceData = None


@dataclass
class AccountabilityCheckResult(TcBaseObj):
    """
    The structure characterizes compare result for each source line
    
    :var source: the sourse BOM line
    :var targets: the target BOM lines
    :var checkResult: characterized check result
    """
    source: BusinessObject = None
    targets: List[BusinessObject] = ()
    checkResult: int = 0
