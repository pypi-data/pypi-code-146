from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOfficeStyleSheetResponse(TcBaseObj):
    """
    The list of Office template stylesheets attached to the ReportDefinition.
    
    :var officetemplates: The names of the office template stylesheets attached to the ReportDefinition object via the
    GRM relationship.
    :var serviceData: The standard ServiceData
    """
    officetemplates: List[str] = ()
    serviceData: ServiceData = None
