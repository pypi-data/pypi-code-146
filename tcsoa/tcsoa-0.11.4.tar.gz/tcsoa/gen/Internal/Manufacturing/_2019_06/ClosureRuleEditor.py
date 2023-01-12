from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TraversedSecondaryObjectInfo(TcBaseObj):
    """
    Information about traversal information of the secondary object.
    
    :var secondaryObjectType: The business object name of the secondary object that is traversed from primary object.
    It can be any business object name.
    :var imanRelationType: The ImanRelation type name that relates the primary and secondary object. It can be any iman
    relation.
    :var imanRelationDescription: Description of the Iman Relation.
    :var isSecondaryIncluded: If true, the secondary object type is included in traversal.
    :var isSecondaryEditable: If true,the user has option to modify the traversal of secondary object.
    :var isPrimaryIncluded: If true, the primary object type is included in traversal.
    :var isPrimaryEditable: If true,the user has option to modify the traversal of primary object.
    """
    secondaryObjectType: str = ''
    imanRelationType: str = ''
    imanRelationDescription: str = ''
    isSecondaryIncluded: bool = False
    isSecondaryEditable: bool = False
    isPrimaryIncluded: bool = False
    isPrimaryEditable: bool = False


@dataclass
class ClosureRuleTraversalInput(TcBaseObj):
    """
    The structure related to selected closure rule and the bomline by the user.
    
    :var topBOMLine: The top BOMLine for traversal information.
    :var closureRuleName: The closure rule name for which the clauses have to be updated.
    """
    topBOMLine: BusinessObject = None
    closureRuleName: str = ''


@dataclass
class ClosureRuleTraversalResponse(TcBaseObj):
    """
    The closure rule traversal response.
    
    :var traversalInfo: A map (string,TraversedSecondaryObjectInfo) of primary object type name and secondary object
    traversal information.
    :var serviceData: Service data containing partial errors.
    """
    traversalInfo: PrimaryToSecondaryTraversalMap = None
    serviceData: ServiceData = None


"""
The map of the primary object type and a structure holding the information about its secondary object types.
"""
PrimaryToSecondaryTraversalMap = Dict[str, List[TraversedSecondaryObjectInfo]]
