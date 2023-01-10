from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetFilteredIPATypeResponse(TcBaseObj):
    """
    resopnse for getFilteredIPAType SOA
    
    :var serviceData: serive data
    :var flat: a vector of processes that their process structure already contain a flat FIPA.
    :var nested: a vector of processes that their process structure already contains a nested FIPA
    :var unset: processes that their process structure doesn't contain any FIPA yet.
    """
    serviceData: ServiceData = None
    flat: List[BusinessObject] = ()
    nested: List[BusinessObject] = ()
    unset: List[BusinessObject] = ()


@dataclass
class DeleteFilteredIPAInputInfo(TcBaseObj):
    """
    Contains the information about deleting filtered IPAs.
    
    :var process: The business object of the process from which filtered IPA needs to be deleted.
    :var isRecursive: Indicates whether all the filtered IPAs in the hierachy of the process should be deleted or just
    one filtered IPA directly under the process should be deleted.
    """
    process: BusinessObject = None
    isRecursive: bool = False
