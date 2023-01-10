from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0Profiler
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PerformanceInfoResponse(TcBaseObj):
    """
    A structure of vector of 'Fnd0Profiler' and 'ServiceData'.
    
    :var performanceServiceData: Partial Errors if any.
    :var performanceDataVec: List of 'Fnd0Profiler' objects, one for each service operation request executed.
    """
    performanceServiceData: ServiceData = None
    performanceDataVec: List[Fnd0Profiler] = ()
