from __future__ import annotations

from tcsoa.gen.Cad._2007_01.StructureManagement import AbsOccInfo, RelativeStructureChildInfo, AssemblyArrangementInfo
from tcsoa.gen.BusinessObjects import BOMLine, AssemblyArrangement, ItemRevision
from tcsoa.gen.Cad._2007_06.StructureManagement import ClassicOptionInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Cad._2007_09.StructureManagement import VariantCondInfo
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BomLineVariantCondition(TcBaseObj):
    """
    This contains the variant condition information for a given BOMLine object.
    
    :var bomLine: Refers to BOMLine object on which variant condition are defined.
    :var conditionClauses: Refers to a list of VariantCondInfo struct objects which has classic variant condition
    information.
    """
    bomLine: BOMLine = None
    conditionClauses: List[VariantCondInfo] = ()


@dataclass
class VariantConditionResponse(TcBaseObj):
    """
    This contains the variant condition information for a set of BOMLine objects.
    
    :var variantConditions: Refers to a list of 'BomLineVariantCondition' struct objects, contains the variant
    condition on BOMLine object.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    """
    variantConditions: List[BomLineVariantCondition] = ()
    serviceData: ServiceData = None


@dataclass
class ClassicOptionData(TcBaseObj):
    """
    Contains the option information for a single item revision.
    
    :var itemRevision: itemRevision
    :var optionData: optionData
    """
    itemRevision: ItemRevision = None
    optionData: List[ClassicOptionInfo] = ()


@dataclass
class ClassicOptionsResponse(TcBaseObj):
    """
    Contains the option information for a set of ItemRevision objects.
    
    :var itemRevisionOptionData: Refers to a list of 'ClassicOptionData' struct, which has ItemRevision and
    corresponding classic variant option list.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the service
    operation, plain objects, and error information.
    """
    itemRevisionOptionData: List[ClassicOptionData] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateAbsoluteStructureInfo2(TcBaseObj):
    """
    Contains Last Modified Date of BVR, contextItemRev, List of AbsOccInfo for bvr qualified overrides and a list of
    AssemblyArrangementInfo for bvr/arrangement qualified overrides.
    
    :var lastModifiedOfBVR: Last Modified Date of BVR
    :var contextItemRev: ItemRevision object reference of the context assembly to create/validate the occurrence,
    required reference
    :var bvrAbsOccInfo: List of AbsOccInfo for bvr qualified overrides
    :var arrAbsOccInfo: List of AssemblyArrangementInfo for bvr/arrangement qualified overrides, may be null
    """
    lastModifiedOfBVR: datetime = None
    contextItemRev: ItemRevision = None
    bvrAbsOccInfo: List[AbsOccInfo] = ()
    arrAbsOccInfo: List[AssemblyArrangementInfo] = ()


@dataclass
class CreateOrUpdateAbsoluteStructurePref2(TcBaseObj):
    """
    Contains a flag to check whether BVR needs to be modified, if input last modified date is different from actual and
    a cadOccIdAttrName which identifies the BOMLine attribute that is used to identify relative occurrences to update.
    
    :var overwriteForLastModDate: Flag to check whether BVR needs to be modified, if input last modified date is
    different from actual.
    :var cadOccIdAttrName: Identifies the BOMLine attribute that is used to identify relative occurrences to update.
    """
    overwriteForLastModDate: bool = False
    cadOccIdAttrName: str = ''


@dataclass
class CreateOrUpdateRelativeStructureInfo2(TcBaseObj):
    """
    Contains lastModifiedOfBVR, a parent ItemRevision object, list of type RelativeStructureChildInfo and a  boolean
    value to convey precision of the BVR.
    
    :var lastModifiedOfBVR: Last Modified Date of BVR
    :var parent: ItemRevision object reference for which the context assembly is created or updated, required reference
    :var childInfo: List of type RelativeStructureChildInfo
    :var precise: Flag for updating the BVR to precise(true)/imprecise(false)
    """
    lastModifiedOfBVR: datetime = None
    parent: ItemRevision = None
    childInfo: List[RelativeStructureChildInfo] = ()
    precise: bool = False


@dataclass
class CreateOrUpdateRelativeStructurePref2(TcBaseObj):
    """
    Contains overwriteForLastModDate, cadOccIdAttrName and a list of item types.
    
    :var overwriteForLastModDate: Flag to check whether BVR needs to be modified, if input last modified date is
    different from actual.
    :var cadOccIdAttrName: String representing the occurrence note type which holds the value for the CAD occurrence id
    or PSOccurrenceThread uid
    :var itemTypes: List of item types that the client is interested in, such that if the overall structure in
    Teamcenter contains structure relating to other item types or subtypes not in this list,
    that structure will not be deleted if this operation is complete.
    """
    overwriteForLastModDate: bool = False
    cadOccIdAttrName: str = ''
    itemTypes: List[str] = ()


@dataclass
class DeleteAssemblyArrangementsInfo2(TcBaseObj):
    """
    Information to delete assembly arrangements.
    
    :var lastModifiedOfBVR: Last modified date of BOM view revision object under the input 'itemRev'.  This input is
    not required.  If this input date is different than the current last modified date and the
    'overwriteForLastModDate' preference is false the input will be ignored and processing will continue with the next
    input.  In this scenario, error 215033 will be returned.  If the dates are different and the
    'overwriteForLastModDate' preference is true, processing will continue with the current input, the BVR will be
    modified and the arrangements deleted.  In this scenario, error 215034 will be returned.
    :var itemRev: Object reference of the item revision context assembly from which the assembly arrangements are to be
    removed.  This is a required input.  An error will be returned if a valid 'itemRev' is not specified.
    :var arrangements: List of assembly arrangement object references to be deleted.
    """
    lastModifiedOfBVR: datetime = None
    itemRev: ItemRevision = None
    arrangements: List[AssemblyArrangement] = ()


@dataclass
class DeleteAssemblyArrangementsPref(TcBaseObj):
    """
    Preference structure for 'deleteAssemblyArrangements'.
    
    :var overwriteForLastModDate: Flag to check whether the structure needs to be updated if the input last modified
    date is different from the current last modified date of the object in Teamcenter.  If false, but the
    'DeleteAssemblyArrangementsInfo2' 'lastModifiedOfBVR' input specified is different than the set modified date,
    partial error 215033 will be returned.
    """
    overwriteForLastModDate: bool = False


@dataclass
class DeleteRelativeStructureInfo2(TcBaseObj):
    """
    Contains lastModifiedOfBVR, parent itemRevision and childInfo.
    
    :var lastModifiedOfBVR: Last Modified Date of BVR
    :var parent: ItemRevision object reference for the context assembly from which children are to be removed
    :var childInfo: List of identifiers of the relative occurrences to be deleted. This is the CAD occurrence id or
    PSOccurrenceThread uid to uniquely identify the occurrence under a particular context Item Revision.
    """
    lastModifiedOfBVR: datetime = None
    parent: ItemRevision = None
    childInfo: List[str] = ()


@dataclass
class DeleteRelativeStructurePref2(TcBaseObj):
    """
    Preference structure for 'deleteRelativeStructure'.
    
    :var overwriteForLastModDate: Flag to check whether the structure needs to be updated if the input last modified
    date is different from the current last modified date of the object in Teamcenter.  If false, but the
    'DeleteRelativeStructureInfo3' 'lastModifiedOfBVR' input specified is different than the set modified date, partial
    error 215033 will be returned.
    :var cadOccIdAttrName: The BOMLine attribute that contains the CAD occurrence identifier.
    """
    overwriteForLastModDate: bool = False
    cadOccIdAttrName: str = ''
