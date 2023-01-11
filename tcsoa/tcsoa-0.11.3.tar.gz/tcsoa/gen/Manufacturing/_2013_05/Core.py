from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject
from typing import Dict, List
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
    :var relationTypes: A list of relation types, currently only FND_TraceLink relation is supported.
    :var relationDirection: The relation direction to search. The value includes 1(primary), 2(secondary) and 0(primary
    and secondary). It is only valid if the relation types are given.
    :var relationDepth: The depth to search, -1 to search all levels and any other positive integer value to search up
    to that level. It is only valid if the relation types are given.
    """
    clientID: str = ''
    context: BusinessObject = None
    nodes: List[BusinessObject] = ()
    byIdOnly: bool = False
    allContexts: bool = False
    inContextLine: BusinessObject = None
    relationTypes: List[str] = ()
    relationDirection: int = 0
    relationDepth: int = 0


@dataclass
class MatchObjectsAgainstVariantRulesArg(TcBaseObj):
    """
    This structure provides input parameters for the matchObjectsAgainstVariantRules operation.
    
    :var objects: The objects whose variant definition is to be checked against the set of variant rules or product
    variants. Currently only BOMLines are accepted.
    :var variantRules: The variant rules or product variants which are to be applied consecutively to each object. The
    objects must be of type 'VariantRule' or 'Mfg0BvrProductVariant', respectively.
    """
    objects: List[RuntimeBusinessObject] = ()
    variantRules: List[BusinessObject] = ()


@dataclass
class MatchObjectsAgainstVariantRulesResponse(TcBaseObj):
    """
    The response structure for the matchObjectsAgainstVariantRules operation.
    
    :var serviceData: The ServiceData object for this request.
    :var results: A list of result structures; each entry corresponds to an entry in the
    MatchObjectsAgainstVariantRulesArg vector passed to the matchObjectsAgainstVariantRules operation.
    """
    serviceData: ServiceData = None
    results: List[MatchObjectsAgainstVariantRulesResult] = ()


@dataclass
class MatchObjectsAgainstVariantRulesResult(TcBaseObj):
    """
    A set of data collected by the matchObjectsAgainstVariantRules operation for a specific
    MatchObjectsAgainstVariantRulesArg structure.
    
    :var matrix: A map that holds for each of the runtime objects supplied in the MatchObjectsAgainstVariantRulesArg
    structure the matching variant rules or product variants.
    :var warnings: A list of localized warning messages that describe inconsistencies in the configuration of the
    involved windows, if the variant configuration of a window does not satisfy the configuration of a supplied variant
    rule or product variant. The warnings are of the form "The window configuration for structure "<top line title>""
    is missing the following variant rule/product variant(s): <rule-name>, ...".
    """
    matrix: VariantRuleMap = None
    warnings: List[str] = ()


"""
A map that collects for a set of runtime objects a list of variant rules or, alternatively, product variants. This type maps a 'RuntimeBusinessObject' to a list of 'BusinessObject's.
"""
VariantRuleMap = Dict[RuntimeBusinessObject, List[BusinessObject]]
