from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanQuery
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindSavedQueriesCriteriaInput(TcBaseObj):
    """
    Structure that contains the input criteria required to find the saved queries.
    
    :var queryNames: Names of saved queries to be found.
    :var queryDescs: Descrptions of saved queries to be found.
    :var queryType: The type of the saved queries.
    """
    queryNames: List[str] = ()
    queryDescs: List[str] = ()
    queryType: int = 0


@dataclass
class FindSavedQueriesResponse(TcBaseObj):
    """
    Holds the response for FindSavedQueries.
    
    :var savedQueries: A vector of Saved Query objects.
    :var serviceData: Standard ServiceData
    """
    savedQueries: List[ImanQuery] = ()
    serviceData: ServiceData = None
