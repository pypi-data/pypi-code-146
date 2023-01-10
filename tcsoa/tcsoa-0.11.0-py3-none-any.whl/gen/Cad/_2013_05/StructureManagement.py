from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, PSBOMView, AssemblyArrangement, ItemRevision, Item, ConfigurationContext
from tcsoa.gen.Cad._2007_01.StructureManagement import AttributesInfo, RevisionRuleConfigInfo, OccNote
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Cad._2009_04.StructureManagement import RelativeStructureParentInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AskChildPathBOMLineOutputNode(TcBaseObj):
    """
    This structure represents a node in the product structure. This structure is tied to a specific client ID of the
    input. Within the context of an input client ID, this structure represents the child path and its corresponding
    BOMLine object in the product structure.
    
    :var childPath: This is the PSOccurrenceThread UID or the Clone Stable ID specified in the input that represents a
    particular node in the context of the child path or occurrence thread chain.
    :var bomline: The BOMLine object corresponding to the input child path.
    """
    childPath: str = ''
    bomline: BOMLine = None


@dataclass
class AskChildPathBOMLinesResponse2(TcBaseObj):
    """
    This structure defines the response from the 'askChildPathBOMLines' operation. The response contains the BOMLine
    objects for each of the input child paths which are still present in the Product Structure in Teamcenter. Each
    BOMLine object in the 'output' is mapped to its corresponding input 'clientId' and one 'childpath'. Only the input
    nodes which are still in the Product Structure in Teamcenter will be in the 'output'. If an input node no longer
    exists in the Product Structure, it will not be present in the 'output'.
    
    :var output: A map of input Client ID to a vector of structure containing the input child path and its
    corresponding BOMLine object.
    :var serviceData: The SOA framework object containing plain objects and error information.
    """
    output: AskChildPathClientIdToBOMLineMap = None
    serviceData: ServiceData = None


@dataclass
class MoveInfo(TcBaseObj):
    """
    This structure represents the information for moving a single occurrence from its current parent assembly to its
    target parent assembly in the context of a higher level assembly.
    
    :var commonParent: The item revision of the common parent assembly where this move is occurring. Only ItemRevision
    type is supported for now.
    :var sourceAssembly: The item revision of the source assembly from where the occurrence is being moved.
    :var occThreadPathToBeMoved: The occurrence thread path of the BOM line to be moved. The occurrence thread path is
    in a bottom up list. The first entry in the list should be occurrence to be moved and the last entry should be the
    occurrence thread for the common parent.
    :var occThreadPathTargetParent: The occurrence thread path of the target parent. The thread path is a bottom up
    list. The first entry in the list is the target parent assembly and the last entry in the list the common parent
    for the move.
    """
    commonParent: BusinessObject = None
    sourceAssembly: BusinessObject = None
    occThreadPathToBeMoved: List[str] = ()
    occThreadPathTargetParent: List[OccThreadEquivalent] = ()


@dataclass
class OccThreadEquivalent(TcBaseObj):
    """
    This structure identifies the child occurrence in the parent assembly. This structure can identify an child
    occurrence that are already existing in Teamcenter as well as the child occurrences that are not yet created in
    Teamcenter.
    
    :var parent: The item revision of the parent assembly. Only item revisions are allowed.
    :var idType: Type of child identifier. The legal values are: 'OccurrenceThread', 'CadOccId', 'ClientId'.
    :var id: The identifier for the occurrence as specified by the 'idType' member. The types of identifiers that can
    be used are the occurrence thread path, CAD occurrence Id and client Id. In cases where an occurrence with the
    specified identifier value does not exist in Teamcenter, the corresponding occurrence will be created.
    :var isNew: flag to indicate if this occurrence is new in the parent assembly.
    """
    parent: BusinessObject = None
    idType: OccThreadIdType = None
    id: str = ''
    isNew: bool = False


@dataclass
class RelOccInfo(TcBaseObj):
    """
    This structure contains the list of attributes information, a flag to specify if the quantity is to be set as
    required, occurrence transform and occurrence notes information for the occurrence.
    The 'MoveInfo' structure contains details on the moving an occurrence from its current parent to a new target
    parent.
    
    :var attrsToSet: Name and value pairs for the attribute information to set or update on the occurrence specified in
    the form of BOM line property names. For example, the BOM line occurrence name property could be specified with the
    attrsToSet name as bl_occurrence_name and the value as the occurrence name.
    :var asRequired: Flag to specify that the quantity is as required. The default value is FALSE.
    :var occTransform: Positioning information for the occurrence. This needs to be ordered in the standard matrix
    format.
    :var occNotes: Note information for the occurrence.
    :var moveInfo: Optional data specifying the occurrence to be moved and the parent to which to be moved to.
    """
    attrsToSet: List[AttributesInfo] = ()
    asRequired: bool = False
    occTransform: List[float] = ()
    occNotes: List[OccNote] = ()
    moveInfo: MoveInfo = None


@dataclass
class RelativeStructureChildInfo3(TcBaseObj):
    """
    This structure contains information for the child node of a relative structure
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure. If clientId is not provided then it can be difficult to align the
    input with the output or any returned errors.
    :var childBomViewTypeName: The name of the BOM view type of the child to be added to the parent BOMViewRevision. If
    not specified, the 'bomViewTypeName' specified in the input preference  'CreateOrUpdateRelativeStructurePref' will
    be used as the default. For example, this can be used in a mult-CAD usage, where a JTView of a child originally
    created in a different CAD system needs to be added to a parent in NX, where the default view type is view.
    :var cadOccId: The CAD occurrence ID or PSOccurrenceThread UID is used to uniquely identify the occurrence under a
    particular context item revision or General Design Element (GDE) for update. The 'cadOccId' can be null for create.
    A valid cadOccId must be passed when this operation is called with the 'RelativeStructureParentInfo' 'complete'
    input set to true. If a valid 'cadOccId' is not supplied when 'complete' is set to true, this operation creates a
    new occurrence and any data associated against an existing occurrence is removed/lost. This parameter depends on
    the 'CreateOrUpdateRelativeStructurePref' 'cadOccIdAttrName' preference for finding the existing BOM line
    :var child: The child object for the occurrence creation. Only ItemRevision and GeneralDesignElement (GDE) are
    supported. If the child occurrence exists, but the input child object is different than the existing child object,
    the existing child will be replaced by the input child. Existing children are found referencing the occurrence
    found by the 'cadOccId' input
    :var occInfo: The property information to set or updated for this occurrence. The optional 'moveInfo' structure
    specifies if this occurrence is being moved to a new parent assembly.
    """
    clientId: str = ''
    childBomViewTypeName: str = ''
    cadOccId: str = ''
    child: BusinessObject = None
    occInfo: RelOccInfo = None


@dataclass
class CreateOrUpdateRelativeStructureInfo4(TcBaseObj):
    """
    Contains the data for creating or updating the relative product structure for a item revision. It includes the
    information about the parent and its object and a list of type 'RelativeStructureChildInfo3' that describes the
    first level children and their occurrence information.
    
    :var parentInfo: Object reference of the context assembly for create or update of the child occurrence, required
    input reference.
    :var childInfo: List of child info structures for creating the occurrences or updating the occurrence attributes.
    If no child objects are specified and 'RelativeStructureParentInfo' 'complete' is true, all existing child objects
    will be removed. If no child objects are specified and 'RelativeStructureParentInfo' 'complete' is false, the input
    is ignored.
    """
    parentInfo: RelativeStructureParentInfo = None
    childInfo: List[RelativeStructureChildInfo3] = ()


@dataclass
class CreateWindowsInfo2(TcBaseObj):
    """
    Main input structure that defines Item or ItemRevision of the top line in the BOMWindow. In the input, either
    revRuleConfigInfo object and objectsForConfigure object(variant rules or saved option set) or configContext object
    is required.
    
    :var clientId: Identifier that helps the client to track the objects created.
    :var item: Item object reference.
    :var itemRev: ItemRevision object reference.
    :var bomView: PSBOMView object reference
    :var revRuleConfigInfo: Structure with information about RevisionRuleConfigInfo
    :var objectsForConfigure: List of variant rules or single stored option set object to set on this window
    :var activeAssemblyArrangement: Active assembly arrangement of this BOMWindow
    :var configContext: ConfigurationContext object reference.
    :var bomWinPropFlagMap: Mapping for window property and respective value that needs to be set on window. User need
    to populate this map with following property string values as key and true or false as value, which will be set or
    unset on the window
    
    Valid property values are 
    
        show_unconfigured_variants
        show_unconfigured_changes
        show_suppressed_occurrences
        is_packed_by_default
        show_out_of_context_lines
        fnd0show_uncnf_occ_eff
        fnd0bw_in_cv_cfg_to_load_md
    """
    clientId: str = ''
    item: Item = None
    itemRev: ItemRevision = None
    bomView: PSBOMView = None
    revRuleConfigInfo: RevisionRuleConfigInfo = None
    objectsForConfigure: List[BusinessObject] = ()
    activeAssemblyArrangement: AssemblyArrangement = None
    configContext: ConfigurationContext = None
    bomWinPropFlagMap: StringMap = None


class OccThreadIdType(Enum):
    """
    Identifies the type of data being sent by the client to identify the child occurrence information in the parent
    assembly.
    The legal values are: 'OccurrenceThread, CadOccId, ClientId.'
    """
    OccurrenceThread = 'OccurrenceThread'
    CadOccId = 'CadOccId'
    ClientId = 'ClientId'


"""
This map contains the return data for the 'AskChildPathBOMLines' operation. The key for the map is the input Client ID. The value will be a vector of 'AskChildPathBOMLineOutputNode'. The output node structure contains an input child path (which can be a PSOccurrenceThread UID or Clone Stable ID) and its corresponding BOMLine object. The map will contain the BOMLine object for all the valid nodes in the input. For nodes that are no longer available in the Product Structure in Teamcenter, there will be no entry in this map. In other words, if particular input has no corresponding BOMLine object for it in the output, it is implied that that node no longer exists in the Product Structure in Teamcenter.
"""
AskChildPathClientIdToBOMLineMap = Dict[str, List[AskChildPathBOMLineOutputNode]]


"""
This is map of string Key to string Value.
"""
StringMap = Dict[str, str]
