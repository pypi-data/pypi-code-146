from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, MEAppearancePathNode, ItemRevision
from typing import Dict, List
from tcsoa.gen.Internal.Rdv._2009_01.VariantManagement import NVEMetaToken
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NodeAnswer(TcBaseObj):
    """
    Structure containing list of valid background nodes for distance/target
    
    :var backgroundNodeList: List of AppearancePathNode UIDs
    """
    backgroundNodeList: List[str] = ()


@dataclass
class OccNotesAttributes(TcBaseObj):
    """
    The part data information about each component is provided by way of the OccNotesAttributes data structure.
    
    :var noteType: The Note Type for the Part Solution to be added.
    :var noteText: The Note Text for the Part Solution to be added.
    """
    noteType: str = ''
    noteText: str = ''


@dataclass
class ProximityTarget(TcBaseObj):
    """
    Structure contain references to proximity distance and target BOMLine objects APN UID.
    
    :var proxtargetId: Identifier that helps the client track the object(s) created.
    :var proximity: Proximity Distance in assembly units (supported by the underlying search engine)
    :var target: target BOMLine APN UID
    """
    proxtargetId: str = ''
    proximity: float = 0.0
    target: str = ''


@dataclass
class ReplacePartSolutionInputInfo(TcBaseObj):
    """
    The information to replace part is provided by way of the 'ReplacePartSolutionInputInfo' data structure.
    
    :var values: List of OccNotesAttributes objects for each replacing component that contains the Part data for the
    replacing Part Solution, i.e. all the Note Types for the Part Solution along with the corresponding Note Texts.
    :var component: The reference to the Part Solution to be replaced with.  It should be of type Item Revision or its
    subtypes. This is a mandatory attribute for the operation to succeed and cannot be null.
    :var bomLine: The BOMLine object for which the Part Solution is to be replaced. This is a mandatory attribute for
    the operation to succeed and cannot be null.
    :var abeAPN: The Appearance Path Node of the associated Architecture Breakdown Element.
    :var metaExpr: List of NVEMetaExpression objects to be applied to new replaced Part Solution. The Meta Expression
    helps in balancing out the variant condition before generating the variant condition.
    :var validate: A flag. If set to true the operation will validate the combination of variants supplied through the
    NVEs and will fail the operation if the validation fails.
    :var splitAndClone: A flag which states whether the clone should be created or not.
    :var carrySubstitutes: A flag which states whether the substitutes should be carried forward or not.
    :var quantity: The quantity of the replacing Part Solution.
    """
    values: List[OccNotesAttributes] = ()
    component: ItemRevision = None
    bomLine: BOMLine = None
    abeAPN: MEAppearancePathNode = None
    metaExpr: List[NVEMetaToken] = ()
    validate: bool = False
    splitAndClone: bool = False
    carrySubstitutes: bool = False
    quantity: int = 0


@dataclass
class ReplacePartSolutionOutputInfo(TcBaseObj):
    """
    The structure 'ReplacePartSolutionOutputInfo' represents the output information for 'replacePartInProduct'
    operation.
    
    :var bomLine: The bomline for which the Part Solution is to be replaced.
    :var component: The newly replaced Part Solution. It will be of type Item Revision or its subtypes.
    """
    bomLine: BOMLine = None
    component: ItemRevision = None


@dataclass
class ReplacePartSolutionResponse(TcBaseObj):
    """
    The 'ReplacePartSolutionResponse' structure represents the reference of the newly added component and the
    'ServiceData' object.
    
    :var output: The list of  ReplacePartSolutionOutputInfo objects.
    :var serviceData: The 'ServiceData' object containing error codes and error messages along with the indices for
    which the 'replacePartInProduct' operation fails.
    """
    output: List[ReplacePartSolutionOutputInfo] = ()
    serviceData: ServiceData = None


@dataclass
class BackgroundOccurrences(TcBaseObj):
    """
    Output structure that contains the references to valid background nodes
    
    :var numProcessedRequests: actual number of the answers (empty aswell) provided
    :var numSuggestedRequests: server suggested number of the answers provided. Ex:100
    :var nodeanswerLists: list of 'NodeAnswer' objects corresponding to the respective targets
    """
    numProcessedRequests: int = 0
    numSuggestedRequests: int = 0
    nodeanswerLists: List[NodeAnswer] = ()


@dataclass
class BackgroundOccurrencesResponse(TcBaseObj):
    """
    Main output structure that contains the references to valid background nodes (APN or Absocc) UIDs and 'ServiceData'
    
    :var output: List of 'BackgroundOccurrence' objects for respective 'TargetOccurence' objects
    :var servicedata: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    """
    output: BackgroundOccurrencesMap = None
    servicedata: ServiceData = None


@dataclass
class TargetOccurrences(TcBaseObj):
    """
    Main input structure containing references to distance and targets
    
    :var clientId: Identifier that helps the client track the object(s) created. This is used to correlate the input
    objects with the output response being sent back to the client.
    :var topitemrev: UID of top ItemRevision
    :var revrulename: Name of the RevisionRule
    :var disttargetsList: List of target APN or Absocc UIDs and corresponding proximity distances
    """
    clientId: str = ''
    topitemrev: str = ''
    revrulename: str = ''
    disttargetsList: List[ProximityTarget] = ()


@dataclass
class AddPartSolutionInputInfo(TcBaseObj):
    """
    The information of added part is provided by way of the 'AddPartSolutionInputInfo' data structure.
    
    :var values: The 'OccNotesAttributes' for each added component that contains the Part data for the Part Solution 
    to be added, i.e. all the Note Types for the Part Solution along with the corresponding Note Texts.
    :var component: The reference to the Part Solution to be added.  It should be of type Item Revision or its
    subtypes. This is a mandatory attribute for the operation to succeed and cannot be null.
    :var abeLine: The BOMLine object to which the Part Solution is to be added. This is a mandatory attribute for the
    operation to succeed and cannot be null.
    :var prodRevs: The reference to the Product Item Revisions associated with the Architecture Breakdown for each Part
    Solution to be added. This is a mandatory attribute for the operation to succeed and cannot be null.
    :var abeApn: The Appearance Path Node for each  Part Solution to be added.
    :var metaExpr: The list of NVEMetaExpression objects to be applied  to new Part Solution. The Meta Expression helps
    in balancing out the variant condition before generating the variant condition.
    :var validate: A flag if set to true the operation will validate the combination of variants supplied through the
    NVEs and will fail the operation if the validation fails.
    :var quantity: The quantity of the Part Solution to be added.
    """
    values: List[OccNotesAttributes] = ()
    component: ItemRevision = None
    abeLine: BOMLine = None
    prodRevs: List[ItemRevision] = ()
    abeApn: MEAppearancePathNode = None
    metaExpr: List[NVEMetaToken] = ()
    validate: bool = False
    quantity: int = 0


@dataclass
class AddPartSolutionOutputInfo(TcBaseObj):
    """
    The structure 'AddPartSolutionOutputInfo' represents the output information for 'addPartToProduct' operation.
    
    :var component: The Part Solution to be added. It should be of type Item Revision or its subtypes.
    :var partSolutionAPN: Appearance Path Node of the newly added Part Solution.
    """
    component: ItemRevision = None
    partSolutionAPN: MEAppearancePathNode = None


@dataclass
class AddPartSolutionResponse(TcBaseObj):
    """
    The 'AddPartSolutionResponse' structure represents reference to the Appearance Path Node corresponding to the newly
    added part solution and the 'ServiceData' object.
    
    :var output: List of  'AddPartSolutionOutputInfo' objects containing Appearance Path Nodes corresponding to each of
    the newly added Part Solutions.
    :var serviceData: The 'ServiceData' object containing error codes and error messages along with the indices for
    which the 'addPartToProduct' operation fails.
    """
    output: List[AddPartSolutionOutputInfo] = ()
    serviceData: ServiceData = None


"""
Mapping of clientId to output BackgroundOccurences
"""
BackgroundOccurrencesMap = Dict[str, BackgroundOccurrences]
