from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OkToCheckoutResponse(TcBaseObj):
    """
    This structure contains the list and 'ServiceData' objects. The list contains verdict true or false for passed in
    object indicating if object can be checked out or not. 'ServiceData' contains error at index where it occurred for
    each input object.
    
    :var verdict: A list indicating if the input business object can be checked out. "true" indicates the object may be
    checked out. "false" indicates the object may not be checked out.
    :var serviceData: Contains the partial errors for any objects for which the 'okToCheckout' validation failed.
    """
    verdict: List[bool] = ()
    serviceData: ServiceData = None
