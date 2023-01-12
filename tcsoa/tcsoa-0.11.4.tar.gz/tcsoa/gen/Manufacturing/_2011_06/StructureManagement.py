from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReferencedContexts(TcBaseObj):
    """
    the structure used for three different modes: add, set, remove
    
    :var context: the top line of BOP window which will be referenced
    :var addRefContexts: contexts, which will reference
    :var removeRefContexts: contexts, which will be removed
    :var removeExistingRef: remove all referenced contexts
    """
    context: BusinessObject = None
    addRefContexts: List[BusinessObject] = ()
    removeRefContexts: List[BusinessObject] = ()
    removeExistingRef: bool = False


@dataclass
class ReferencedContextsResponse(TcBaseObj):
    """
    the structure contains referenced contexts and used for response.
    
    :var refcontexts: vector of vectors referenced contexts according to the order from the input vector
    :var serviceData: service data will return errors only. No data will be return via Service Data.
    """
    refcontexts: List[ContextsArray] = ()
    serviceData: ServiceData = None


@dataclass
class ContextsArray(TcBaseObj):
    """
    the structure contains array of contexts
    
    :var contextsarray: array of contexts ( any types)
    """
    contextsarray: List[BusinessObject] = ()
