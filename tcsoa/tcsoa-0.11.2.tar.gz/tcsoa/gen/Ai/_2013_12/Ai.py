from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Ai._2012_09.Ai import ProjectFilter
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindRequestsWithDependencyFilter(TcBaseObj):
    """
    structure that captures the filtering options for getting the Request Objects after considering dependency. This
    will include the AppInterface filter options too.
    
    :var aiQryParams: structure to capture the filter option on parent(s) ApplicationInterfaces of the RequestObject(s)
    :var requestStatus: vector of strings representing the statuses on the request to search for. Currently, the valid
    values are a combination of (case sensitive): Normal, Warning, Severe, Abort
    :var stateDescription: state description to use for searching for RequestObject.
    :var statusDescription: status message by which to filter for RequestObjects.
    :var customStrings: map of strings that have the custom key and value pair to search on.
    """
    aiQryParams: ProjectFilter = None
    requestStatus: List[str] = ()
    stateDescription: str = ''
    statusDescription: str = ''
    customStrings: StrToStrMap201312 = None


"""
string to string map.
"""
StrToStrMap201312 = Dict[str, str]
