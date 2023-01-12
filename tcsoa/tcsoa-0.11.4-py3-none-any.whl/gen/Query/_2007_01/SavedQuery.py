from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RetrieveQueryCriteriaResponse(TcBaseObj):
    """
    RetrieveQueryCriteriaResponse
    
    :var output: vector of SaveQueryCriteriaInfo
    :var serviceData: standard ServiceData member
    """
    output: List[SaveQueryCriteriaInfo] = ()
    serviceData: ServiceData = None


@dataclass
class SaveQueryCriteriaInfo(TcBaseObj):
    """
    SaveQueryCriteriaInfo
    
    :var searchName: The name of the saved search.
    :var queryName: The name of the query associated with this search.
    :var keys: The attribute names for the query.
    :var values: The attribute values for the query.
    """
    searchName: str = ''
    queryName: str = ''
    keys: List[str] = ()
    values: List[str] = ()
