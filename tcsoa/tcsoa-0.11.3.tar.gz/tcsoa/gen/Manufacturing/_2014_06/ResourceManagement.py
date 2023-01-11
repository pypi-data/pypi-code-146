from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CheckResult(TcBaseObj):
    """
    Contains the check results for one tool.
    
    :var icoId: The ID of the tool whose parameters were checked.
    :var status: If the status value is 0, checking succeeded. If it is not 0, some check failed. The details why the
    checking failed are described in the report.
    
    :var report: A list of strings that make up the lines of the report.
    """
    icoId: str = ''
    status: int = 0
    report: List[str] = ()


@dataclass
class CheckToolParametersResponse(TcBaseObj):
    """
    A CheckToolParametersResponse structure contains the reports and statuses for all tools that were checked, as well
    as a ServiceData object that may contain error descriptions, if any errors occurred.
    
    :var serviceData: Service data that can contain error descriptions.
    :var checkResults: A list containing a check result for each tool.
    """
    serviceData: ServiceData = None
    checkResults: List[CheckResult] = ()
