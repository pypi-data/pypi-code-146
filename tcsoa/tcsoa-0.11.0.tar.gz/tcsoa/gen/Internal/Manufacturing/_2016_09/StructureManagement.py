from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_10.StructureManagement import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AsyncCloningStructsInfo(TcBaseObj):
    """
    A list of AsyncCloningStructsInfo which contains VisStructureContext objects which are to be cloned in CPC. The
    structure contains additional cloning information as well.
    
    :var newName: The name of new structure to be created as a cloned structure in CPC.
    :var newDescription: The description of new structure to be created as a cloned structure in CPC.
    :var newId: Id of new structure to be created as a cloned structure in CPC.
    :var newRevId: The revision id of new structure to be created as a cloned structure in CPC.
    :var scopes: The list of  VisStructureContext objects to be cloned in CPC. It can be either root
    VisStructureContext object or multiple VisStructureContext objects within the same structure.
    :var cloningRule: The rule used for cloning. The value varies based on the structure type which is getting cloned.
    For example, the acceptable value for Mfg0MEPlantBOP is "ProjectPlantBOPTemplate".
    :var cloningParams: A map (string, string) representing cloning parameter and its value, such as
    ("CPC_carryOverICs","true") for carry over Incremental Changes. Other cloning parameters are "CPC_cloneSupressLine"
    and "CPC_createDIPA" for clone suppressed lines and create Dynamic In-Process Assembly (DIPA) respectively.
    """
    newName: str = ''
    newDescription: str = ''
    newId: str = ''
    newRevId: str = ''
    scopes: List[BusinessObject] = ()
    cloningRule: str = ''
    cloningParams: AsyncCloningParams = None


@dataclass
class AsyncCreateCPCInputInfo(TcBaseObj):
    """
    The input to the service operation is a structure which contains a list of VisStructureContext objects;  which are
    to be cloned and\or referred, cloning information, name and description of new CPC.
    
    :var cloningStructsInfo: A list of AsyncCloningStructsInfo which contains VisStructureContext objects which are to
    be cloned in CPC. The structure contains additional cloning information as well.
    :var releaseStatus: It contains the release status which gets associated with line(s) in the cloned structure if
    the line(s) doesn't have any release status in the original structure. The preference
    MEAlternativeDefaultReleaseStatus specifies the valid values.
    :var effectivityInfo: The information required to set effectivity for a list of cloned BOMLine objects.
    :var originalCCUid: The uid of the MECollaborationContext from which CPC is to be created.
    :var cpcName: Name of the CPC to be created.
    :var cpcDesc: Description of the CPC to be created.
    :var refStructures: List of VisStructureContext objects from the original CC that are going to be referred in the
    CPC.
    """
    cloningStructsInfo: List[AsyncCloningStructsInfo] = ()
    releaseStatus: str = ''
    effectivityInfo: AsyncEffectivityInfoInput = None
    originalCCUid: BusinessObject = None
    cpcName: str = ''
    cpcDesc: str = ''
    refStructures: List[BusinessObject] = ()


@dataclass
class AsyncEffectivityInfoInput(TcBaseObj):
    """
    The information required to set effectivity for a list of cloned BOMLine objects. Same as EffectivityInfoInput data
    type used in (createCollabPlanningContext) synchronous operation.
    
    :var endItem: Effectivity end Item.
    :var endItemRev: Effectivity end ItemRevision.
    :var unitRangeText: Effectivity unit range, for example "5-10". Multiple range can also be provided, for example
    "3,5-10,20-50". This range belongs to the end Item which is part of the structrue on which the unit effectivity is
    applied.
    Valid unit ranges are:
     -StartUnit
    -StartUnit - EndUnit
    -StartUnit - SO
    -StartUnit - UP
            where, StartUnit <= EndUnit 
    -StartUnit1 - EndUnit1, StartUnit2 - EndUnit2(Ex: 10 - 12, 15, 16 - UP)
            where StartUnit2 > EndUnit1.
    - All units are positive integers
    
    For example, the effectivity can be 3 - 5 where 3 is start unit and 5 is end unit.
    It can also be 3 - UP where 3 is start unit and "UP" means anything above the start unit. "UP" and "SO" indicates
    open ended effectivity.  "SO" is stock out means effectivity will be applicable till the stock out condition.
    :var dateRange: The list of effectivity date range. For instance, opened date range could be specified as "05 Jan -
    UP" and closed date range as "01 Jan - 03 Apr". The list may have any number of opened and closed date range. For
    example, If you select multiple dates such as start date 19th May 2015 and End date 22nd May 2015 , start date 19th
    June 2015 and end date 22nd June 2015, the date Range list have 4 values as below : 2015-02-19, 2015-05-22,
    2015-06-19,2015-06-22.
    :var openEndedStatus: Effectivity open ended status.
    - 0 : for closed unit range effectivity or date effectivity.
    - 1 : for opened unit range effectivity or date effectivity (UP).
    - 2 : for opened unit range effectivity or date effectivity stock out (SO).
    For example, if you select open ended effectivity such as start date 19th May 2015 and end date "UP", the dateRange
    list has 2015-05-19 with "openEndedStatus" value as "1".
    """
    endItem: Item = None
    endItemRev: ItemRevision = None
    unitRangeText: str = ''
    dateRange: List[datetime] = ()
    openEndedStatus: int = 0


@dataclass
class LinkStructuresInput(TcBaseObj):
    """
    This operation links or unlinks the BOMViews of the toplines of the two input structures by the given relation.
    
    :var sourceLine: The BOMLine of the source structure to be linked.
    :var targetLine: The BOMLine of the target structure to be linked.
    :var relationName: The name of the relation to link the structures.
    :var link: True to link structures, False to unlink structures.
    """
    sourceLine: BusinessObject = None
    targetLine: BusinessObject = None
    relationName: str = ''
    link: bool = False


@dataclass
class LinkStructuresResponse(TcBaseObj):
    """
    Response to hold linked structures.
    
    :var serviceData: The updated objects element will contain the connected PSBOMView objects. May also contain
    partial errors.
    :var additionalInfo: Future use
    """
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class ObjectAlignmentInput(TcBaseObj):
    """
    A list of ObjectAlignmentInput objects specifying the input structures.
    
    :var inputLine: The  line of structure to process.
    :var additionalInfo: Reserved for future use.
    """
    inputLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class CompletenessCheckPartStructureResp(TcBaseObj):
    """
    Returns complete lines, incomplete lines and reasons for incomplete lines.
    
    :var completeLines: The list of BOMLline objects which are complete.
    :var incompleteLines: The list of BOMLine objects  which are evaluated as incomplete.
    :var incompleteLinesReason: The reasons the line is incomplete.A comma delimited string of reasons. Same size as
    incompleteLines.
    :var serviceData: Partial Errors
    :var additionalInfo: Reserved for future use.
    """
    completeLines: BusinessObject = None
    incompleteLines: BusinessObject = None
    incompleteLinesReason: str = ''
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class CreateDesignPartAlignmentInput(TcBaseObj):
    """
    List of CreateDesignPartAlignmentInput which specifies Design BOMLine, Part BOMLine and align mode .
    
    :var designLine: The Design BOMLine for alignment.
    :var partLine: The Part BOMLine for alignment.
    :var alignMode: The string representing align mode is "AssignDesign" | "NoAssign"
    :var additionalInfo: Future use.
    """
    designLine: BusinessObject = None
    partLine: BusinessObject = None
    alignMode: str = ''
    additionalInfo: AdditionalInfo = None


@dataclass
class DesignPartAlignmentInput(TcBaseObj):
    """
    Specifies Design and Part objects to verify.
    
    :var designLine: The input Design BOMLine. (Optional)
    :var partLine: The Part BOMLine. If no Design exist the service will issue an error.
    :var additionalInfo: Reserved for future use.
    """
    designLine: BusinessObject = None
    partLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class DesignPartAlignmentResponse(TcBaseObj):
    """
    Returns service objects or partial errors.
    
    :var serviceData: Updated objects and partial error information.
    :var additionalInfo: Future use.
    """
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


"""
A map (string, string) of the cloning parameters representing cloning parameter and its value. Same as CloningParams data type used in (createCollabPlanningContext) synchronous operation.
"""
AsyncCloningParams = Dict[str, str]
