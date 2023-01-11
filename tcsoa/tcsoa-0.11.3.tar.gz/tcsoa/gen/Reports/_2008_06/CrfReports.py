from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReportsCriteria2(TcBaseObj):
    """
    Criteria needed to retrieve report definitions.
    At least one of the optional parameters must be included.
    
    :var clientId: Client identifier for routing purposes (required)
    :var reportDefinitionId: Report definition ID (optional)
    :var reportDefinitionName: Report definition name (optional)
    :var category: Designates report category, e.g. item, summary or custom (optional)
    :var source: Solution source of report definition, e.g. Teamcenter, TcRA (optional)
    :var status: For future use, may be null
    :var contextObjects: A vector of ID's representing context object(s) (required for item reports).
    """
    clientId: str = ''
    reportDefinitionId: str = ''
    reportDefinitionName: str = ''
    category: str = ''
    source: str = ''
    status: str = ''
    contextObjects: List[BusinessObject] = ()
