from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, VariantRule, RevisionRule, StructureContext, ApprSearchCriteriaGroup, Item, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class StructureCntxtObjectInfo(TcBaseObj):
    """
    This structure contains the information required to create or update the SCO.
    
    :var prdItemRevision: Product Item Revision used during performing the search.
    :var revRule: Revision Rule used during performing the search. For e.g, 'Latest working'.
    :var varRule: Variant Rule set while performing the search.
    :var workParts: List of work parts selected from DesignContext(DC) UserInterface(UI).
    :var tgtBomLines: List of all the Target BOMLine objects selected in DC UI.
    :var bgdBomLines: List of Background BOMLine objects returned by the search.
    :var selTgtBomLines: List of selected Target BOMLine objects used. This is used for storing     the selections.
    :var selBgdBomLines: List of selected Background BOMLine objects. This is used for storing the selections.
    :var tgtSearchCrtGrp: Object of Appearance Search Criteria Group for Target.
    :var bgdSearchCrtGrp: Object of Appearance Search Criteria Group for Background.
    """
    prdItemRevision: ItemRevision = None
    revRule: RevisionRule = None
    varRule: VariantRule = None
    workParts: List[Item] = ()
    tgtBomLines: List[BOMLine] = ()
    bgdBomLines: List[BOMLine] = ()
    selTgtBomLines: List[BOMLine] = ()
    selBgdBomLines: List[BOMLine] = ()
    tgtSearchCrtGrp: ApprSearchCriteriaGroup = None
    bgdSearchCrtGrp: ApprSearchCriteriaGroup = None


@dataclass
class UpdateSCOInputInfo(TcBaseObj):
    """
    This structure contains the StructureContext object and 'StructureCntxtObjectInfo' object containing information
    that needs to be updated.
    
    :var strCntxtObject: Structure Context Object that needs to be updated. This SCO object will be updated with the
    modified values.
    :var scoInfo: Object of 'StructureCntxtObjectInfo' structure. It internally holds all the details related to the
    search criteria and search results.
    """
    strCntxtObject: StructureContext = None
    scoInfo: StructureCntxtObjectInfo = None


@dataclass
class UpdateSCOResponse(TcBaseObj):
    """
    This structure contains the updated StructureContext object and error, if any, in serviceData object.
    
    :var strCntxtObject: Object of StructureContext updated with the values supplied through the input parameter.
    :var serviceData: Contains any exceptions if occurred during updation of SCOs.
    """
    strCntxtObject: StructureContext = None
    serviceData: ServiceData = None


@dataclass
class CreateSCOInputInfo(TcBaseObj):
    """
    This structure specifies the type, name and description information of a SCO object.
    
    :var scoType: Type of the Structure Context Object. For e.g. VisStructureContext.
    :var scoName: Name by which the StructureContext Object will be created.
    :var scoDesc: Description provided while creating the StructureContext object in DC UI.
    :var scoInfo: 'StructureCntxtObjectInfo' object which contains all the details related to the search criteria and
    search results.
    """
    scoType: str = ''
    scoName: str = ''
    scoDesc: str = ''
    scoInfo: StructureCntxtObjectInfo = None


@dataclass
class CreateSCOResponse(TcBaseObj):
    """
    This structure contains newly created StructureContext object and 'ServiceData' object
    
    :var strCntxtObject: Object of StructureContext created newly using the values passed in the     input parameter.
    This object encapsulates complete DesignContext session information.
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during creation of SCO.
    """
    strCntxtObject: StructureContext = None
    serviceData: ServiceData = None
