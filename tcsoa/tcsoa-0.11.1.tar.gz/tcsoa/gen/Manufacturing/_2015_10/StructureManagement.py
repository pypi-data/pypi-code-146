from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CloningStructsInfo(TcBaseObj):
    """
    Contains BOMLine objects which are to be cloned in CPC along with additional cloning information.
    
    :var newName: The name of new structure to be created as a cloned structure in CPC.
    :var newDescription: The description of new structure to be created as a cloned structure in CPC.
    :var newId: ID of new structure to be created as a cloned structure in CPC.
    :var newRevId: The revision ID of new structure to be created as a cloned structure in CPC.
    :var scopes: The list of  BOMLine objects to be cloned in CPC. It can be either root BOMLine or multiple BOMLine
    objects within the same structure.
    :var cloningRule: The rule used for cloning. The value varies based on the structure type which is getting cloned.
    For example, the acceptable value for Mfg0MEPlantBOP is  "ProjectPlantBOPTemplate".
    :var cloningParams: A map (string, string) containing cloning parameter as key and its flag as the value, such as 
    ("CPC_carryOverICs","true") for carry over Increamental Changes. Other cloning parameters are
    "CPC_cloneSupressLine" and "CPC_createDIPA" for clone suppressed lines and create Dynamic In-Process Assembly
    (DIPA) respectively.
    """
    newName: str = ''
    newDescription: str = ''
    newId: str = ''
    newRevId: str = ''
    scopes: List[BusinessObject] = ()
    cloningRule: str = ''
    cloningParams: CloningParams = None


@dataclass
class CreateCPCInputInfo(TcBaseObj):
    """
    A list of BOMLine objects  that are to be cloned and\or referred, cloning information, name and description of new
    CPC.
    
    :var cloningStructsInfo: A list of CloningStructureInfo which contains BOMLine objects which are to be cloned in
    CPC. The structure contains additional cloning information as well.
    :var releaseStatus: The release status which gets associated with line(s) in the cloned structure. If the line(s)
    doesn't have any release status in the original structure. It is configurable but in this version only acceptable
    value is "Alternate Planning Initial".
    :var effectivityInfo: The information required to set effectivity for a list of cloned BOMLine objects.
    :var originalCCUid: The UID of the MECollaborationContext from which CPC is to be created.
    :var cpcName: Name of the CPC to be created.
    :var cpcDesc: Description of the CPC to be created.
    :var refStructures: List of  BOMLine objects from the original CC that are going to be referred in the CPC.
    """
    cloningStructsInfo: List[CloningStructsInfo] = ()
    releaseStatus: str = ''
    effectivityInfo: EffectivityInfoInput = None
    originalCCUid: BusinessObject = None
    cpcName: str = ''
    cpcDesc: str = ''
    refStructures: List[BusinessObject] = ()


@dataclass
class CreateCPCResponse(TcBaseObj):
    """
    Contains newly created CPC data.
    
    :var cpcObject: The created CPC object.
    :var serviceData: The Service Data
    """
    cpcObject: BusinessObject = None
    serviceData: ServiceData = None


@dataclass
class EffectivityInfoInput(TcBaseObj):
    """
    The information required to set effectivity for a list of cloned BOMLine objects.
    
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
    June 2015 and end date 22nd June 2015, the dataRange list have 4 values as below : 2015-02-19, 2015-05-22,
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


"""
Map of the cloning parameters. The key of the map is cloning parameter and its value is a flag.
"""
CloningParams = Dict[str, str]
