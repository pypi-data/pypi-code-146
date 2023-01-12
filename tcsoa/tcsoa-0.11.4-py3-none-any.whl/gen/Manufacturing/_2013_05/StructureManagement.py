from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class FindAffectedCCsOutput(TcBaseObj):
    """
    The output object for FindAffectedCCs SOA.
    This object contains a list of FindAffectedOutputObject. This vector represents all of the queried objects and all
    of the affected CCs.
    
    :var affectedObjects: Each vector node inside "affectedObjects" includes  a quaried item and a single Collaboration
    Context. For example, if CC1 (Collaboration Context) and CC2 (Collaboration Context) contain inside their process
    structures both item1 and item 2 and the two items are quaried for affected Collaboration Contexts, the output will
    be as follows:
    1. Item1, CC1
    2. Item1, CC2
    3. Item2, CC1
    4. Item2, CC2
    
    Each of the items is represented by two vector nodes, one vector node for each relation to a CC.
    """
    affectedObjects: List[FindAffectedOutputObject] = ()


@dataclass
class FindAffectedCCsResponse(TcBaseObj):
    """
    A list of output objects and a service data.
    
    :var output: The output data includes the affected CCs and the items which is related to each CC.
    :var serviceData: The service data output.
    """
    output: List[FindAffectedCCsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class FindAffectedOutputObject(TcBaseObj):
    """
    The output object which contains the queried object and one of it's related CCs
    
    :var queryObject: The item queried for affected CCs.
    :var affectedCC: One of the affected CCs of the query item.
    """
    queryObject: WorkspaceObject = None
    affectedCC: WorkspaceObject = None
