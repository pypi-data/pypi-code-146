from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindNodeInContextInputInfo(TcBaseObj):
    """
    Input struct for the find node in context service
    
    :var clientID: Client ID
    :var context: The topline that defines the search scope.
    :var nodes: The nodes to search.
    :var byIdOnly: If true all abs occs with the same Id will be search for, if no exact apn is matched.
    :var allContexts: If true then all contexts will be searched otherwise only the current context will be searched if
    no current context specified at the time then the context of the topline is used.
    :var inContextLine: A more specific scope to searh in.
    """
    clientID: str = ''
    context: BusinessObject = None
    nodes: List[BusinessObject] = ()
    byIdOnly: bool = False
    allContexts: bool = False
    inContextLine: BusinessObject = None


@dataclass
class FindNodeInContextResponse(TcBaseObj):
    """
    The Response struct.
    
    :var resultInfo: Infornation retrieves for each input struct that we looked for.
    :var serviceData: Service data.
    """
    resultInfo: List[FoundNodesInfo] = ()
    serviceData: ServiceData = None


@dataclass
class FoundNodesInfo(TcBaseObj):
    """
    A struct that hold all the results on a single search parallel to the one input struct.
    
    :var clientID: Client ID
    :var resultNodes: In each search we look into a vector of nodes to search.
    """
    clientID: str = ''
    resultNodes: List[NodeInfo] = ()


@dataclass
class GetAffectedPropertiesArg(TcBaseObj):
    """
    This structure provides the input parameters for the getAffectedProperties operation.  It describes the property
    changes applied to a process or operation structure for which the affected runtime properties are inquired.
    
    :var rootNode: he root node of the process or operation structure that is inspected.
    :var changedNodes: The list of process or operation nodes that have been changed.
    :var changedProperties: The name of the properties that have been changed.
    """
    rootNode: BusinessObject = None
    changedNodes: List[BusinessObject] = ()
    changedProperties: List[str] = ()


@dataclass
class NodeInfo(TcBaseObj):
    """
    The struct that holds the result for each node in the input.
    
    :var foundNodes: The found nodes we find.
    :var originalNode: The original input node.
    """
    foundNodes: List[BusinessObject] = ()
    originalNode: BusinessObject = None
