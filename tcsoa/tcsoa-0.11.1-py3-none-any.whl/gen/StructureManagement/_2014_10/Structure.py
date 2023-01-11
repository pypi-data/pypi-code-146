from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, POM_object, RevisionRule, Folder, TC_Project, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CloneStructureDefaultNaming(TcBaseObj):
    """
    The CloneStructureDefaultNaming structure conatians the information to help form new Item IDs.
    
    :var autogen: Auto assign new item IDs. If set to True this takes precedence over all other parameters.
    :var prefix: Substring to be prefixed to the old item ID to form a new item ID. This parameter can be used in
    conjuction with the other parameters except when autogen is set to True.
    :var suffix: Substring to be suffixed to the old item ID to form a new item ID. This parameter can be used in
    conjuction with the other parameters except when autogen is set to True..
    :var from: Substring to be replaced from the old item ID by another substring to form a new item ID. This parameter
    is required to work in conjuction with the "to" parameter but can be used in conjuction with the other parameters
    except when autogen is set to True.
    :var to: Substring to replace with a substring from the old item ID to form a new item ID. This parameter is
    required to work in conjuction with the "from" parameter but can be used in conjuction with the other parameters
    when except autogen is set to True.
    """
    autogen: bool = False
    prefix: str = ''
    suffix: str = ''
    from_: str = ''
    to: str = ''


@dataclass
class CloneStructureExpandOrUpdateDuplicateItemsOutput(TcBaseObj):
    """
    The CloneStructurExpandOrUpdateDuplicateItemsOutput represents the collection of all related data objects with the
    structure ItemRevision object(s) or part family masters ItemRevision object(s).
    
    :var parentObject: The BOM structure ItemRevision or a part family master ItemRevision.
    :var parentObjectCloneable: Indicates if the object can be cloned. 
    0 - users choice to clone or not
    1 - mandatory - If it is mandatory that cad dependent type will come in pre-checked and the user will not be able
    to de-select it.
    2 - Must not be cloned - If set the cad dependent type will come in unchecked and the user will not be able to
    select it.
    
    :var relatedObjectInfo: List of all dependent objects that are related to the object.
    """
    parentObject: ItemRevision = None
    parentObjectCloneable: int = 0
    relatedObjectInfo: List[CloneStructureRelatedItemsInfo] = ()


@dataclass
class CloneStructureExpandOrUpdateItemsInfo(TcBaseObj):
    """
    The CloneStructureExpandOrUpdateItemsInfo structure contains the information needed to conduct an expand or update
    of a BOM structure that will be duplicated.
    
    :var bomline: If it is not null, expand it and get its dependencies based on the depTypes. The BOMLine can be any
    line in the structure that the user picks for expansion.
    :var itemRevs: The ItemRevision objects to perform search dependencies on. If empty, the ItemRevision objects to be
    used will be from the expansion of the BOMLine.
    :var cadOptions: The dependency types to use for the operation. 
    Following are the CAD options values that are used for CAD Dependency searches: 
    Drawings, Required, PartFamilyMaster, PartFamilyMember, AllDep and  Internal.
    """
    bomline: BOMLine = None
    itemRevs: List[ItemRevision] = ()
    cadOptions: List[str] = ()


@dataclass
class CloneStructureExpandOrUpdateResponse(TcBaseObj):
    """
    The CloneStructureExpandOrUpdateResponse structure contains the results of the structure dependent data search.
    
    :var outputs: List of CloneStructureExpandOrUpdateDuplicateItemsOutput which contains information about the BOM
    structure ItemRevision to its related data relationships.
    :var additionalDependencies: List of available non static CAD dependencies that are derived from the CAD dependency
    closure rules
    :var serviceData: The error information will be recorded here.
    """
    outputs: List[CloneStructureExpandOrUpdateDuplicateItemsOutput] = ()
    additionalDependencies: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class CloneStructureInputInfo(TcBaseObj):
    """
    CloneStructureInputInfo that contains all the information needed to validate and duplicated multiple structures in
    one API call.
    
    :var topLines: The top BOMLine or selected BOMLine of the structure to be cloned. The user can select a sub
    assembly from the original structure to clone. (If running Async mode this input needs to be NULL.)
    :var cadOptions: List of CAD dependency options to process and traverse in the structure to be duplicated.
    Typical options would be Drawings, Required, PartFamilyMaster, PartFamilyMember, AllDep and Internal.
    :var defaultName: The pattern to form the new ItemId.
    :var dataMap: A struct vector of original ItemRevisions and instructions which tells duplicate operation what to do
    with each component of the structure.
    :var cloneFlags: A bitmap for the duplicate flags set.
    1 - smart selection using topLine assigned projects
    2 - rename cad files
    4 - return cloned object map information
          (nor supported in background mode) 
          (RAC will always set this to false)
    8 - run duplicate in background mode
          (this activates the Async mode if it is available)
    16- run duplicate in validate mode
    
    :var projects: The user selected projects to which to add the duplicated Item objects.
    :var defaultFolder: The folder to add the duplicated structures into. (can be NULL)
    :var revRule: If duplicate operation is being run in the background send in the revRule to use when creating the
    new BOMWindow (required for Async).
    :var topItemRevs: If duplicate operation is being run in the background need the top item revision of the structure
    to create the new BOM Window (required for Async).
    """
    topLines: List[BOMLine] = ()
    cadOptions: List[str] = ()
    defaultName: CloneStructureDefaultNaming = None
    dataMap: List[CloneStructureSaveAsIn] = ()
    cloneFlags: int = 0
    projects: CloneStructureProjectInfo = None
    defaultFolder: Folder = None
    revRule: RevisionRule = None
    topItemRevs: List[ItemRevision] = ()


@dataclass
class CloneStructureProjectInfo(TcBaseObj):
    """
    The CloneStructureProjectInfo contains project information for Structure Clone to validate the projects and assign
    the cloned objects to the user selected projects.
    
    :var assign: Flag that determines if projects are to be assigned to new cloned objects.
    :var validate: Flag that determines if validation needs to be executed on projects.
    :var projects: List of projects that the new cloned objects will be assigned to.
    """
    assign: bool = False
    validate: bool = False
    projects: List[TC_Project] = ()


@dataclass
class CloneStructureRelatedItemsInfo(TcBaseObj):
    """
    The CloneStructureRelatedItemsInfo represents the dependent data found and how it is related to a structure
    ItemRevision. RelatedItemsInfo also can represent a family table member to a family table master.
    
    :var relatedObject: An ItemRevision that is the related data.
    :var relatedObjectCloneable: Indicates if the relObj can be cloned.
    0 - users choice to clone or not
    1 - mandatory - If it is mandatory that cad dependent type will come in pre-checked and the user will not be able
    to de-select it.
    2 - Must not be cloned - If set the cad dependent type will come in unchecked and the user will not be able to
    select it
    
    :var relatedObjectGRMName: The GRM relationship used to find the related data.
    :var relatedObjectCADOptionName: The cad dependency type use for the operation.
    """
    relatedObject: ItemRevision = None
    relatedObjectCloneable: int = 0
    relatedObjectGRMName: str = ''
    relatedObjectCADOptionName: str = ''


@dataclass
class CloneStructureResponse(TcBaseObj):
    """
    The CloneStructureResponse structure contains the response information for the cloneStructure API. 
    
    :var dataMap: This is populated when validation of BOM structure fails or validateOnly flag is set to true. Reason
    for returning this information is it allows the calling client to reuse this data to speed the re-validation of the
    structure once the user fixes the error. The struct vector will contain the original Item Revisions, operation
    type, replacing item revision, MFK, PropertyValues and DeepCopyData overrides for each level of the structure.
    
    If validation passes and validateOnly flag is set to false this will be empty.
    
    :var clonedItemRevInfoMap: Map of bomlines to their new cloned item rev and clone status.
    :var clonedObjectInfoMap: Map of original objects and their cloned equivalent (will be empty if validation fails).
    (not support in Async mode)
    :var serviceData: Standard service data return where the partial errors are placed.
    """
    dataMap: List[CloneStructureSaveAsIn] = ()
    clonedItemRevInfoMap: CloneStructureTopLineDataMap = None
    clonedObjectInfoMap: CloneStructureObjectMap = None
    serviceData: ServiceData = None


@dataclass
class CloneStructureSaveAsIn(TcBaseObj):
    """
    The CloneStructureSaveAsIn structure contains all the instructions that tells duplicate what to do with the
    children of the structure to be duplicated.
    
    :var origItemRevComp: Original item revision component to be cloned.
    :var cloneOperationType: Indicates if the original item revision component is to be:
    0 - Clone, component is part of the structure to be cloned and we want to clone the component.
    1 - Reference, component is part of the structure to be cloned and we want to reference, not clone the component.
    2 - Revise, component is part of the structure to be cloned and we want to revise the component.
    3 - Replace, component is part of the structure to be cloned and we want to replace the component with an existing
    part.
    4 - Include, component is not a part of the structure to be cloned and we want to clone the component because it
    has some relation to the structure to be cloned that is not published to Teamcenter.
    
    :var newItemRevinfo: Struct that contains all information related to item revision based on following operations:
    
    - Clone/Revise - will contain Property values (MFK complaint) to support business object "save-as" and "revise"
    operations
    - Reference - will be empty
    - Replace - will contain replacing Item revision "item_id" and "rev_id" values.
    
    
    :var deepCopyDataOverride: Vector of DeepCopyData elements that instructs the "Save As" operation what attached
    data to clone and not clone (Save As Descriptors) for the item revision.
    Note: Reference, Revise and Replace operation will not use this parameter and such it will be empty.
    """
    origItemRevComp: ItemRevision = None
    cloneOperationType: int = 0
    newItemRevinfo: PropertyValues = None
    deepCopyDataOverride: List[DeepCopyData] = ()


@dataclass
class CloneStructureTopLineData(TcBaseObj):
    """
    The CloneStructureTopLineData structure contains the high-level status information of a BOM structure that was
    validated and duplicated.
    
    :var bomline: The top line assembly that represent the original Item revision that was cloned to make the new
    cloned Item revision.
    :var orignalItemRev: Original Item Revision that was cloned to make the new cloned Item Revision.
    :var clonedNewItemRev: New cloned topline item revision.
    :var status: Status of cloning the topline.
    0 - Clone Successful
    46229 - Clone Failed
    46230 - Clone With Partial Errors
    46231 - Validate Failed
    46232 - Clone Asynchronous Job Submitted
    """
    bomline: BOMLine = None
    orignalItemRev: ItemRevision = None
    clonedNewItemRev: ItemRevision = None
    status: int = 0


@dataclass
class DeepCopyData(TcBaseObj):
    """
    The DeepCopyData data structure holds the relevant information regarding applicable deep copy rules
    
    :var attachedObject: Other side object.
    :var propertyName: Name of relation type or reference property for which DeepCopy rule is configured.
    :var propertyType: If Relation, it represents Relation type property. If Reference, it represents Reference property
    :var copyAction: DeepCopy action [NoCopy, CopyAsReference, CopyAsObject, Select ].
    :var isTargetPrimary: If true the target object is processed as primary, otherwise it is processed as a secondary
    object.
    :var isRequired: If true, the copy action can not be modified. If false, the copy action can be changed to
    different action by the user.In this case, the copy action field in the revise dialog is editable.
    :var copyRelations: If true, the custom properties on the source relation object are copied over to the
    newly-created relation. If false, custom properties are not copied.
    :var operationInputTypeName: OperationInput type name.
    :var childDeepCopyData: List of DeepCopy data for the secondary objects on the other side.
    :var operationInputs: OperationInput field to capture property values of attached object, to apply on copied object
    of attached object. Map of property name(key) and property values(values) in string format of attached object, to
    be set on copied object of attached object. The calling client is responsible for converting the different property
    types (int, float, date .etc) to a string using the appropriate toXXXString functions in the SOA client framework
    Property class.
    """
    attachedObject: BusinessObject = None
    propertyName: str = ''
    propertyType: str = ''
    copyAction: str = ''
    isTargetPrimary: bool = False
    isRequired: bool = False
    copyRelations: bool = False
    operationInputTypeName: str = ''
    childDeepCopyData: List[DeepCopyData] = ()
    operationInputs: PropertyValues = None


"""
This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.


"""
PropertyValues = Dict[str, List[str]]


"""
This maps the original objects  to the new cloned objects
"""
CloneStructureObjectMap = Dict[POM_object, POM_object]


"""
Map that maps original Topline to new cloned Topline with its status
"""
CloneStructureTopLineDataMap = Dict[BOMLine, CloneStructureTopLineData]
