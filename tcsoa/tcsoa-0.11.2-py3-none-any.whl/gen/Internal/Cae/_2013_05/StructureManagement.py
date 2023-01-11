from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetCAEPropertyComparisonDetailsResponse(TcBaseObj):
    """
    Data structure to capture the response of 'getCAEPropertyComparisonDetails' method. This has property comparison
    details for selected BOMLine object and 'serviceData' to capture the partial errors.
    
    :var result: Detail results of the comparison for the selected BOMLine object. This is an XML document that
    conforms to the http://www.ugs.com/Schemas/SMENode schema.
    :var serviceData: 'serviceData' member to capture any partial errors.
    """
    result: str = ''
    serviceData: ServiceData = None
