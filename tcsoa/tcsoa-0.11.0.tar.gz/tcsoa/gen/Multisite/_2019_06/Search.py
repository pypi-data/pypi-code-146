from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SearchFailure(TcBaseObj):
    """
    This structure returns failure during publish/unpublish operation
    
    :var failureObject: The object that failed to publish.
    :var failedSite: The name of the site the object failed to publish to.
    :var failureCodes: A list of failure codes for the failureObject.
    :var failureStrings: A list of error strings corresponding to each error in failureCodes.
    """
    failureObject: BusinessObject = None
    failedSite: str = ''
    failureCodes: List[int] = ()
    failureStrings: List[str] = ()


@dataclass
class SearchResponse(TcBaseObj):
    """
    Return structure for publish/unpublish operation
    
    :var failureInfo: A list of SearchFailure structures. Each structure contains failure information for a specific
    business object that was supplied.
    :var serviceData: The standard ServiceData return.
    """
    failureInfo: List[SearchFailure] = ()
    serviceData: ServiceData = None


"""
Map of string array property names to values (string, vector).
"""
StringVectorMap1 = Dict[str, List[str]]
