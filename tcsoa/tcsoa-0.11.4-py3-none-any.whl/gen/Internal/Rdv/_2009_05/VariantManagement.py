from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Internal.Rdv._2009_01.VariantManagement import MetaExprTokens
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NVEMetaExprTokensResponse(TcBaseObj):
    """
    This structure contains list of 'MetaExprTokens' and the 'ServiceData' object.
    
    :var metaExprs: Contains the list of 'MetaExprTokens' objects.
    :var serviceData: The ServiceData object containing full/partial errors.
    """
    metaExprs: List[MetaExprTokens] = ()
    serviceData: ServiceData = None


@dataclass
class SearchResponse(TcBaseObj):
    """
    'SearchResponse' structure contains the location of the plmxml file on the transient volume, in which the search
    results are available.
    
    :var plmxmlFileLocation: The pruned plmxml file location to download to client
    :var serviceData: The 'ServiceData' object containing the PartialError details, if any.
    """
    plmxmlFileLocation: str = ''
    serviceData: ServiceData = None


@dataclass
class SearchResults(TcBaseObj):
    """
    'SearchResults' structure contains all the search results along with errors if any, after the search completion
    
    :var backgroundBOMLines: Vector of BOMLine objects that matched the search criteria
    :var unconfiguredBOMLines: Vector of BOMLine objects that did not match the search criteria but are still part of
    the product context
    :var unconfigurableBOMLines: Vector of BOMLine objects that were encountered during the process of matching the
    bookmark strings for which no revision configures using the current RevisionRule, leaving some bookmark strings
    unmatched
    :var unconfiguredVOOBOMLines: Vector of BOMLine objects that got unconfigured by applying the Valid Overlay Options
    with the input criteria
    :var serviceData: An object of 'ServiceData' which contains any errors if occurred during execution of the VOO
    operation.
    """
    backgroundBOMLines: List[BOMLine] = ()
    unconfiguredBOMLines: List[BOMLine] = ()
    unconfigurableBOMLines: List[BOMLine] = ()
    unconfiguredVOOBOMLines: List[BOMLine] = ()
    serviceData: ServiceData = None
