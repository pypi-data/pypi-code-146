from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ChangeItemRevision, BOMEdit, PSBOMViewRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetNoteVariantOutput(TcBaseObj):
    """
    'GetNoteVariantOutput' structure contains object references to 1) the BOMEdit, 2) the associated change revision,
    3) the solution bvr, and 4) the impacted bvr.  It also contains a list of details count and a list of strings
    representing some textual details of the note or variant change.
    
    :var bomChange: An object reference to a BOMEdit
    :var changeRev: An object reference to a change revision.
    :var solutionBVR: An object reference to the Solution bvr.
    :var impactedBVR: An object reference to the Impacted bvr.
    :var vCount: Count of note or variant change details
    :var vBomChangeDetails: Note or variant change details.
    """
    bomChange: BOMEdit = None
    changeRev: ChangeItemRevision = None
    solutionBVR: PSBOMViewRevision = None
    impactedBVR: PSBOMViewRevision = None
    vCount: List[int] = ()
    vBomChangeDetails: List[str] = ()


@dataclass
class GetNoteVariantResponse(TcBaseObj):
    """
    'GetNoteVariantResponse' structure contains a list of 'GetNoteVariantOutput' structures and a standard service data.
    
    :var output: A reference to the list of GetNoteVariantOutput
    :var serviceData: Standard Service data.
    """
    output: List[GetNoteVariantOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetNoteVariantsInput(TcBaseObj):
    """
    GetNoteVariantsInput structure contains an object reference to a BOMEdit whose integer type is EITHER 6 (=Note
    Change) OR 7(=Variant Change) and a matching context string.
    
    :var bomChangeNode: An object reference to a BOMEdit
    :var contextRelName: A context string of two possible values: CM_note_change_details or CM_variant_change_details.
    """
    bomChangeNode: BusinessObject = None
    contextRelName: str = ''
