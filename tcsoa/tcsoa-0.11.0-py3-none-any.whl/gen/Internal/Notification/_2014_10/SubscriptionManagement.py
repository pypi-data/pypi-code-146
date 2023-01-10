from __future__ import annotations

from tcsoa.gen.BusinessObjects import Condition
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetSubscriptionConditionsResponse(TcBaseObj):
    """
    The response from the query request will include a list of the Conditions that have the correct signature to be
    used as Subscription criteria.
    
    :var conditions: A list of the Condition objects that can be used as part of a Subscription definition.
    :var serviceData: Returned service data.
    """
    conditions: List[Condition] = ()
    serviceData: ServiceData = None
