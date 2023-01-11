from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, AbsOccurrence, BusinessObject, AbsOccData, AssemblyArrangement, PSOccurrenceThread, VariantRule, PSBOMViewRevision, Dataset, MEAppearancePathNode, BOMWindow, Form, ItemRevision
from tcsoa.gen.Cad._2007_01.StructureManagement import AttributesInfo, RevisionRuleConfigInfo, OccNote, RelationAndTypesFilter, AssemblyArrangementInfo, RelOccInfo
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpandPSAllLevelsInfo(TcBaseObj):
    """
    Contains parentBomLines & excludeFilter.
    
    :var parentBomLines: List of parent bom lines that needs to be expanded
    :var excludeFilter: Filter to exclude the type of BOMLines.
    Valid values are:
    None2 -- Returns all information about the structure.
    ExcludeOverridden2 -- Excludes structure or property values that are removed by AbsOccs substitution.
    ExcludeICHistory2 -- Excludes structure (or property values) that are configured out by ICs.
    ExcludeGDEs2 -- Excludes lines that are GDEOccurrences.
    ExcludeImanItemLines2 -- Excludes any lines that are ImanItemLines.
    """
    parentBomLines: List[BOMLine] = ()
    excludeFilter: BOMLineFilter2 = None


@dataclass
class ExpandPSAllLevelsOutput(TcBaseObj):
    """
    Structure containing ExpandPSParentData2 corresponding to the parent and a list of ExpandPSData of the children
    
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
    :var includeOccurrenceTypes: List of Occurrence Types that needs to be included when the expansion of the BOM takes
    place.
    :var excludeOccurrenceTypes: List of Occurrence Types that needs to be excluded when the expansion of the BOM takes
    place.
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter] = ()
    includeOccurrenceTypes: List[str] = ()
    excludeOccurrenceTypes: List[str] = ()


@dataclass
class ExpandPSAllLevelsResponse2(TcBaseObj):
    """
    A list of ExpandPSAllLevelsOutput2 so that a set of parent BOMLines can be expanded.
    
    :var output: List of ExpandPSAllLevelsOutput1 which contains ExpandPSParentData and list of ExpandPSData
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    For this service, all objects are returned to the plain objects group.
    Error information will also be returned mapped to input object.
    """
    output: List[ExpandPSAllLevelsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPSData(TcBaseObj):
    """
    Through this structure, the child bom line , the object of the bom line and the object attached to the bom line
    object are returned.
    
    :var bomLine: BOMline object reference of the children
    :var objectOfBOMLine: Object that the child represents
    :var relatedObjects: List of objects attached to children with given relation
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    relatedObjects: List[ExpandPSRelatedObjectInfo] = ()


@dataclass
class ExpandPSNamedReferenceInfo(TcBaseObj):
    """
    This structure is used to identify the reference object corresponding to the named reference.
    
    :var namedReferenceType: type of reference object.
    :var namedReferenceName: name of reference object.
    :var referenceObject: Object reference corresponding to the named reference.
    :var fileTicket: FMS ticket used to retrieve the file in cases where referenceObject is a file.
    """
    namedReferenceType: str = ''
    namedReferenceName: str = ''
    referenceObject: BusinessObject = None
    fileTicket: str = ''


@dataclass
class ExpandPSOneLevelInfo(TcBaseObj):
    """
    Contains the parent BOM lines whose children are to be expanded.
    
    :var parentBomLines: List of parent BOM lines to be expanded.
    :var excludeFilter: A filter used to identify the type of BOM lines to exclude.
    Valid values are: None2 -- Returns all information about the structure.
    ExcludeOverridden2 -- Excludes structure or property values that are removed by AbsOccs subsititution.
    ExcludeICHistory2 -- Excludes structure that are configured out by ICs.
    ExcludeGDEs2 -- Excludes lines that are GDEOccurrences.
    ExcludeImanItemLines2 -- Excludes lines that are ImanItemLines.
    """
    parentBomLines: List[BOMLine] = ()
    excludeFilter: BOMLineFilter2 = None


@dataclass
class ExpandPSOneLevelOutput(TcBaseObj):
    """
    Used to return a parent bomline and its related data, and a list of bomlines and related data that share that
    parent.
    
    :var parent: parent data member
    :var children: list of children returned for the parent
    """
    parent: ExpandPSParentData = None
    children: List[ExpandPSData] = ()


@dataclass
class ExpandPSOneLevelPref(TcBaseObj):
    """
    Contains a list of filtering criteria (RelationAndTypesFilter) used in a product structure expand operation.
    
    :var expItemRev: Flag indicating whether to return related object(s).
    :var info: List of the relation name and the related object types to return along with the children.  If no
    RelationAndTypesFilter is supplied (info is empty), and expItemRev is true, then all related object types are to be
    accepted.
    :var includeOccurrenceTypes: List of Occurrence Types that needs to be included when the expansion of the BOM takes
    place.
    :var excludeOccurrenceTypes: List of Occurrence Types that needs to be excluded when the expansion of the BOM takes
    place.
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter] = ()
    includeOccurrenceTypes: List[str] = ()
    excludeOccurrenceTypes: List[str] = ()


@dataclass
class ExpandPSOneLevelResponse2(TcBaseObj):
    """
    Is the response object returned in a product structure one level expand operation.
    
    :var output: List of ExpandPSOneLevelOutput structures.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    For this service, all objects are returned to the plain objects group.
    Error information will also be returned.
    """
    output: List[ExpandPSOneLevelOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPSParentData(TcBaseObj):
    """
    Through this structure, the parent bom line , the object of the bom line and the objects attached to the bom line
    object are returned.
    
    :var bomLine: BOMline object reference of the parent
    :var objectOfBOMLine: Object that the parent represents
    :var parentRelatedObjects: List of object references attached to parent with given relation
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    parentRelatedObjects: List[ExpandPSRelatedObjectInfo] = ()


@dataclass
class ExpandPSRelatedObjectInfo(TcBaseObj):
    """
    This structure associates a related object, named references and reference objects.
    
    :var relatedObject: The resulting related object by following a relation specified in the ExpandPSOneLevelPref
    :var namedRefList: List of named reference and reference object of relatedObject.
    """
    relatedObject: BusinessObject = None
    namedRefList: List[ExpandPSNamedReferenceInfo] = ()


@dataclass
class ApnToThreadPathStruct(TcBaseObj):
    """
    Contains the appearance path node and the occurrence thread path corresponding to the apn.
    
    :var apn: The appearance path node
    :var occThreadPath: The occurrence thread path corresponding to the apn
    """
    apn: MEAppearancePathNode = None
    occThreadPath: List[PSOccurrenceThread] = ()


@dataclass
class FormInfo(TcBaseObj):
    """
    Form information for the occurrence.
    
    :var formObject: The form object reference.  This input can be null for create, but it is required for update.
    :var name: The form name attribute value.
    :var description: The form description attribute value.
    :var formType: The form type name.
    :var attributes: The attributes to be set or updated on the form.
    """
    formObject: Form = None
    name: str = ''
    description: str = ''
    formType: str = ''
    attributes: List[NameValueStruct] = ()


@dataclass
class GetAbsoluteStructureDataResponse(TcBaseObj):
    """
    Contains list of overrides and serviceData.
    
    :var overrides: List of overrides
    :var serviceData: Contains populated plain object list and partial errors.
    """
    overrides: List[AbsOccStructureDataInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AbsOccAttachment2(TcBaseObj):
    """
    Contains an override object which is attached as the override data and a 'relationTypeName' to relate the
    'AbsOccData' to the object.
    
    :var overrideObject: The object which is attached as the override data.
    :var relationTypeName: Relation name or property name to relate 'AbsOccData' to object.
    """
    overrideObject: BusinessObject = None
    relationTypeName: str = ''


@dataclass
class AbsOccCreateDatasetAttachmentInfo(TcBaseObj):
    """
    Dataset information for attaching a dataset to the absolute occurrence.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var datasetInfo: The information used to create or update the dataset.
    :var relationTypeName: The relation type used for the dataset attached to the absolute occurrence.
    :var createIfFound: Flag to specify whether to create, update or attach the specified dataset if the supplied type
    and relation already exist as an override.
    """
    clientId: str = ''
    datasetInfo: DatasetInfo = None
    relationTypeName: str = ''
    createIfFound: bool = False


@dataclass
class AbsOccCreateFormAttachmentInfo(TcBaseObj):
    """
    Form information for attaching a form to the absolute occurrence.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var formInfo: The information used to create or update the form.
    :var relationTypeName: The relation type used for the form attached to the absolute occurrence.
    :var createIfFound: Flag to specify whether to create, update or attach the specified form if the supplied type and
    relation already exist as an override.
    """
    clientId: str = ''
    formInfo: FormInfo = None
    relationTypeName: str = ''
    createIfFound: bool = False


@dataclass
class AbsOccDataGRMExpansionInfo(TcBaseObj):
    """
    Contains a relationName and secondary objects attached as a override with the given relation.
    
    :var relationName: The relation name found for the override.
    :var objects: The secondary objects attached as a override with the given relation.
    """
    relationName: str = ''
    objects: List[BusinessObject] = ()


@dataclass
class AbsOccDataInfo2(TcBaseObj):
    """
    Detailed attribute information for the occurrence.
    
    :var overridesToSet: List of attribute information to set as overrides for the occurrence.
    :var overridesToRemove: List of attribute names that will be unset or removed as overrides for the occurrence.  For
    example, to remove a transform override, add the attribute name for the transform to this list.
    :var usedArr: Reference of existing used arrangement for this absolute occurrence.
    :var boundingBoxInfo: No longer used. Bounding Box information is now passed in through 'datasetAttachments'.
    :var asRequired: Used to set the quantity as required occurrence flag.
    :var occTransform: Positioning information for the occurrence.
    :var occNotes: List of note information for the occurrence.
    :var attachments: Attachments to add to the occurrence.
    :var attachmentsToUnattach: Attachments to remove from the occurrence.
    :var datasetAttachments: Dataset attachments to create or update for the occurrence.
    :var formAttachments: Form attachments to create or update for the occurrence.
    :var clientIdOfUsedArrangement: Client ID of the used arrangement created for this absolute occurrence.
    """
    overridesToSet: List[AttributesInfo] = ()
    overridesToRemove: List[str] = ()
    usedArr: AssemblyArrangement = None
    boundingBoxInfo: List[BoundingBoxInfo] = ()
    asRequired: bool = False
    occTransform: List[float] = ()
    occNotes: List[OccNote] = ()
    attachments: List[AbsOccAttachment2] = ()
    attachmentsToUnattach: List[AbsOccAttachment2] = ()
    datasetAttachments: List[AbsOccCreateDatasetAttachmentInfo] = ()
    formAttachments: List[AbsOccCreateFormAttachmentInfo] = ()
    clientIdOfUsedArrangement: str = ''


@dataclass
class AbsOccDataPref(TcBaseObj):
    """
    Contains a filter that needs to be applied when expanding a GRM override and the filter that needs to be applied on
    the data that is returned based on the qualifier.
    
    :var relationFilterInfos: The filter that needs to be applied when expanding a GRM override.
    :var qualifierFilter: The filter that needs to be applied on the data that is returned based on the qualifier.
    Legal values are : 'None' 'IncludeBvrOnlyQualifyingOverrides' 'IncludeBvrAndUpperQualifyingOverrides' 
    """
    relationFilterInfos: List[RelationAndTypesFilter] = ()
    qualifierFilter: AbsOccDataQualifierFilter = None


@dataclass
class NameValueStruct(TcBaseObj):
    """
    Contains name and list of value strings.
    
    :var name: Attribute name to set
    :var values: Attribute value to set
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class NamedReferenceObjectInfo(TcBaseObj):
    """
    Contains clientId, Object reference, namedReferenceName, typeName and dataNameValuePairs.
    
    :var clientId: Unique identifier to track the related object.
    :var object: Object reference of the object for update, null for create
    :var namedReferenceName: The Named Reference from the dataset to this object, required. NamedReference values  are
    defined for each Dataset type. The customer can add more values as needed. To get a current list of valid Named
    Reference values the programmer can either use BMIDE or can call the SOA Core service getDatasetTypeIno.
    :var typeName: Type of the object to be created. Required for object creation only.
    :var dataNameValuePairs: List of NameValueStruct.
    """
    clientId: str = ''
    object: BusinessObject = None
    namedReferenceName: str = ''
    typeName: str = ''
    dataNameValuePairs: List[NameValueStruct] = ()


@dataclass
class OptionsInfo(TcBaseObj):
    """
    This contains classic variant option information.
    
    :var optionName: Refers to classic variant option name.
    :var optionValue: Refers to classic variant option value.
    :var assocRev: Refers to the ItemRevision object on which the classic variant options are defined.
    """
    optionName: str = ''
    optionValue: str = ''
    assocRev: ItemRevision = None


@dataclass
class AbsOccInfo2(TcBaseObj):
    """
    Attribute information for the occurrence.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var absOcc: Absolute occurrence object reference.  This input can be null for create.
    :var cadOccIdPath: Path of CAD occurrence IDs that identify or find the BOM line.
    :var absOccData: Override data to set for the absolute occurrence.
    """
    clientId: str = ''
    absOcc: AbsOccurrence = None
    cadOccIdPath: List[str] = ()
    absOccData: AbsOccDataInfo2 = None


@dataclass
class AbsOccQualifierInfo(TcBaseObj):
    """
    Contains the context BVR for which the overrides are to be retrieved and an upperQualifier.
    
    :var qualifyingBVR: The context BVR for which the overrides are to be retrieved.
    :var upperQualifier: Context object of the override (such as Arrangement).
    """
    qualifyingBVR: PSBOMViewRevision = None
    upperQualifier: BusinessObject = None


@dataclass
class AbsOccStructureDataInfo(TcBaseObj):
    """
    Contains the list of apn and occurrence thread path that the override are applied. The occurrence thread paths that
    are returned & dataOverrideInfo.
    
    :var occThreadPaths: The list of apn and occurrence thread path that the override are applied.
    The occurrence thread paths that are returned for the given override are in top down order.
    Since the operation returns unconfigured data, the client needs to match the thread paths in previously expanded
    context with the returned ones to determine the exact override.
    :var dataOverrideInfo: dataOverrideInfo
    """
    occThreadPaths: List[ApnToThreadPathStruct] = ()
    dataOverrideInfo: DataOverrideInfo = None


@dataclass
class ReconfigureBOMWindowsInfo(TcBaseObj):
    """
    This contains the list of BOMWindow objects and corresponding corresponding RevisionRule object and VariantRule
    object or StoredOptionSet object information.
    
    :var clientID: Used to track the object(s) created
    :var bomWindow: The BOMWindow object which needs to be reconfigured.
    :var objectForConfigure: Refers to an VariantRule object or StoredOptionSet object information.
    :var revRuleConfigInfo: Refers to an 'RevisionRuleConfigInfo' struct object.
    """
    clientID: str = ''
    bomWindow: BOMWindow = None
    objectForConfigure: BusinessObject = None
    revRuleConfigInfo: RevisionRuleConfigInfo = None


@dataclass
class ReconfigureBOMWindowsOutput(TcBaseObj):
    """
    Contains updated BOMWindow along with the corresponding clientIds.
    
    :var clientID: clientID
    :var bomWindow: The reconfigured BOMWindow
    """
    clientID: str = ''
    bomWindow: BOMWindow = None


@dataclass
class ReconfigureBOMWindowsResponse(TcBaseObj):
    """
    This contains the response for the 'reconfigureBOMWindows' operation.
    
    :var output: This contains list of 'ReconfigureBOMWindowsOutput' struct object, which returns the BOMWindow which
    has updated configuration.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the service
    and error information if any.
    """
    output: List[ReconfigureBOMWindowsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class RelatedObjectTypeAndNamedRefs(TcBaseObj):
    """
    This structure contains a related object type and the list of its named references to be processed.
    
    :var objectTypeName: objectTypeName
    :var namedReferenceNames: namedReferenceNames
    """
    objectTypeName: str = ''
    namedReferenceNames: List[str] = ()


@dataclass
class RelationAndTypesFilter(TcBaseObj):
    """
    This structure contains a relation name and a list of related object types and its named references
    (RelatedObjectTypeAndNamedReferences).  Together they are used to filter objects passed back in a product structure
    expand operation.
    
    :var relationName: Relation name.
    :var relatedObjAndNamedRefs: List of related object types and named references.
    :var namedRefHandler: An enumeration used to identify how named references will be processed.
    Valid values are:
    NoNamedRefs -- No named references are to be processed. The input RelatedObjectTypeAndNamedRefs will be ignored.
    AllNamedRefs -- All named references are to be processed. The input RelatedObjectTypeAndNamedRefs will be ignored.
    UseNamedRefsList -- Only the named references listed in the input RelatedObjectTypeAndNamedRefs struct are
    processed.
    PreferredJT -- Specialized code for selecting which named references to process is executed.
    This is intended for selecting the most appropriate JT files for visualization purposes.
    If related object is a DirectModel, RelatedObjectTypeAndNamedReferences contents will be ignored and only the
    preferred JT is returned.
    If related object is not Direct Model, named reference expansion will proceed as though namedRefHandler is
    UseNamedRefsList.
    """
    relationName: str = ''
    relatedObjAndNamedRefs: List[RelatedObjectTypeAndNamedRefs] = ()
    namedRefHandler: NamedRefHandler = None


@dataclass
class RelativeStructureChildInfo2(TcBaseObj):
    """
    Contains information about the child structure.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with the output or any returned errors.
    :var cadOccId: The CAD occurrence ID or PSOccurrenceThread UID is used to uniquely identify the occurrence under a
    particular context item revision or General Design Element (GDE) for update.  The 'cadOccId' can be null for
    create.  A valid 'cadOccId' must be passed when this operation is called with the 'RelativeStructureParentInfo'
    'complete' input set to true. If a valid 'cadOccId' is not supplied when 'complete' is set to true, this operation
    creates a new occurrence and any data associated against an existing occurrence is removed/lost.  This parameter
    depends on the 'CreateOrUpdateRelativeStructurePref' 'cadOccIdAttrName' preference for finding the existing BOM
    line.
    :var child: The child object for the occurrence creation.  Only item revision and General Design Element (GDE) are
    supported.  If the child occurrence exists, but the input child object is different than the existing child object,
    the existing child will be replaced by the input child.  Existing children are found referencing the occurrence
    found by the 'cadOccId' input.
    :var occInfo: The property information for this occurrence.
    """
    clientId: str = ''
    cadOccId: str = ''
    child: BusinessObject = None
    occInfo: RelOccInfo = None


@dataclass
class SaveBOMWindowsResponse(TcBaseObj):
    """
    Contains the response for the saveBOMWindows operation.
    
    :var serviceData: Any failures will be returned in the ServiceData list of partial errors.
    """
    serviceData: ServiceData = None


@dataclass
class BoundingBox(TcBaseObj):
    """
    Holds the boundingbox co-ordinates  information.
    
    :var xmin: BoundingBox x-coordinate min value in double
    :var ymin: BoundingBox y-coordinate min value in double
    :var zmin: BoundingBox z-coordinate min value in double
    :var xmax: BoundingBox x-coordinate max value in double
    :var ymax: BoundingBox y-coordinate max value in double
    :var zmax: BoundingBox z-coordinate max value in double
    """
    xmin: float = 0.0
    ymin: float = 0.0
    zmin: float = 0.0
    xmax: float = 0.0
    ymax: float = 0.0
    zmax: float = 0.0


@dataclass
class BoundingBoxInfo(TcBaseObj):
    """
    BoundingboxInfo contains boundingbox information and dataset to which it will be attached.This Dataset member
    corresponds to the AbsOccAttachment.overrideObject member to which to apply Bounding Box information.
    
    :var dataset: Dataset object to apply BoundingBox info to
    :var boundingBoxVector: List of xyz coordinate info for Dataset bounding
    """
    dataset: Dataset = None
    boundingBoxVector: List[BoundingBox] = ()


@dataclass
class VariantRulesOutput(TcBaseObj):
    """
    This contains output data for 'createVariantRules' operation.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var vrule: Refers to newly created VariantRule object.
    """
    clientId: str = ''
    vrule: VariantRule = None


@dataclass
class CommitDatasetFileInfo(TcBaseObj):
    """
    Contains basic information for a file to be uploaded to a dataset.
    
    :var dataset: The dataset object reference.
    :var createNewVersion: Flag that if true signifies a new version of the file should be created.
    :var datasetFileTicketInfos: List of dataset file ticket information.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileTicketInfos: List[DatasetFileTicketInfo] = ()


@dataclass
class CreateOrUpdateAbsoluteStructureInfo3(TcBaseObj):
    """
    Input structure for createOrUpdateAbsoluteStructure.
    
    :var lastModifiedOfBVR: Last modified date of BOM view revision (BVR) under the input 'contextItemRev'.  This input
    is not required.  If this input date is different than the current last modified date and the
    'overwriteForLastModDate' preference is false the input will be ignored and processing will continue with the next
    input.  In this scenario, error 215033 will be returned.  If the dates are different and the
    'overwriteForLastModDate' preference is true, processing will continue with the current input.  In this scenario,
    error 215034 will be returned.
    :var contextItemRev: Item revision object reference of the context assembly to create or validate the occurrence. 
    This is a required reference input.
    :var bvrAbsOccInfo: List of absolute occurrence information for the BVR qualified overrides.
    :var arrAbsOccInfo: List of assembly arrangement information for the BVR or arrangement qualified overrides.  This
    input is not required.
    """
    lastModifiedOfBVR: datetime = None
    contextItemRev: ItemRevision = None
    bvrAbsOccInfo: List[AbsOccInfo2] = ()
    arrAbsOccInfo: List[AssemblyArrangementInfo] = ()


@dataclass
class CreateOrUpdateAbsoluteStructurePref3(TcBaseObj):
    """
    Preference structure for 'createOrUpdateAbsoluteStructure'.
    
    :var overwriteForLastModDate: Flag to check whether the BOM view revision will be updated if the input last
    modified date is different from the current last modified date of the object in Teamcenter.  If false, but the
    'CreateOrUpdateAbsoluteStructureInfo3' 'lastModifiedOfBVR' input specified is different than the set modified date,
    partial error 215033 will be returned.
    :var overridesToSynchronize: The attributes that the client is synchronizing when the 'complete' flag is true.
    These are the attribute names that the client is interested in. Any override properties not in this list will not
    be deleted when 'complete' is true.
    :var relationFilters: The relation overrides that the client is synchronizing when the 'complete' flag is true. 
    For instance if a relation filter of IMAN_reference relation name and 'DirectModel' 'relationTypeName' is specified
    and an override of type is in the existing structure but not specified in the input, then it will be deleted.
    :var cadOccIdAttrName: Identifies the BOM line attribute that is used to identify relative occurrences to update.
    """
    overwriteForLastModDate: bool = False
    overridesToSynchronize: List[str] = ()
    relationFilters: List[RelationAndTypesFilter] = ()
    cadOccIdAttrName: str = ''


@dataclass
class CreateOrUpdateAbsoluteStructureResponse2(TcBaseObj):
    """
    The response from the 'createOrUpdateAbsoluteStructure' operation.
    
    :var absOccOutput: Map of input 'clientId' to the created, updated or found absolute occurrence.
    :var asmArrangementOutput: Map of input 'clientId' to the created or updated assembly arrangement.
    :var formOutput: Map of input client id to the created form.
    :var datasetOutput: Information for the created or updated dataset.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' with created or updated
    occurrences, arrangements, datasets or forms. Created forms are added as plain objects.
    """
    absOccOutput: ClientIdToAbsOccMap2 = None
    asmArrangementOutput: ClientIdToAsmArrangementMap = None
    formOutput: ClientIdToFormMap = None
    datasetOutput: List[DatasetOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateRelativeStructureInfo3(TcBaseObj):
    """
    Contains lastModifiedOfBVR,a parent ItemRevision object, list of type RelativeStructureChildInfo and a  boolean
    value to specify BVR precision.
    
    :var lastModifiedOfBVR: Last Modified Date of BVR.  Used for comparison with current last modified date for
    overwrite determination.
    :var parent: Object reference of the context assembly for create or update of the child occurrence, required input
    reference.
    :var childInfo: List of type RelativeStructureChildInfo
    :var precise: Flag for updating the BVR to precise(true)/imprecise(false)
    """
    lastModifiedOfBVR: datetime = None
    parent: BusinessObject = None
    childInfo: List[RelativeStructureChildInfo2] = ()
    precise: bool = False


@dataclass
class CreateOrUpdateRelativeStructurePref3(TcBaseObj):
    """
    Contains overwriteForLastModDate, continueOnError,cadOccIdAttrName and a list of object types.
    
    :var overwriteForLastModDate: Flag to check whether BVR needs to be modified, if input last modified date is
    different from actual.
    :var continueOnError: Flag to continue with process on encountering error.
    :var cadOccIdAttrName: String representing the occurrence note type which holds the value for the CAD occurrence id
    or PSOccurrenceThread uid
    :var objectTypes: List of object types that the client is interested in, such that if the overall structure in
    Teamcenter contains object types or subtypes not in this list, that structure will not be deleted if this operation
    is complete.
    """
    overwriteForLastModDate: bool = False
    continueOnError: bool = False
    cadOccIdAttrName: str = ''
    objectTypes: List[str] = ()


@dataclass
class CreateVariantRulesInfo(TcBaseObj):
    """
    Contains the input for creating a new VariantRule object and to be associated with a ItemRevision object.
    
    :var clientID: Identifier that helps the client to track the object(s) created.
    :var vruleName: Refers to VariantRule object name.
    :var vruleDescription: Refers to VariantRule object description.
    :var rev: The ItemRevision object on which the VariantRule object to be created and attached.
    :var parent: The parent object tag to which the VariantRule object is associated. This is optional and if NULL,
    VariantRule object will be associated with ItemRevision object.
    :var relation: The relation used to associate the VariantRule object to ItemRevision object or parent.
    :var options: Refers to a list of 'OptionsInfo' struct, which has the classic variant option details.
    """
    clientID: str = ''
    vruleName: str = ''
    vruleDescription: str = ''
    rev: ItemRevision = None
    parent: BusinessObject = None
    relation: str = ''
    options: List[OptionsInfo] = ()


@dataclass
class CreateVariantRulesResponse(TcBaseObj):
    """
    This contains response for 'createVariantRules' operation.
    
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the service
    and error information if any.
    :var output: Refers to a list of 'VariantRulesOutput' struct objects, which in turn refers to newly created
    VariantRule objects.
    """
    serviceData: ServiceData = None
    output: List[VariantRulesOutput] = ()


@dataclass
class DataOverrideInfo(TcBaseObj):
    """
    Contains overrideData and GRM override information.
    
    :var overrideData: The AbsOccData object, which has information about qualifier, absolute ocuurence and override
    information.
    :var expandedOverrides: The GRM override information if the AbsOccData is of type AbsOccGRMAnchor.
    """
    overrideData: AbsOccData = None
    expandedOverrides: List[AbsOccDataGRMExpansionInfo] = ()


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    Contains clientId, fileName, namedReferencedName, boolean flags isText, allowReplace, and boundingBoxesAvailable as
    well as list of BoundingBoxes.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var fileName: The name of file to be uploaded.  Only the file name should be specified; the path should not be
    included.
    :var namedReferencedName: The name of the reference to use from the dataset to this file.  This input is required.
    :var isText: Flag that if true signifies the file is a text file.
    :var allowReplace: Flag that if true signifies the file can be overwritten.
    :var boundingBoxesAvailable: Flag that if true signifies bounding box information is available.
    :var boundingBoxes: List of bounding boxes, which hold the bounding box coordinate information.
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False
    boundingBoxesAvailable: bool = False
    boundingBoxes: List[BoundingBox] = ()


@dataclass
class DatasetFileTicketInfo(TcBaseObj):
    """
    Contains basic information for a file to be uploaded to a dataset.
    
    :var datasetFileInfo: Member of type DatasetFileInfo.
    :var ticket: FMS ticket to use in file upload.
    """
    datasetFileInfo: DatasetFileInfo = None
    ticket: str = ''


@dataclass
class DatasetInfo(TcBaseObj):
    """
    Contains clientId, Dataset object reference for update, Name attribute value, basisName, description, Type
    attribute value, lastModifiedOfDataset, ID attribute value, datasetRev, createNewVersion flag,
    namedReferencePreference, dataList, datasetFileInfos, and List of NamedReferenceObjectInfos.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var dataset: The dataset object reference.  This input can be null for create, but it is required for update.
    :var namedReferencePreference: The preference name which holds the list of named references to delete from one
    dataset version to the next.
    :var dataList: The attribute name and values to set on the dataset.
    :var datasetFileInfos: List of dataset file information.
    :var namedReferenceObjectInfos: List of dataset named reference information.
    :var name: The dataset name attribute value.
    :var basisName: The basis name attribute value.  This is used when the name is null or blank.
    :var description: The dataset description attribute value.
    :var type: The dataset type name.
    :var lastModifiedOfDataset: Last modified date of the dataset.
    :var id: The dataset ID attribute value.
    :var datasetRev: The dataset revision attribute value.
    :var createNewVersion: Flag that if true signifies a new version of the dataset should be created.
    """
    clientId: str = ''
    dataset: Dataset = None
    namedReferencePreference: str = ''
    dataList: List[NameValueStruct] = ()
    datasetFileInfos: List[DatasetFileInfo] = ()
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo] = ()
    name: str = ''
    basisName: str = ''
    description: str = ''
    type: str = ''
    lastModifiedOfDataset: datetime = None
    id: str = ''
    datasetRev: str = ''
    createNewVersion: bool = False


@dataclass
class DatasetOutput(TcBaseObj):
    """
    Created or updated dataset and file upload information.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var dataset: The dataset object reference of the created or updated dataset.
    :var commitInfo: Information for a file to be uploaded to a dataset.
    """
    clientId: str = ''
    dataset: Dataset = None
    commitInfo: List[CommitDatasetFileInfo] = ()


@dataclass
class DeleteRelativeStructureInfo3(TcBaseObj):
    """
    Information to delete relative structures.
    
    :var lastModifiedOfBVR: Last modified date of BOM view revision under the input 'parent'.  This input is not
    required.  If this input date is different than the current last modified date and the 'overwriteForLastModDate'
    input preference is false the input will be ignored and processing will continue with the next input.  In this
    scenario, error 215033 will be returned.  If the dates are different and the 'overwriteForLastModDate' input
    preference is true, processing will continue with the current input and the BVR will be modified.  In this
    scenario, error 215034 will be returned.
    :var parent: The item revision context assembly from which the child occurrences are to be removed.  This is a
    required input.  An error will be returned if a valid parent is not specified.
    :var childInfo: List of identifiers of the relative occurrences to be deleted. This is the CAD occurrence ID or
    PSOccurrenceThread UID that uniquely identifies the occurrence under a particular context item revision.
    """
    lastModifiedOfBVR: datetime = None
    parent: BusinessObject = None
    childInfo: List[str] = ()


class AbsOccDataQualifierFilter(Enum):
    """
    Specifies the filter that needs to be applied on the output absolute occurrence data that returned in the response.
    For example an occurrence can have overrides only with qualifying BVR and overrides with both upper and qualifying
    BVR. Legal values are:
    None -- When the upperQualifer is not specified all absoccdata excluding ones with upper qualifiers are returned.
    IncludeBvrOnlyQualifyingOverrides -- When an upperQualifer is specified all absoccdata that has given upper
    qualifier is returned.
    IncludeBvrAndUpperQualifyingOverrides -- Brings all absoccdata that has BVR only and which has upper and BVR
    qualifier.
    """
    None_ = 'None'
    IncludeBvrOnlyQualifyingOverrides = 'IncludeBvrOnlyQualifyingOverrides'
    IncludeBvrAndUpperQualifyingOverrides = 'IncludeBvrAndUpperQualifyingOverrides'


class NamedRefHandler(Enum):
    """
    Identifies which named references will be processed in a product structure one level expand operation.
    Legal values are : 'UseNamedRefsList, NoNamedRefs, AllNamedRefs, PreferredJT.'
    """
    UseNamedRefsList = 'UseNamedRefsList'
    NoNamedRefs = 'NoNamedRefs'
    AllNamedRefs = 'AllNamedRefs'
    PreferredJT = 'PreferredJT'


class BOMLineFilter2(Enum):
    """
    Identifies which BOM lines are to be processed. Legal values are : 'None2, ExcludeOverridden2, ExcludeICHistory2,
    ExcludeGDEs2, ExcludeImanItemLines2'.
    """
    None2 = 'None2'
    ExcludeOverridden2 = 'ExcludeOverridden2'
    ExcludeICHistory2 = 'ExcludeICHistory2'
    ExcludeGDEs2 = 'ExcludeGDEs2'
    ExcludeImanItemLines2 = 'ExcludeImanItemLines2'


"""
ClientIdToAbsOccMap2
"""
ClientIdToAbsOccMap2 = Dict[str, AbsOccurrence]


"""
ClientIdToAsmArrangementMap
"""
ClientIdToAsmArrangementMap = Dict[str, List[AssemblyArrangement]]


"""
ClientIdToFormMap
"""
ClientIdToFormMap = Dict[str, Form]
