from __future__ import annotations

from typing import List
from tcsoa.gen.Ai._2012_09.Ai import RequestDetail
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindRequestOnAiWithReferencesResponse(TcBaseObj):
    """
    The latest RequestObjects (by creation date) that are on the AppInterface objects (latest by creation date) that
    reference the input baseRefs .
      The following partial errors may be returned:
    -     Invalid inputs
    -     Permission errors  
    
    
    
    :var details: Each element in the details (type _2012_09::Ai::RequestDetail) vector maps to the corresponding set
    based input vector and contains the following fields.
    :var serviceData: The standard soa serviceData that is used for adding partial errors and sending properties of the
    object. The properties that are returned by default ( without getting not loaded exception ) are:
    - object_name
    - object_desc
    
    """
    details: List[RequestDetail] = ()
    serviceData: ServiceData = None
