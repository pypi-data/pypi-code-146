from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, AbsOccurrence, BusinessObject, AssemblyArrangement, PSBOMView, PSOccurrenceThread, VariantRule, RevisionRule, Dataset, Folder, CFMOverrideEntry, BOMWindow, Item, ItemRevision
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpandPSAllLevelsInfo(TcBaseObj):
    """
    Contains parent BOMLines to expand and an exclude filter to specify children to exclude.
    
    :var parentBomLines: List of parent bom lines that needs to be expanded
    :var excludeFilter: Filter to exclude the type of BOMLines.
    Valid values are: None -- Returns all information about the structure.
    ExcludeOverridden -- Excludes structure or property values that are removed by AbsOccs subsititution.
    ExcludeICHistory -- Excludes structure (or property values) that are configured out by ICs.
    ExcludeGDEs -- Excludes lines that are GDEOccurrences.
    ExcludeNonImanItemLines -- Excludes any lines that are not ImanItemLines.
    """
    parentBomLines: List[BOMLine] = ()
    excludeFilter: BOMLineFilter = None


@dataclass
class ExpandPSAllLevelsOutput(TcBaseObj):
    """
    Contains ExpandPSParentData corresponding to the parent and a list of ExpandPSData of the children
    
    :var parent: ExpandPSParentData member
    :var children: List of ExpandPSData children found for this parent.
    """
    parent: ExpandPSParentData = None
    children: List[ExpandPSData] = ()


@dataclass
class ExpandPSAllLevelsPref(TcBaseObj):
    """
    More than one filtering criteria can be specified using this which is nothing but a list of  RelationAndTypesFilter
    
    :var expItemRev: Flag to check for expanding the item revision further
    :var info: List of the relation name and the types of objects of the given relation to return along with the
    children
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter] = ()


@dataclass
class ExpandPSAllLevelsResponse(TcBaseObj):
    """
    A list of ExpandPSAllLevelsOutput so that a set of parent bom lines can be expanded.
    
    :var output: List of ExpandPSAllLevelsOutput which contains ExpandPSParentData and list of ExpandPSData
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    For this service, all objects are returned to the plain objects group.
    Error information will also be returned.
    """
    output: List[ExpandPSAllLevelsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPSData(TcBaseObj):
    """
    Through this structure, the child bom line , the item revision of the bom line and the datasets attached to the bom
    line item  revision are returned.
    
    :var bomLine: BOMline object reference of the children
    :var itemRevOfBOMLine: ItemRevision object reference of children
    :var datasets: List of Dataset object references attached to children
    """
    bomLine: BOMLine = None
    itemRevOfBOMLine: ItemRevision = None
    datasets: List[Dataset] = ()


@dataclass
class ExpandPSOneLevelInfo(TcBaseObj):
    """
    Contains parent BOMLines to expand and an exclude filter to specify children to exclude.
    
    :var parentBomLines: List of parent bom lines that needs to be expanded
    :var excludeFilter: Filter to exclude the type of BOMLines.
    Valid values are: None -- Returns all information about the structure.
    ExcludeOverridden -- Excludes structure or property values that are removed by AbsOccs subsititution.
    ExcludeICHistory -- Excludes structure that are configured out by ICs.
    ExcludeGDEs -- Excludes lines that are GDEOccurrences.
    ExcludeNonImanItemLines -- Excludes any lines that are not ImanItemLines.
    """
    parentBomLines: List[BOMLine] = ()
    excludeFilter: BOMLineFilter = None


@dataclass
class ExpandPSOneLevelOutput(TcBaseObj):
    """
    Structure containing ExpandPSParentData corresponding to the parent and a list of ExpandPSData of the children
    
    :var parent: ExpandPSParentData member
    :var children: List of ExpandPSData children found for this parent.
    """
    parent: ExpandPSParentData = None
    children: List[ExpandPSData] = ()


@dataclass
class ExpandPSOneLevelPref(TcBaseObj):
    """
    More than one filtering criteria can be specified using this which is nothing but a list of  RelationAndTypesFilter
    
    :var expItemRev: Flag to check for expanding the item revision further
    :var info: List of RelationAndTypesFilters that contain the relation names and the types of objects of the given
    relation.
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter] = ()


@dataclass
class ExpandPSOneLevelResponse(TcBaseObj):
    """
    A ExpandPSOneLevelResponse containing the return for this operation.
    
    :var output: List of ExpandPSOneLevelOutput which contains ExpandPSParentData and list of ExpandPSData
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    For this service, all objects are returned to the plain objects group. Error information will also be returned.
    """
    output: List[ExpandPSOneLevelOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPSParentData(TcBaseObj):
    """
    Through this structure, the parent bom line , the item revision of the bom line and the datasets attached to the
    bom line item revision are returned.
    
    :var bomLine: BOMline object reference of the parent
    :var itemRevOfBOMLine: ItemRevision object reference of parent
    :var parentDatasets: List of Dataset object references attached to parent
    """
    bomLine: BOMLine = None
    itemRevOfBOMLine: ItemRevision = None
    parentDatasets: List[Dataset] = ()


@dataclass
class AbsOccAttachment(TcBaseObj):
    """
    Contains a dataset object reference with the JT override data and a relationTypeName to relate AbsOccData to
    Dataset.
    
    :var dataset: Dataset object reference with the JT override data
    :var relationTypeName: Relation/property to relate AbsOccData to Dataset
    """
    dataset: Dataset = None
    relationTypeName: str = ''


@dataclass
class AssemblyArrangementInfo(TcBaseObj):
    """
    Structure with arrangement qualified override information for the occurrence.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var arrangement: The assembly arrangement object reference.  This input can be null for create, but it is required
    for update.
    :var name: The name of the arrangement.
    :var isDefault: Flag to specify whether 'arrangement' is the default arrangement.
    :var description: The arrangement description.
    :var externalUid: The UID required for create.
    :var absOccInfo: List of absolute occurrence information for the BOM view revision qualified overrides.
    """
    clientId: str = ''
    arrangement: AssemblyArrangement = None
    name: str = ''
    isDefault: bool = False
    description: str = ''
    externalUid: str = ''
    absOccInfo: List[AbsOccInfo] = ()


@dataclass
class GetRevisionRulesResponse(TcBaseObj):
    """
    Contains the response for getRevisionRules operation.
    
    :var output: List of RevisionRuleInfo which contains Revision rule, configure attribute status along with override
    information
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error
    """
    output: List[RevisionRuleInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetVariantRulesResponse(TcBaseObj):
    """
    Contains the response for getVariantRules operation.
    
    :var inputItemRevToVarRules: Holds map of itemRevision to list of VariantRules.
    :var serviceData: The ServiceData
    """
    inputItemRevToVarRules: ItemRevisionToVariantRulesMap = None
    serviceData: ServiceData = None


@dataclass
class AbsOccDataInfo(TcBaseObj):
    """
    Contains list of AttributesInfo for overrides to set, list of attribute names to unset/remove the overrides, a
    boolean flag, occTransform which contains the positioning information for the occurrence,
    list of note information for the occurrence, list of AbsOccAttachment for the attachments, list of the
    AbsOccAttachment to unattach,
    client id of the used arrangement for this absolute occurrence and a reference of used arrangement for this
    absolute occurrence.
    
    :var overridesToSet: List of AttributesInfo for overrides to set
    :var overridesToRemove: List of attribute names to unset/remove the overrides for on the occurrence, for example to
    remove a transform override, add the attribute name for the transform to this list.
    :var asRequired: Used to the set the quantity as required occurrence flag
    :var occTransform: Positioning information for the occurrence
    :var occNotes: List of note information for the occurrence
    :var attachments: List of AbsOccAttachment for the attachments
    :var attachmentsToUnattach: List of the AbsOccAttachment to unattach
    :var clientIdOfUsedArrangement: Client id of the used arrangement for this absolute occurrence, if arrangement is
    yet to be created
    :var usedArr: Reference of used arrangement for this absolute occurrence if arrangement has already been created
    """
    overridesToSet: List[AttributesInfo] = ()
    overridesToRemove: List[str] = ()
    asRequired: bool = False
    occTransform: List[float] = ()
    occNotes: List[OccNote] = ()
    attachments: List[AbsOccAttachment] = ()
    attachmentsToUnattach: List[AbsOccAttachment] = ()
    clientIdOfUsedArrangement: str = ''
    usedArr: AssemblyArrangement = None


@dataclass
class AbsOccInfo(TcBaseObj):
    """
    Attribute information for the occurrence
    
    :var clientId: Identifier that helps the client track the object(s) created
    :var absOcc: AbsOccurrence object reference , may be null for create
    :var cadOccIdPath: List of IDs of the cad occurrences
    :var absOccData: Member of AbsOccDataInfo
    """
    clientId: str = ''
    absOcc: AbsOccurrence = None
    cadOccIdPath: List[str] = ()
    absOccData: AbsOccDataInfo = None


@dataclass
class OccNote(TcBaseObj):
    """
    Contains note type and note text information for the occurrence note.
    
    :var noteType: The type of the occurrence note to set.
    :var noteText: The text for the occurrence note.
    """
    noteType: str = ''
    noteText: str = ''


@dataclass
class OverrideInfo(TcBaseObj):
    """
    This contains information about the override RevisionRule Entry.
    
    :var ruleEntry: Refers to the CFMOverrideEntry of RevisionRule object.
    :var folder: Refers to the Folder of override rule entry of RevisionRule object.
    """
    ruleEntry: CFMOverrideEntry = None
    folder: Folder = None


@dataclass
class AttributesInfo(TcBaseObj):
    """
    Name and value data to be set as attributes on the related object.
    
    :var name: The attribute name.
    :var value: The value to set for the attribute.
    """
    name: str = ''
    value: str = ''


@dataclass
class RelOccInfo(TcBaseObj):
    """
    Contains information about the relative occurrence.
    
    :var attrsToSet: Name and value pairs for the attribute information to set or update on the occurrence specified in
    the form of BOM line property names.  For example, the BOM line occurrence name property could be specified with
    the 'attrsToSet' 'name' as bl_occurrence_name and the 'value' as the occurrence name.
    :var asRequired: Flag to specify that the quantity is as required.  The default is FALSE.
    :var occTransform: Positioning information for the occurrence.  This needs to be ordered in the standard matrix
    format.
    :var occNotes: Note information for the occurrence.
    """
    attrsToSet: List[AttributesInfo] = ()
    asRequired: bool = False
    occTransform: List[float] = ()
    occNotes: List[OccNote] = ()


@dataclass
class RelationAndTypesFilter(TcBaseObj):
    """
    This consists of a string which indicates the relation name and a list of strings which indicate the object types.
    An object that falls under these input criteria is returned along with the children.
    
    :var relationName: Relation name
    :var relationTypeNames: List of the relation name types
    """
    relationName: str = ''
    relationTypeNames: List[str] = ()


@dataclass
class RelativeStructureChildInfo(TcBaseObj):
    """
    Contains clientId, cadOccId, an item revision and occurrence information structure.
    
    :var clientId: Identifier that helps the client track the object(s) created
    :var cadOccId: This is the CAD occurrence id or PSOccurrenceThread uid to uniquely identify the occurrence under a
    particular context Item Revision, can be null for create.
    A valid cadOccId must be passed when the calling the service with complete = true.
    If a valid cadOccId is not supplied when complete = true, the service creates new occurrences and any data
    associated against the old occurrence is lost.
    :var child: Item Revision for the PSOccurrence creation, required reference, if the precise flag is false, then the
    Item will be obtained from the Item Revision and used
    :var occInfo: Member of type RelOccInfo.
    """
    clientId: str = ''
    cadOccId: str = ''
    child: ItemRevision = None
    occInfo: RelOccInfo = None


@dataclass
class RevisionRuleConfigInfo(TcBaseObj):
    """
    This contains the RevisionRule object configuration information.
    
    :var clientId: Identifier that helps the client track the object(s) created
    :var revRule: The RevisionRule object used for configuration of this BOMWindow object.
    :var props: Refers to 'RevisionRuleEntryProps' struct object.
    """
    clientId: str = ''
    revRule: RevisionRule = None
    props: RevisionRuleEntryProps = None


@dataclass
class RevisionRuleEntryProps(TcBaseObj):
    """
    This contains information about the RevisionRule Entry Properties.
    
    :var unitNo: Refers to the unit number of RevisionRule object.
    :var date: Refers to the date of RevisionRule object.
    :var today: Refers to a flag to indicate that the date is today on RevisionRule object.
    :var endItem: Refers to Item and indicates end item for RevisionRule object.
    :var endItemRevision: Refers to ItemRevision and indicates end item revision for RevisionRule object.
    :var overrideFolders: Refers to a list of 'OverrideInfo' struct.
    """
    unitNo: int = 0
    date: datetime = None
    today: bool = False
    endItem: Item = None
    endItemRevision: ItemRevision = None
    overrideFolders: List[OverrideInfo] = ()


@dataclass
class RevisionRuleInfo(TcBaseObj):
    """
    Contains the revisionRule object reference, a map of string attribute to boolean flag to indicate the configurable
    and a list of override information.
    
    :var revRule: RevisionRule object reference
    :var hasValueStatus: A map of string attribute to boolean flag to indicate the configurable attribute has values on
    it and information about override folder.
    :var overrideFolders: List of override information
    """
    revRule: RevisionRule = None
    hasValueStatus: ConfigureAttrStatusMap = None
    overrideFolders: List[OverrideInfo] = ()


@dataclass
class CloseBOMWindowsResponse(TcBaseObj):
    """
    Contains a serviceData containing objects that were deleted.
    
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information. For this service, ServiceData contains BOM window and top line.
    """
    serviceData: ServiceData = None


@dataclass
class CreateBOMWindowsInfo(TcBaseObj):
    """
    main input structure that defines item or item revision of the top line in the BOM window
    
    :var clientId: Identifier that helps the client track the object(s) created
    :var item: Item object reference for which BOM window needs to create
    :var itemRev: ItemRevision object reference
    :var bomView: PSBOMView object reference
    :var revRuleConfigInfo: Structure with information about the RevisionRuleConfigInfo
    :var objectForConfigure: Tag for Variant rule or option set to use on this BOM window
    :var activeAssemblyArrangement: Active assembly arrangement of this BOM window
    """
    clientId: str = ''
    item: Item = None
    itemRev: ItemRevision = None
    bomView: PSBOMView = None
    revRuleConfigInfo: RevisionRuleConfigInfo = None
    objectForConfigure: BusinessObject = None
    activeAssemblyArrangement: AssemblyArrangement = None


@dataclass
class CreateBOMWindowsOutput(TcBaseObj):
    """
    The output structure that contains the created BOMWindow object and top line BOMLine object representing the item
    or item revision.
    
    :var clientId: Identifier that helps the client track the object(s) created
    :var bomWindow: Object reference for the BOMWindow created
    :var bomLine: Oject reference for the BOMLine created
    """
    clientId: str = ''
    bomWindow: BOMWindow = None
    bomLine: BOMLine = None


@dataclass
class CreateBOMWindowsResponse(TcBaseObj):
    """
    Contains list of CreateBOMWindowsOutput which contains created BOMWindow object and top line BOMLine object
    representing the item or item revision along with the client id and a serviceData containing objects that were
    created/deleted.
    
    :var output: List of CreateBOMWindowsOutput which contains created BOMWindow object and top line BOMLine object
    representing the item or item revision along with the client id
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information. For this service, ServiceData contains BOM window and top line.
    """
    output: List[CreateBOMWindowsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateAbsoluteStructureInfo(TcBaseObj):
    """
    Contains item revision object reference of the context assembly to create/validate the occurrence, list of
    AbsOccInfo for bvr qualified overrides and a list of AssemblyArrangementInfo for bvr/arrangement qualified
    overrides.
    
    :var contextItemRev: ItemRevision object reference of the context assembly to create/validate the occurrence,
    required reference
    :var bvrAbsOccInfo: List of AbsOccInfo for bvr qualified overrides
    :var arrAbsOccInfo: List of AssemblyArrangementInfo for bvr/arrangement qualified overrides, may be null
    """
    contextItemRev: ItemRevision = None
    bvrAbsOccInfo: List[AbsOccInfo] = ()
    arrAbsOccInfo: List[AssemblyArrangementInfo] = ()


@dataclass
class CreateOrUpdateAbsoluteStructurePref(TcBaseObj):
    """
    Contain cadOccIdAttrName which identifies the BOMLine attribute that is used to identify relative occurrences to
    update.
    
    :var cadOccIdAttrName: Identifies the BOMLine attribute that is used to identify relative occurrences to update.
    """
    cadOccIdAttrName: str = ''


@dataclass
class CreateOrUpdateAbsoluteStructureResponse(TcBaseObj):
    """
    Contains response for createOrUpdateAbsoluteStructure operation.
    
    :var absOccOutput: Map of input clientId for the absolute occurrence to created/updated/found absolute occurrence
    :var asmArrOutput: Map of input client id to created/updated/found AssemblyArrangement
    :var serviceData: The ServiceData contains any other created (AbsOccData, AbsOccDataQualifier), updated (like BVR),
    relevant related, or deleted objects from this operation.
    """
    absOccOutput: ClientIdToAbsOccMap = None
    asmArrOutput: ClientIdToAsmArrMap = None
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateRelativeStructureInfo(TcBaseObj):
    """
    Contains a parent ItemRevision object, list of type RelativeStructureChildInfo and a boolean value for whether the
    BVR should be set to precise.
    
    :var parent: ItemRevision object reference for which the context assembly is created or updated, required reference
    :var childInfo: List of type RelativeStructureChildInfo
    :var precise: Flag for updating the BVR to precise(true)/imprecise(false)
    """
    parent: ItemRevision = None
    childInfo: List[RelativeStructureChildInfo] = ()
    precise: bool = False


@dataclass
class CreateOrUpdateRelativeStructurePref(TcBaseObj):
    """
    Contains cadOccIdAttrName and a list of item types.
    
    :var cadOccIdAttrName: String representing the occurrence note type which holds the value for the CAD occurrence id
    or PSOccurrenceThread uid
    :var itemTypes: List of item types that the client is interested in, such that if the overall structure in
    Teamcenter contains structure relating to other item types or subtypes not in this list, that structure will not be
    deleted if this operation is complete.
    """
    cadOccIdAttrName: str = ''
    itemTypes: List[str] = ()


@dataclass
class CreateOrUpdateRelativeStructureResponse(TcBaseObj):
    """
    The response for createOrUpdateRelativeStructure operation.
    
    :var output: Member of type ClientIdToPSOccurrenceThreadMap
    :var serviceData: Mwmber of type Teamcenter::Soa::Server::ServiceData serviceData
    """
    output: ClientIdToPSOccurrenceThreadMap = None
    serviceData: ServiceData = None


@dataclass
class DeleteAssemblyArrangementsInfo(TcBaseObj):
    """
    Contains ItemRevision object reference and list of AssemblyArrangement.
    
    :var itemRev: ItemRevision object reference
    :var arrangements: List of AssemblyArrangement object references to be deleted
    """
    itemRev: ItemRevision = None
    arrangements: List[AssemblyArrangement] = ()


@dataclass
class DeleteAssemblyArrangementsResponse(TcBaseObj):
    """
    The response for the 'deleteAssemblyArrangements' operation.
    
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' with deleted assembly
    arrangements. Assembly arrangement UIDs will be returned as deleted objects.
    """
    serviceData: ServiceData = None


@dataclass
class DeleteRelativeStructureInfo(TcBaseObj):
    """
    Contains parent item revision and list of child information structures.
    
    :var parent: ItemRevision object reference for the context assembly from which children are to be removed
    :var childInfo: List of identifiers of the relative occurrences to be deleted. This is the CAD occurrence id or
    PSOccurrenceThread uid to uniquely identify the occurrence under a particular context Item Revision
    """
    parent: ItemRevision = None
    childInfo: List[str] = ()


@dataclass
class DeleteRelativeStructurePref(TcBaseObj):
    """
    Contains cadOccIdAttrName.
    
    :var cadOccIdAttrName: BOMLine attribute name that contains the CAD occurrence identifier.
    """
    cadOccIdAttrName: str = ''


@dataclass
class DeleteRelativeStructureResponse(TcBaseObj):
    """
    The response for 'deleteRelativeStructure' operation.
    
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData 'with updated context BVR
    objects and the deleted relative occurrences. CAD occurrence IDs or PSOccurrenceThread UIDs will be returned as
    deleted objects.
    """
    serviceData: ServiceData = None


class BOMLineFilter(Enum):
    """
    BOMLineFilter. 
    Legal values are :  'None, ExcludeOverridden, ExcludeICHistory, ExcludeGDEs, ExcludeNonImanItemLines'.
    """
    None_ = 'None'
    ExcludeOverridden = 'ExcludeOverridden'
    ExcludeICHistory = 'ExcludeICHistory'
    ExcludeGDEs = 'ExcludeGDEs'
    ExcludeNonImanItemLines = 'ExcludeNonImanItemLines'


"""
ItemRevisionToVariantRulesMap
"""
ItemRevisionToVariantRulesMap = Dict[ItemRevision, List[VariantRule]]


"""
ClientIdToAbsOccMap
"""
ClientIdToAbsOccMap = Dict[str, AbsOccurrence]


"""
ClientIdToAsmArrMap
"""
ClientIdToAsmArrMap = Dict[str, AssemblyArrangement]


"""
ClientIdToPSOccurrenceThreadMap
"""
ClientIdToPSOccurrenceThreadMap = Dict[str, PSOccurrenceThread]


"""
ConfigureAttrStatusMap
"""
ConfigureAttrStatusMap = Dict[str, bool]
