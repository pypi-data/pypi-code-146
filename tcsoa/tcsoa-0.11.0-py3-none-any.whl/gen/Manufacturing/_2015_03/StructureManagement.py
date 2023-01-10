from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MoveAndResequenceParameter(TcBaseObj):
    """
    The structure specifies the nodes to be moved, their target, whether dropped on the target, context based on which
    find number to be decided and whether to clone or move the nodes to the new target.
    
    :var sourceNodes: A list of BOMLine objects to be re-sequenced within parent or moved to another target BOMLine.
    :var targetNode: The BOMLine to which the source BOMLine objects are to be moved.
    :var predecessor: The BOMLine below which source BOMLine objects are dropped. The find number of dropped lines is
    altered to position them after the predecessor. The find number of siblings following the pasted BOMLine objects
    may also change. Ignored if the parameter isDroppedOnTarget is true which signifies that source BOMLine objects are
    directly dropped on the target BOMLine, as a result find numbers are generated for dropped BOMLine objects and the
    BOMLine objects are position as the last children in the BOM structure.
    :var isDroppedOnTarget: Specifies whether source BOMLine objects are directly dropped on the target node. If true,
    the find numbers are generated for dropped BOMLine objects and the BOMLine objects are position as the last
    children in the BOM structure. If false, find numbers are generated so as to position them after the predecessor.
    However, in case predecessor is NULL then the find numbers are generated for dropped BOMLine objects and BOMLine
    objects are position as the first children in the BOM structure.
    :var findNumberContext: Context based on which find numbers of dropped BOMLine objects are generated. Relevant only
    if the target BOMLine is process resource of type Mfg0BvrProcessResource.
    :var isPasteDuplicate: Specifies whether the source BOMLine objects are to be cloned to the new target BOMLine
    instead of move. If true, source BOMLine objects are cloned to the target BOMLine objects. If false, the source
    BOMLine objects are moved to the target BOMLine.
    """
    sourceNodes: List[BusinessObject] = ()
    targetNode: BusinessObject = None
    predecessor: BusinessObject = None
    isDroppedOnTarget: bool = False
    findNumberContext: BusinessObject = None
    isPasteDuplicate: bool = False


@dataclass
class MoveAndResequenceResponse(TcBaseObj):
    """
    response structure for the service method moveAndResequenceNodes.
    
    :var createdICRevs: List of newly created Incremental Change (IC) revisions.
    :var createdFutureICRevs: List of newly created future IC revisions.
    :var newChildLines: The map (BOMLine, List of BOMLine) of target BOMline and the newly created or moved BOMLine
    objects under it.
    :var serviceData: The service data containing partial errors.
    """
    createdICRevs: List[WorkspaceObject] = ()
    createdFutureICRevs: List[WorkspaceObject] = ()
    newChildLines: TargetToNewChildLinesMap = None
    serviceData: ServiceData = None


"""
The map of target BOMline and the newly created or moved BOMLine objects under it.
"""
TargetToNewChildLinesMap = Dict[BusinessObject, List[BusinessObject]]
