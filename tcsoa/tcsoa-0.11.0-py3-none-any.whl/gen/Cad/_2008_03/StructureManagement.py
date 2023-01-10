from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AskChildPathBOMLinesInfo(TcBaseObj):
    """
    A set of input information for a single product structure including the associated child paths to be evaluated by
    this operation.
    
    :var clientId: Identifier used to relate partial errors associated with an instance of this information.
    :var parentBomLine: The BOM line parent of the first PS Occurrence Thread UID specified by each of the paths.
    :var useAsStable: Indicates that the child paths are specified by "stable" rather than "real" PS Occurrence Thread
    UIDs.
    :var childPaths: One or more PS Occurrence Thread child paths.
    """
    clientId: str = ''
    parentBomLine: BOMLine = None
    useAsStable: bool = False
    childPaths: List[AskChildPathBOMLinesPath] = ()


@dataclass
class AskChildPathBOMLinesPath(TcBaseObj):
    """
    One or more PS Occurrence Threads defining an input child path within a given product structure from a parent to a
    child.
    
    :var clientId: Identifier used to relate partial errors associated with an instance of this information.
    :var childPath: An ordered list of PS Occurrence Thread UIDs that specify a path from a parent
    Teamcenter::BOMLineImpl through the product structure to the child.
    """
    clientId: str = ''
    childPath: List[str] = ()


@dataclass
class AskChildPathBOMLinesResponse(TcBaseObj):
    """
    Defines the response from the askPSOccThreadChildBOMLines operation.
    
    :var output: A map of input PS Occurrence Thread UIDs to BOMLines.
    :var serviceData: The SOA framework object containing plain objects, and error information.
    """
    output: AskChildPathBOMLineMap = None
    serviceData: ServiceData = None


"""
AskChildPathBOMLineMap
"""
AskChildPathBOMLineMap = Dict[str, BOMLine]
