from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, WorkspaceObject, RevisionRule, Folder, Awb0Element, Awb0ProductContextInfo, ItemRevision
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceManagement import InputContext5, ChildOccsLoadNxtCursor5
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.OccurrenceManagement import DefaultName, ParentChildrenInfo, OccurrenceSortInput
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.OccurrenceManagement import EffectivityRange, SourceContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import OccurrenceCursor, OccurrenceInfo6, UserContextInfo, FocusOccurrenceInput
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.OccurrenceManagement import InfoForElementCreation
from typing import Dict, List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import OccurrenceFilterInput, OccurrenceFilterOutput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddObjectData2(TcBaseObj):
    """
    The structure contains object to be added as child of input parentElement or productContext.
    
    :var parentElement: The Awb0Element object under which objectsToBeAdded is added. Only parentElement or
    productContext may be set, not both.
    :var objectsToBeAdded: Business object to be added into product. This will be added under parentElement or
    productContext. It can be Item, ItemRevision, GenericDesignElement or Awb0Element.
    :var siblingElement: The newly added Awb0Element object should be added after this Awb0Element object.This is an
    optional parameter which is used for Requirement structures.
    :var inputCtxt: The input context has the information about filter, configuration, and page size.
    :var sortCriteria: Criteria to sort the occurrences based on internal property name and sorting order e.g. "ASC"
    and "DESC".
    :var addObjectIntent: Indicates user gesture. Possible value is 'DragAndDropIntent'
    :var fetchPagedOccurrences: If true then return the entire pageful along with created Awb0Element.
    :var requestPref: Map (string, string) of preference names and value pairs. Allowed preference names are:
    includeInterfaces , includeUnconfigured and . Allowed values are: True/False. Keys and values are case sensitive.
    :var numberOfElements: Indicates quantity of elements user wants to create.
    """
    parentElement: Awb0Element = None
    objectsToBeAdded: List[BusinessObject] = ()
    siblingElement: Awb0Element = None
    inputCtxt: InputContext5 = None
    sortCriteria: OccurrenceSortInput = None
    addObjectIntent: str = ''
    fetchPagedOccurrences: bool = False
    requestPref: RequestPreference9 = None
    numberOfElements: int = 0


@dataclass
class OccurrencesData2(TcBaseObj):
    """
    The OccurrencesData2 supplies the product and the configuration rules to configure the product and get a page of
    occurrences along with effective column configuration. Optionally, filters and sorting criteria may be provided to
    filter or sort the resulting occurrences.
    
    :var product: The top-level product. It may be an ItemRevision representing a product or a Mdl0odelElement such as
    a Cpd0CollaborativeDesign.
    :var parentElement: Parent occurrence for which child occurrences is to be retrieved.
    :var focusOccurrenceInput: Contains input information required to set the focusChildOccurrence.
    :var config: Specifies the complete set of configuration rules including RevisionRule, Effectivity and VariantRule
    to configure content.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var filter: A recipe to search and filter occurrences and sort the results.
    :var sortCriteria: Criteria to sort the occurrences based on intetnal property name and sorting order e.g. "ASC"
    and "DESC".
    :var requestPref: A map  (string, string) of preference names and value pairs. Allowed preference names are:
    "includeInterfaces" , and  "includeUnconfigured".   Allowed values are: True/False. Keys and values are case
    sensitive. When preference "includeInterface" with value true is specified the operation shall  return instances of
    Awb0Interface objects. When preference "includeUnconfigured" with value true is specified the operation shall
    return instances of unconfigured Awb0Element objects.
    """
    product: BusinessObject = None
    parentElement: str = ''
    focusOccurrenceInput: FocusOccurrenceInput = None
    config: OccurrenceConfigInput1 = None
    cursor: OccurrenceCursor = None
    filter: OccurrenceFilterInput = None
    sortCriteria: OccurrenceSortInput = None
    requestPref: RequestPreference2 = None


@dataclass
class OccurrencesResp2(TcBaseObj):
    """
    Contains the resulting occurrences found for product from which retrieval was requested. This data structure also
    returns a cursor to be sent back to the subsequent call to getOccurrences in order to rerieve more pages of results.
    
    :var rootProductContext: The Awb0ProductContextInfo for the root occurrence.
    :var parentProductContext: The Awb0ProductContextInfo for the parent occurrence.
    :var sourceContextToInfoMap: Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to
    its corresponding configuration information.
    :var parentChildrenInfos: List of parent and its children information. This will be populated only when
    loadTreeHierarchyThreshold requestPref is not empty.
    :var requestPref: A map (string, string) of preference names and value pairs. Allowed preference names are:
    "includeInterfaces" , and "includeUnconfigured". Allowed values are: True/False. Keys and values are case
    sensitive. When preference "includeInterface" with value true is specified the operation shall  return instances of
    Awb0Interface objects. When preference "includeUnconfigured" with value true is specified the operation shall
    return instances of unconfigured Awb0Element objects.
    :var serviceData: Contains the list of all BusinessObjects that make up the output, as well as any errors that
    might have occurred as part of the service invocation.
    :var parentOccurrence: The parent occurrence for list of childOccurrences.
    :var focusProductContext: The Awb0ProductContextInfo for the focus occurrence.
    :var focusChildOccurrence: The focus child occurrence for which sibling occurrences are desired.
    :var occurrences: List of resulting occurrences that exist in the configured structure. The configured occurrence
    object is of type Awb0Element
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var userWorkingContextInfo: User's working context information for opened content.
    :var filter: Updated search filter information.
    :var elementToPCIMap: Map containing pair of Root Occurrence (Awb0Element) to its corresponding
    Awb0ProductContextInfo object in Product Set container.
    """
    rootProductContext: Awb0ProductContextInfo = None
    parentProductContext: Awb0ProductContextInfo = None
    sourceContextToInfoMap: SourceContextToInfoMap2 = None
    parentChildrenInfos: List[ParentChildrenInfo] = ()
    requestPref: RequestPreference2 = None
    serviceData: ServiceData = None
    parentOccurrence: OccurrenceInfo6 = None
    focusProductContext: Awb0ProductContextInfo = None
    focusChildOccurrence: OccurrenceInfo6 = None
    occurrences: List[OccurrenceInfo6] = ()
    cursor: OccurrenceCursor = None
    userWorkingContextInfo: UserContextInfo = None
    filter: OccurrenceFilterOutput = None
    elementToPCIMap: ElementToProductContextInfoMap1 = None


@dataclass
class PackElementsData(TcBaseObj):
    """
    Contains a list of Awb0Element objects that are to be "pack" or "unpack", the sorting order criteria and the input
    configuration context.
    
    :var packMode: Indicates if input Awb0Element objects to be packed or unpacked. The valid values are:
    0 - packs the input Awb0Element objects
    1 - unpacks the input Awb0Element objects.
    :var elements: A list of Awb0Element objects that are to be "pack" or "unpack".
    :var sortCriteria: Criteria to sort the occurrences based on internal property name and sorting order e.g. "ASC"
    and  "DESC".
    :var inputCtxt: Input context has the information about filter, configuration, and page size.
    """
    packMode: int = 0
    elements: List[Awb0Element] = ()
    sortCriteria: OccurrenceSortInput = None
    inputCtxt: InputContext5 = None


@dataclass
class PackElementsResp(TcBaseObj):
    """
    A list of Awb0Element objects information on which "pack" or "unpack" action is performed. It also contains the
    information required to build the visible Awb0Element positions.
    
    :var elementsToBeSelected: A list of Awb0Element objects to be selected.
    :var parentChildrenInfos: A list of parent and its children information.
    :var serviceData: Service data containing the changed Awb0Element objects in updated objects list.
    """
    elementsToBeSelected: List[OccurrenceInfo6] = ()
    parentChildrenInfos: List[ParentChildrenInfo] = ()
    serviceData: ServiceData = None


@dataclass
class PagedOccurrencesInfo2(TcBaseObj):
    """
    List of paged child occurrences and the cursor representing the point to which results have been retrieved.
    
    :var childOccurrences: The list of child occurrences, also represent the page of occurrences.
    :var focusOccurrence: The focused occurrence is the occurrence which needs to be searched. The focusedOccurrence is
    the Awb0Element which user wants to find with-in given product.
    :var productContext: The Awb0ProductContextInfo to be associated with the parent that was requested for expand.
    There are scenarios where the given parent may be associated with a configuration context that is different from
    the root to configure it sub level contents. If NULL then configuration context is same as that of nearest parent
    occurrence having non-null value.
    :var cursor: Cursor that represents point to which results have been retrieved.
    :var startReached: If true, the childOccurrences is considered as the first page of occurrences. This value is used
    to identify the start location of occurrence page for two way scrolling functionality.
    :var endReached: If true, the childOccurrences is considered as the last page of occurrences. This value is used to
    identify the end location of occurrence page for two way scrolling functionality.
    """
    childOccurrences: List[OccurrenceInfo6] = ()
    focusOccurrence: Awb0Element = None
    productContext: Awb0ProductContextInfo = None
    cursor: ChildOccsLoadNxtCursor5 = None
    startReached: bool = False
    endReached: bool = False


@dataclass
class SelectedNewElementInfo2(TcBaseObj):
    """
    This structure contains the list of new Awb0Element objects added. List of paged child occurrences and the cursor
    representing the point to which results have been retrieved.
    
    :var newElements: This structure contains the list of new Awb0Element objects added. List of paged child
    occurrences and the cursor representing the point to which results have been retrieved.
    :var pagedOccurrencesInfo: List of paged child occurrences and the cursor representing the point to which results
    have been retrieved.
    """
    newElements: List[Awb0Element] = ()
    pagedOccurrencesInfo: PagedOccurrencesInfo2 = None


@dataclass
class UserContextState2(TcBaseObj):
    """
    This structure contains the current user's client state information for the opened object.
    
    :var openedObject: It can be the ItemRevision, Cpd0CollaborativeDesign or Awb0SavedBookmark object. The client
    state information like active tab, selected Awb0Element will be persisted for this object and the current user.
    :var sublocationAttributes: A map (string, list of strings) of client state attribute name and value pairs. At this
    time only one (key) attribute name is supported: "activeSublocation". Supported values are: (tab names like)
    "overview", "viewer". Keys and values are case in-sensitive. Content sublocation client state attributes that need
    to be persisted will be send to the client using this map.
    :var cloneContentSaveSpecifications: A map ( Awb0ProductContextInfo, list of 'cloneContentSaveAsIn') having
    information about various clone options like Clone, Reference and Ignore action per child Awb0Element per product.
    """
    openedObject: BusinessObject = None
    sublocationAttributes: SublocationAttributes3 = None
    cloneContentSaveSpecifications: CloneContentSaveSpecifications = None


@dataclass
class CloneContentData(TcBaseObj):
    """
    CloneContentData contains all the information needed to validate or duplicate the structure.
    
    :var productContextInfo: The Awb0ProductContextInfo object containing configuration information.
    :var defaultName: Contains the pattern to form the new IDs for the underlying objects (e.g ItemRevision) of the
    input Awb0Element objects.
    :var dataList: A list of Awb0Element objects and clone options.
    :var cloneFlags: A bit mask for the duplicate flags set.
                2 - Rename cad files.
                8 - Run in background mode.
    :var defaultFolder: The folder to add the duplicated structures to. 
    If NULL, the cloned assembly will not be added to a folder. User will have to search for it when needed.
    """
    productContextInfo: Awb0ProductContextInfo = None
    defaultName: DefaultName = None
    dataList: List[CloneContentSaveAsIn] = ()
    cloneFlags: int = 0
    defaultFolder: Folder = None


@dataclass
class CloneContentSaveAsIn(TcBaseObj):
    """
    Structure containing original Awb0Element objects and instructions which tells clone operation what to do with each
    component of the structure.
    
    :var element: Awb0Element object to be cloned.
    :var cloneOperationType: Indicates if the original object is to be:
    0 - Clone, The underlying object represented by Awb0Element to be cloned while instantiating in cloned structure.
    1 - Reference, The underlying object represented by Awb0Element to be referenced while instantiating in cloned
    structure.
    2 - Revise, The underlying object represented by Awb0Element to be revised while instantiating in cloned structure.
    3 - Replace, The underlying object represented by Awb0Element to be replaced by existing part while instantiating
    in cloned structure.
    5 - Ignore, The underlying object represented by Awb0Element should be ignored while instantiating in cloned
    structure.
    :var clonedObjectInfo: A map (string, string) of property names and its value pairs.  
    For example: 
    For the operation type Replace, the map will contain property "item_id" and "rev_id" as keys and their
    corresponding values as values.
    """
    element: Awb0Element = None
    cloneOperationType: int = 0
    clonedObjectInfo: PropertyValues = None


@dataclass
class AddObjectResp2(TcBaseObj):
    """
    The structure contains parent objects under which object was added. When serviceData containing Awb0Element as
    created objects.
    
    :var selectedNewElementInfo: List of new Awb0Element objects and paged occurrences for input parent under which add
    was performed.
    :var newElementInfos: List of NewElementInfo3 when the parent is instantiated more than once.
    :var reloadContent: if true, the content must be reloaded to see updated information.
    :var serviceData: The service data containing created Awb0Element in the created list and partial error if any.
    """
    selectedNewElementInfo: SelectedNewElementInfo2 = None
    newElementInfos: List[NewElementInfo3] = ()
    reloadContent: bool = False
    serviceData: ServiceData = None


@dataclass
class InfoForAddElemData2(TcBaseObj):
    """
    This structure contains information to identify type that can be added as child of input parentElement.
    
    :var parentElement: Awb0Element under which another Awb0Element to be added as child. This is specified if
    Awb0Element needs to be added under parent context. This is optional parameter.
    :var occurrenceTypeName: Internal Name of the occurrence type. This is specified to get the allowed related object
    type names for the given occurrence type name. This is optional parameter.
    """
    parentElement: Awb0Element = None
    occurrenceTypeName: str = ''


@dataclass
class InfoForAddElemResp2(TcBaseObj):
    """
    This structure contains allowable child type name, mapped Awb0Element type name and type name to be searched
    through Full Text Search and a flag indicating if the object type is of occurrence type.
    
    :var preferredTypeInfo: Preferred type information to create Awb0Element.
    :var allowedTypeInfos: List of all allowed types to create and add Awb0Element as child.
    :var preferredExists: true if preferred type is found for input Awb0Element, false otherwise.
    :var serviceData: The service data containing partial error if any.
    :var isOccurrence: If true, if allowedTypeInfos contains information for revisable occurrence; otherwise, false.
    """
    preferredTypeInfo: InfoForElementCreation = None
    allowedTypeInfos: List[InfoForElementCreation] = ()
    preferredExists: bool = False
    serviceData: ServiceData = None
    isOccurrence: bool = False


@dataclass
class NewElementInfo3(TcBaseObj):
    """
    This structure contains parent Awb0Element under which new Awb0Element objects was created.
    
    :var parentElement: Parent under which objects was added.
    :var newElements: List of new OccurrenceInfos created for the parent.
    :var newElementToPositionMap: Position of newly created Awb0Element within its parent.
    """
    parentElement: Awb0Element = None
    newElements: List[OccurrenceInfo6] = ()
    newElementToPositionMap: NewElementToPositionMap2 = None


@dataclass
class OccurrenceConfigInput1(TcBaseObj):
    """
    OcurrenceConfigInput1 specifies the complete set of configuration rules including RevisionRule, Effectivity
    with/without intent values, and VariantRule to configure content. When Awb0ProductContextInfo is specified all
    other configuration parameters are ignored.
    
    :var productContext: Awb0ProductContextInfo containing configuration information.
    :var revisionRule: RevisionRule to configure the product.
    :var sourceContext: Source Context (Fnd0RecipeContainer or Mdl0BaselineRevision) associated with another
    Fnd0RecipeContainer
    :var changeContext: Runtime Business object fnd0ChangeContext that holds the Change Context to be set and
    corresponding Change Configuration Mode.
    :var effectivityDate: Specify the date effectivity to configure the product.
    :var effectivityGroups: List of Fnd0EffGrpRevision objects to configure the product.
    :var unitNo: Unit number to use in order to configure the product.
    :var endItem: Specify the end Item which governs the unit effectivity.
    :var variantRules: List of VariantRule(s) or StoredOptionSet(s) to configure the product.
    :var svrOwningProduct: This indicates the product(ItemRevision or CollaborativeDesign) associated with saved
    VariantRule.
    :var effectivityRanges: List of effectivity data. This data may or may not have effectivity intent values
    associated with the effectivity.
    :var occurrenceScheme: Occurrence scheme associated with product e.g Cpd0CollaborativeDesign.
    """
    productContext: Awb0ProductContextInfo = None
    revisionRule: RevisionRule = None
    sourceContext: WorkspaceObject = None
    changeContext: RuntimeBusinessObject = None
    effectivityDate: datetime = None
    effectivityGroups: List[ItemRevision] = ()
    unitNo: int = 0
    endItem: BusinessObject = None
    variantRules: List[WorkspaceObject] = ()
    svrOwningProduct: BusinessObject = None
    effectivityRanges: List[EffectivityRange] = ()
    occurrenceScheme: BusinessObject = None


"""
A map ( Awb0ProductContextInfo, list of 'cloneContentSaveAsIn') having information about various clone options like Clone, Reference and Ignore action per child Awb0Element per product.
"""
CloneContentSaveSpecifications = Dict[Awb0ProductContextInfo, List[CloneContentSaveAsIn]]


"""
A map of property names and its value pairs (string, string).
"""
PropertyValues = Dict[str, str]


"""
Description:
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive.
"""
RequestPreference2 = Dict[str, List[str]]


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive. The allowed preference names are includeInterfaces. The allowed values are True/False.
"""
RequestPreference9 = Dict[str, List[str]]


"""
Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to its corresponding configuration information
"""
SourceContextToInfoMap2 = Dict[WorkspaceObject, SourceContextInfo]


"""
Map containing Awb0Element to its respective Awb0ProductContextInfo object.
"""
ElementToProductContextInfoMap1 = Dict[Awb0Element, Awb0ProductContextInfo]


"""
A map (string, list of string) of client state attribute name and value pairs. At this time only one (key) attribute name is supported: "activeSublocation". Supported values are: (tab names like) "overview", "viewer" . Keys and values are case in-sensitive.
"""
SublocationAttributes3 = Dict[str, List[str]]


"""
Map containing newly created Awb0Element to its position within parent.
"""
NewElementToPositionMap2 = Dict[Awb0Element, int]
