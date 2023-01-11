from __future__ import annotations

from tcsoa.gen.BusinessObjects import IRDC
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class IRDCResponse(TcBaseObj):
    """
    The IRDC response structure
    
    :var outIRDC: The list of references to class IRDC.
    :var svcData: The Service Data. Partial errors and failures are updated and returned through this object.
    """
    outIRDC: List[IRDC] = ()
    svcData: ServiceData = None
