from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CheckOutForSignResponse(TcBaseObj):
    """
    This structure contains the list of true or false corresponding the input list of the Dataset objects and the list
    of partial errors.
    
    :var verdict: If the Dataset is digitally checked out, the corresponding verdict is true, otherwise false,
    corresponding one to one to input Dataset object.
    :var serviceData: The partial error list if there is any system errors.
    """
    verdict: List[bool] = ()
    serviceData: ServiceData = None
