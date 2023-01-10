from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindCheckedOutsInStructureResponse(TcBaseObj):
    """
    Return structure for findCheckedOutsInStructure operation
    
    :var checkedOutList: This is the structure contains the Tags of all the checked outs objects.
    :var serviceData: This is a common data strucuture used to return sets of Teamcenter
    Data Model object from a service request. This also holds services exceptions.
    """
    checkedOutList: List[BusinessObject] = ()
    serviceData: ServiceData = None
