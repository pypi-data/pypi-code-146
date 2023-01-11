from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, WorkspaceObject, RevisionRule, Awb0Element, Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import OccurrenceCursor, OccurrenceInfo6, UserContextInfo, FocusOccurrenceInput
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_06.OccurrenceManagement import PagedOccurrencesInfo6, InputContext5
from typing import Dict, List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import OccurrenceFilterInput, OccurrenceFilterOutput
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.OccurrenceManagement import ParentChildrenInfo, OccurrenceSortInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddObjectData(TcBaseObj):
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
    """
    parentElement: Awb0Element = None
    objectsToBeAdded: List[BusinessObject] = ()
    siblingElement: Awb0Element = None
    inputCtxt: InputContext5 = None
    sortCriteria: OccurrenceSortInput = None
    addObjectIntent: str = ''
    fetchPagedOccurrences: bool = False
    requestPref: RequestPreference8 = None


@dataclass
class OccurrencesData(TcBaseObj):
    """
    The OccurrencesData supplies the product and the configuration rules to configure the product and get a page of
    occurrences along with effective column configuration. Optionally, filters and sorting criteria may be provided to
    filter or sort the resulting occurrences.
    
    :var product: The top-level product. It may be an Item, ItemRevision representing a product or a Mdl0odelElement
    such as a Cpd0CollaborativeDesign.
    :var parentElement: Parent occurrence for which child occurrences is to be retrieved.
    :var focusOccurrenceInput: Contains input information required to set the focusChildOccurrence.
    :var config: A list of configuration rules to apply to the product.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var filter: A recipe to search and filter occurrences and sort the results.
    :var sortCriteria: Criteria to sort the occurrences based on intetnal property name and sorting order e.g. "ASC"
    and "DESC".
    :var requestPref: Map (string, string) of preference names and value pairs. Allowed preference names are:
    includeInterfaces , includeUnconfigured and . Allowed values are: True/False. Keys and values are case sensitive.
    """
    product: BusinessObject = None
    parentElement: str = ''
    focusOccurrenceInput: FocusOccurrenceInput = None
    config: OccurrenceConfigInput = None
    cursor: OccurrenceCursor = None
    filter: OccurrenceFilterInput = None
    sortCriteria: OccurrenceSortInput = None
    requestPref: RequestPreference8 = None


@dataclass
class OccurrencesResp(TcBaseObj):
    """
    Contains the resulting occurrences found for product from which retrieval was requested. This data structure also
    returns a cursor to be sent back to the subsequent call to getOccurrences in order to rerieve more pages of results.
    
    :var rootProductContext: The Awb0ProductContextInfo for the root occurrence.
    :var parentProductContext: The Awb0ProductContextInfo for the parent occurrence.
    :var sourceContextToInfoMap: Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to
    its corresponding configuration information.
    :var parentChildrenInfos: List of parent and its children information. This will be populated only when
    loadTreeHierarchyThreshold requestPref is not empty.
    :var requestPref: Map (string, string) of preference names and value pairs. Allowed preference names are:
    includeInterfaces, includeUnconfigured and  allowed values are: True/False. Keys and values are case sensitive.
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
    Awb0ProductContextInfo object in Product Set container
    """
    rootProductContext: Awb0ProductContextInfo = None
    parentProductContext: Awb0ProductContextInfo = None
    sourceContextToInfoMap: SourceContextToInfoMap = None
    parentChildrenInfos: List[ParentChildrenInfo] = ()
    requestPref: RequestPreference8 = None
    serviceData: ServiceData = None
    parentOccurrence: OccurrenceInfo6 = None
    focusProductContext: Awb0ProductContextInfo = None
    focusChildOccurrence: OccurrenceInfo6 = None
    occurrences: List[OccurrenceInfo6] = ()
    cursor: OccurrenceCursor = None
    userWorkingContextInfo: UserContextInfo = None
    filter: OccurrenceFilterOutput = None
    elementToPCIMap: ElementToProductContextInfoMap3 = None


@dataclass
class SelectedNewElementInfo(TcBaseObj):
    """
    This structure contains the list of new Awb0Element objects added. List of paged child occurrences and the cursor
    representing the point to which results have been retrieved.
    
    :var newElements: List of new Awb0Element created for the selected parent.
    :var pagedOccurrencesInfo: List of paged child occurrences and the cursor representing the point to which results
    have been retrieved.
    """
    newElements: List[Awb0Element] = ()
    pagedOccurrencesInfo: PagedOccurrencesInfo6 = None


@dataclass
class SourceContextInfo(TcBaseObj):
    """
    Configuration information e.g. Revision Rule name, Variant Rule name, Effectivity formula for the source context
    object.
    
    :var revRuleName: Display name of Revision Rule associated with the source context object
    :var varRuleName: Display name(s) of Variant Rule associated with the source context object.
    :var effectivityFormula: Display value of effectivity formula associated with the source context object
    """
    revRuleName: str = ''
    varRuleName: List[str] = ()
    effectivityFormula: str = ''


@dataclass
class AddObjectResp(TcBaseObj):
    """
    The structure contains parent objects under which object was added. When serviceData containing Awb0Element as
    created objects.
    
    :var selectedNewElementInfo: List of new Awb0Element objects and paged occurrences for input parent under which add
    was performed.
    :var newElementInfos: List of NewElementInfo2 when the parent is instantiated more than once.
    :var reloadContent: if true, the content must be reloaded to see updated information.
    :var serviceData: The service data containing created Awb0Element in the created list and partial error if any.
    """
    selectedNewElementInfo: SelectedNewElementInfo = None
    newElementInfos: List[NewElementInfo2] = ()
    reloadContent: bool = False
    serviceData: ServiceData = None


@dataclass
class EffectivityRange(TcBaseObj):
    """
    Structure to hold a row of effectivity data. This structure can also hold the intent values associated with the
    effecticity row data.
    
    :var unitIn: Unit at which this validity range starts. Valid value is non zero positive integer number.
    :var unitOut: Unit at which this validity range ends. Valid value is non zero positive integer number. Maximum
    value can be 2147483646 ( SO ) or 2147483647 ( UP ).
    :var dateIn: Date at which this validity range starts.
    :var dateOut: Date at which this validity range ends. Maximum value can be 26th Dec 9999 00:00:00 ( SO ) or 30th
    Dec 9999 00:00:00 ( UP ) in UTC timezone.
    :var intentFormula: The intent formula string associated with the current effectivivity row. This string represents
    all the intent values applied to the current effectivity range. This string should have following syntax:
    [Intent_item_ID]<Intent_family_name> = <Applied_family_value>
    Here,
    Intent_item_ID represents the item ID for the intent item associated with the Product Design.
    Intent_family_name, represents the name of the intent family selected, and
    Applied_family_value, is the selected value from intent family.
    For example, [IntentItem01]Manufacturing=Production.
    """
    unitIn: int = 0
    unitOut: int = 0
    dateIn: datetime = None
    dateOut: datetime = None
    intentFormula: str = ''


@dataclass
class NewElementInfo2(TcBaseObj):
    """
    This structure contains parent Awb0Element  under which new Awb0Element objects was created.
    
    :var parentElement: Parent under which objects was added.
    :var newElements: List of new Awb0Element created for the parent.
    :var newElementToPositionMap: Position of newly created Awb0Element within its parent.
    """
    parentElement: Awb0Element = None
    newElements: List[Awb0Element] = ()
    newElementToPositionMap: NewElementToPositionMap = None


@dataclass
class OccurrenceConfigInput(TcBaseObj):
    """
    OccurrenceConfigInput specifies the complete set of configuration rules including RevisionRule, Effectivity
    with/without intent values, and VariantRule to configure content. When Awb0ProductContextInfo is specified all
    other configuration parameters are ignored.
    
    :var productContext: Awb0ProductContextInfo containing configuration information.
    :var revisionRule: RevisionRule to configure the product.
    :var changeContext: Runtime Business object fnd0ChangeContext that holds the Change Context to be set and
    corresponding Change Configuration Mode.
    :var effectivityDate: Specifies the date effectivity to configure the product.
    :var unitNo: Unit number to use in order to configure the product.
    :var endItem: Specifies the end Item which governs the unit effectivity.
    :var variantRules: List of VariantRule(s) or StoredOptionSet(s) to configure the product.
    :var svrOwningProduct: This indicates the product(ItemRevision or CollaborativeDesign) associated with saved
    VariantRule.
    :var effectivityRanges: List of effectivity data. This data may or may not have effectivity intent values
    associated with the effectivity.
    :var occurrenceScheme: Occurrence scheme associated with product e.g Cpd0CollaborativeDesign.
    :var sourceContext: Source Context (Fnd0RecipeContainer or Mdl0BaselineRevision) associated with another
    Fnd0RecipeContainer
    """
    productContext: Awb0ProductContextInfo = None
    revisionRule: RevisionRule = None
    changeContext: RuntimeBusinessObject = None
    effectivityDate: datetime = None
    unitNo: int = 0
    endItem: BusinessObject = None
    variantRules: List[WorkspaceObject] = ()
    svrOwningProduct: BusinessObject = None
    effectivityRanges: List[EffectivityRange] = ()
    occurrenceScheme: BusinessObject = None
    sourceContext: WorkspaceObject = None


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive. The allowed preference names are includeInterfaces. The allowed values are True/False.
"""
RequestPreference8 = Dict[str, List[str]]


"""
Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to its corresponding configuration information.
"""
SourceContextToInfoMap = Dict[WorkspaceObject, SourceContextInfo]


"""
Map containing Awb0Element to its respective Awb0ProductContextInfo object.
"""
ElementToProductContextInfoMap3 = Dict[Awb0Element, Awb0ProductContextInfo]


"""
Map containing newly created Awb0Element to its position within parent.
"""
NewElementToPositionMap = Dict[Awb0Element, int]
