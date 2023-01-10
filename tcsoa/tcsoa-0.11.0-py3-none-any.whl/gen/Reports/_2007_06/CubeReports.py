from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TcRAReportsCriteria(TcBaseObj):
    """
    Criteria needed to retrieve the URL for the specified TcRA operation.
    
    :var messageName: It designates desired TcRA report definition operation, e.g. retrieve, view, edit, delete or set
    permission.
    :var reportDefinition: The report definition ID.
    :var contextObjects: A list of ID's representing context object(s) (required for item reports).
    """
    messageName: str = ''
    reportDefinition: BusinessObject = None
    contextObjects: List[BusinessObject] = ()


@dataclass
class ConstructReportURLResponse(TcBaseObj):
    """
    The response object from constructReportURL operation.
    
    :var url: The URL string for the TcRA servlet.
    :var serviceData: The ServiceData which contains the error stack.
    """
    url: str = ''
    serviceData: ServiceData = None
