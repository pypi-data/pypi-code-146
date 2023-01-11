from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MFGNodePropertyValues(TcBaseObj):
    """
    The structure that holds MFGNode along with property names and their values.
    
    :var node: The MFGNode in BOP structure.
    :var props: Map of Property Name Value Pair
    """
    node: BusinessObject = None
    props: MFGPropertyNameValueMap = None


@dataclass
class PropertyCollectorOutput(TcBaseObj):
    """
    Output structure containing MfgNode, set of Properties that are evaluated for the node and set of property values
    corresponding to the property names.
    
    :var contextType: Context Type of MfgNode
    :var nodeValueList: The vector of MFGNodePropertyValues.
    """
    contextType: str = ''
    nodeValueList: List[MFGNodePropertyValues] = ()


@dataclass
class PropertyCollectorVisitorInfo(TcBaseObj):
    """
    This structure contains list of properties to collect for the corresponding Traversal Rule Key
    
    :var traversalVisitorsKeys: The collection of type of MfgNode and its corresponding MfgContext type.
    :var propToCollectList: The list of properties to be evaluated for the type of MfgNode specified in
    traversalRuleKey.
    """
    traversalVisitorsKeys: List[TraversalKeyInfo] = ()
    propToCollectList: List[str] = ()


@dataclass
class TraversalKeyInfo(TcBaseObj):
    """
    This is a structure of MFGNode types and MFGContext
    
    :var types: set of MFGNode types
    :var context: context of MFGNodes
    """
    types: List[str] = ()
    context: str = ''


@dataclass
class TraversalRuleInfo(TcBaseObj):
    """
    This structure contains TraversalRuleKeys and their corresponding relations properties.
    
    :var traversalRuleKeys: The collection of type of MfgNode and its corresponding MfgContext type.
    :var targets: The list of properties to be used to traverse for current MfgNode to its sub nodes.
    """
    traversalRuleKeys: List[TraversalKeyInfo] = ()
    targets: List[str] = ()


@dataclass
class CollectPropertiesInputInfo(TcBaseObj):
    """
    This is a input structure containing rootNode, set of Traversal Rules and a set of Traversal Visitor info.
    
    :var clientId: Client ID
    :var rootNode: The root node to traverse from.
    :var traversalRuleList: The traversal rules to be used while traversing BOP structure.
    :var propVisitorList: The collection of type of MfgNodes and properties to collect for the type.
    """
    clientId: str = ''
    rootNode: BusinessObject = None
    traversalRuleList: List[TraversalRuleInfo] = ()
    propVisitorList: List[PropertyCollectorVisitorInfo] = ()


@dataclass
class CollectPropertiesOutput(TcBaseObj):
    """
    Structure containing client Id and PropertyCollectoroutput
    
    :var clientId: Client ID
    :var output: vector of PropertyCollectorOutput
    """
    clientId: str = ''
    output: List[PropertyCollectorOutput] = ()


@dataclass
class CollectPropertiesResponse(TcBaseObj):
    """
    Response structure containing service data
    
    :var outputList: The collection of MfgNode, property names and theit values.
    :var serviceData: service data containing partial error data
    """
    outputList: List[CollectPropertiesOutput] = ()
    serviceData: ServiceData = None


"""
This map holds the property name value pairs
"""
MFGPropertyNameValueMap = Dict[str, List[str]]
