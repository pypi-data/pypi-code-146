from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ClosureRule, RuntimeBusinessObject, AssemblyArrangement, WorkspaceObject, PSViewType, RevisionRule, Awb0Element, Awb0ProductContextInfo, ItemRevision
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import SearchSortCriteria2, Criteria, SearchFilter2
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_12.OccurrenceManagement import EffectivityRange, SourceContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import OccurrenceCursor, OccurrenceInfo6, UserContextInfo, FocusOccurrenceInput
from typing import Dict, List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.OccurrenceManagement import OccurrenceSortInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OccurrenceFilterInput2(TcBaseObj):
    """
    'OccurrenceFilterInput' specifies the information about recipe to search and filter the result.
    
    :var recipe: Recipe to provide search criteria.
    :var searchFilterCategories: A list of search filter categories.
    :var searchFilterMap: A map (string,list of SearchFilter) containing the list of search filters for each search
    filter field.
    :var searchSortCriteria: A list of criterion to use to sort the filtered results.
    :var searchFilterFieldSortType: Type of sorting that needs to be performed on the search results. The fields can be
    sorted alphabetically in ascending order or in priority order from highest to lowest. The valid values are
    "Alphabetical" &amp; "Priority".
    :var fetchUpdatedFilters: A boolean flag to control filter data population in response. If true, response contains
    updated filters. If false, response does not contain any filter data. E.g. in case of scrolling down the contents,
    this flag can be set as false not to return updated filter as there won't be any updates.
    """
    recipe: List[Criteria] = ()
    searchFilterCategories: List[SearchFilterField3] = ()
    searchFilterMap: SearchFilterMap3 = None
    searchSortCriteria: List[SearchSortCriteria2] = ()
    searchFilterFieldSortType: str = ''
    fetchUpdatedFilters: bool = False


@dataclass
class OccurrenceFilterOutput2(TcBaseObj):
    """
    'OccurrenceFilterOutput2' specifies the output search criteria and updated filters.
    
    :var recipe: Updated recipe including the user specified filters that were provided in 'OccurrenceFilterInput'.
    :var searchFilterCategories: A list of search filter categories.
    :var searchFilterMap: A map ( String, list of 'SearchFilter2' ) of search filter categories ( String ) with their
    corrosponding list of search filters ( 'SearchFilter2' ). Valid keys are' Ptn0PartitionScheme' and 'Design
    Component'.
    :var defaultCategoryDisplayCount: Number of categories display count.
    """
    recipe: List[Criteria] = ()
    searchFilterCategories: List[SearchFilterField3] = ()
    searchFilterMap: SearchFilterMap3 = None
    defaultCategoryDisplayCount: int = 0


@dataclass
class OccurrenceInfo3(TcBaseObj):
    """
    OccurrenceInfo3 is the information about occurrence that is part of the configuration result and passing the filter
    criteria.
    
    :var occurrence: Instance of the BusinessObject that represents a line in the structure.
    :var occurrenceId: Session Recoverable UID of the configured occurrence.
    :var stableId: Stable UID of occurrence. This strictly used for maintaining expansion state of nodes in tree view.
    :var displayName: Display name of the configured occurrence.
    :var numberOfChildren: Number of children of the configured occurrence.
    :var underlyingObjectType: Internal name of the underlying object that occurrence presents.
    """
    occurrence: BusinessObject = None
    occurrenceId: str = ''
    stableId: str = ''
    displayName: str = ''
    numberOfChildren: int = 0
    underlyingObjectType: str = ''


@dataclass
class OccurrencesData3(TcBaseObj):
    """
    The 'OccurrencesData3' supplies the product and the configuration rules to configure the product and get a page of
    occurrences along with effective column configuration. Optionally, filters and sorting criteria may be provided to
    filter or sort the resulting occurrences.
    
    :var product: The top-level product. It may be an ItemRevision representing a product or a Mdl0odelElement such as
    a Cpd0CollaborativeDesign.
    :var parentElement: Parent occurrence for which child occurrences is to be retrieved.
    :var focusOccurrenceInput: Contains input information required to set the focusChildOccurrence.
    :var config: Specifies the complete set of configuration rules including RevisionRule, Effectivity, ClosureRule and
    VariantRule to configure content.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var filter: A recipe to search and filter occurrences and sort the results.
    :var sortCriteria: Criteria to sort the occurrences based on intetnal property name and sorting order e.g. "ASC"
    and "DESC".
    :var requestPref: A map (string, string) of preference names and value pairs. Allowed preference names are:
    "includeInterfaces" , and "includeUnconfigured". Allowed values are: True/False. Keys and values are case
    sensitive. When preference "includeInterface" with value true is specified the operation shall return instances of
    Awb0Interface objects. When preference "includeUnconfigured" with value true is specified the operation shall
    return instances of unconfigured Awb0Element objects.
    :var expansionCriteria: Criteria to expand node
    """
    product: BusinessObject = None
    parentElement: str = ''
    focusOccurrenceInput: FocusOccurrenceInput = None
    config: OccurrenceConfigInput = None
    cursor: OccurrenceCursor = None
    filter: OccurrenceFilterInput2 = None
    sortCriteria: OccurrenceSortInput = None
    requestPref: RequestPreference10 = None
    expansionCriteria: ExpansionCriteria = None


@dataclass
class OccurrencesResp3(TcBaseObj):
    """
    Contains the resulting occurrences found for product from which retrieval was requested. This data structure also
    returns a cursor to be sent back to the subsequent call to getOccurrences3 in order to rerieve more pages of
    results.
    
    :var rootProductContext: The Awb0ProductContextInfo for the root occurrence.
    :var parentProductContext: The Awb0ProductContextInfo for the parent occurrence.
    :var parentChildrenInfos:  List of parent and its children information.
    :var requestPref:  A map (string, string) of preference names and value pairs. Allowed preference names are:
    "includeInterfaces" , and "includeUnconfigured". Allowed values are: True/False. Keys and values are case
    sensitive. When preference "includeInterface" with value true is specified the operation shall return instances of
    Awb0Interface objects. When preference "includeUnconfigured" with value true is specified the operation shall
    return instances of unconfigured Awb0Element objects.
    :var serviceData: Contains the list of all BusinessObjects that make up the output, as well as any errors that
    might have occurred as part of the service invocation.
    :var parentOccurrence: The parent occurrence for list of childOccurrences.
    :var focusProductContext:  The Awb0ProductContextInfo for the focus occurrence.
    :var focusChildOccurrence: The focus child occurrence for which sibling occurrences are desired.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    :var userWorkingContextInfo: User's working context information for opened content.
    :var filter: Updated search filter information.
    :var elementToPCIMap:  Map containing pair of Root Occurrence (Awb0Element) to its corresponding
    Awb0ProductContextInfo object in Product Set container.
    :var sourceContextToInfoMap: Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to
    its corresponding configuration information.
    """
    rootProductContext: Awb0ProductContextInfo = None
    parentProductContext: Awb0ProductContextInfo = None
    parentChildrenInfos: List[ParentChildrenInfo3] = ()
    requestPref: RequestPreference10 = None
    serviceData: ServiceData = None
    parentOccurrence: OccurrenceInfo6 = None
    focusProductContext: Awb0ProductContextInfo = None
    focusChildOccurrence: OccurrenceInfo6 = None
    cursor: OccurrenceCursor = None
    userWorkingContextInfo: UserContextInfo = None
    filter: OccurrenceFilterOutput2 = None
    elementToPCIMap: ElementToProductContextInfoMap4 = None
    sourceContextToInfoMap: SourceContextToInfoMap3 = None


@dataclass
class ParentChildrenInfo3(TcBaseObj):
    """
    List of parent and its children information.
    
    :var parentInfo: Information of parent occurrence.
    :var childrenInfo: Information of children occurrences corresponding to parentInfo.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    """
    parentInfo: OccurrenceInfo3 = None
    childrenInfo: List[OccurrenceInfo3] = ()
    cursor: OccurrenceCursor = None


@dataclass
class RemoveInContextOverrides(TcBaseObj):
    """
    Contains the Awb0Element object and the overridden property which needs to be removed.
    
    :var element: The Awb0Element whose overridden property value to be removed.
    :var propertyName: Internal name of the property of Awb0Element for which override to be removed.
    :var requestPref: Map of preference names and values pairs(string / list of string ). Preference names and values
    are case sensitive.
    """
    element: RuntimeBusinessObject = None
    propertyName: str = ''
    requestPref: RequestPreference10 = None


@dataclass
class SearchFilterField3(TcBaseObj):
    """
    'SearchFilterField3' contains the resulting configured products found, that contain the queried object. This data
    structure also returns a cursor which can be sent back to a call to in order to rerieve more pages of results.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    :var editable: If true, UI renders an editable text box instead of filter values. E.g. when 'categoryType' is
    "Attribute", in UI instead of displaying filter value a text field should be rendered.
    :var quickSearchable: If true, UI rendes a quick search text box. E.g. when 'categoryType' is "Partition", in UI a
    quick search text box is rendered along with all filter values.
    :var categoryType: The type of the filter category. Valid values are "StringMatch", "Partition", "Attribute"
    ,"ClosureRule", "SelectedElement"," BoxZone", "Proximity"," PlaneZone"
    :var isHierarchical: A boolean to indicate if hiearchical display is required for the filter values that belong to
    this categroy. If true, the filter values must have a hiearchical display in the client. Otherwise the filter
    values are shown as a flat list. Default value of this parameter is false.
    :var isMultiSelect:  If true, multiple filters can be selected within this category. Otherwise only single filter
    can be selected. Default value of this parameter is true.
    :var endIndex: The ending index value of the list. This field is applicable only if the 'searchFilterType' field is
    set to "StringFilter" and has list of values.
    :var endReached: If true, the last page of the results has been reached.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0
    editable: bool = False
    quickSearchable: bool = False
    categoryType: str = ''
    isHierarchical: bool = False
    isMultiSelect: bool = False
    endIndex: int = 0
    endReached: bool = False


@dataclass
class SubsetResponse2(TcBaseObj):
    """
    'SubsetResponse2' contains a output subset recipe and filters for every given product context input.
    
    :var filterOut: A list of filter comprising the recipes and filters for the given Awb0ProducContextInfo.
    :var serviceData: Contains the list of all BusinessObject(s) that make up the output, as well as any errors that
    might have ocurred as part of the service invocation.
    """
    filterOut: List[OccurrenceFilterOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class DetachObjectsInputData(TcBaseObj):
    """
    Represents all required parameters to detach secondary objects with primary object.
    
    :var primaryObj: The primary Awb0Element object for the relation to detach.
    :var secondaryObjs: A list of secondary WorkspaceObject objects for the relations to detach.
    """
    primaryObj: Awb0Element = None
    secondaryObjs: List[WorkspaceObject] = ()


@dataclass
class ExpansionCriteria(TcBaseObj):
    """
    Crietria for node expansion.
    
    :var expandBelow: If true node will be expanded. If false node will not be expanded.
    :var loadTreeHierarchyThreshold: Maximum number of nodes to fetch on any node.
    :var scopeForExpandBelow: Uid of the node.
    :var levelNExpand: Number of levels to be expanded for any node.
    """
    expandBelow: bool = False
    loadTreeHierarchyThreshold: int = 0
    scopeForExpandBelow: str = ''
    levelNExpand: int = 0


@dataclass
class FilterSearchCriteria2(TcBaseObj):
    """
    'FilterSearchCriteria2' provides information related to the value entered in search filter field, as well as the
    category related details.
    
    :var categoryType: The category type under which search is requested. Valid values are:" Partition", "Attribute" ,
    "ClosureRule", "SelectedElement", "BoxZone", "Proximity", "PlaneZone"," StringMatch".
    :var categoryInternalName: The name of the category.
    :var searchString: User entered search text for finding the filters.
    :var endIndex: Next index value of list.
    :var pageSize: Indicates the maximum number of values that can be returned in one service call.
    """
    categoryType: str = ''
    categoryInternalName: str = ''
    searchString: str = ''
    endIndex: int = 0
    pageSize: int = 0


@dataclass
class FindMatchingFilterInput2(TcBaseObj):
    """
    Input for 'findMatchingFilters'.
    
    :var productInfo: Product context info.
    :var appliedCriteria: List of criteria which are already applied. This list is used to set selected parameter in
    returned 'SearchFilter2'.
    :var searchCriteria: search criteria
    """
    productInfo: Awb0ProductContextInfo = None
    appliedCriteria: List[Criteria] = ()
    searchCriteria: FilterSearchCriteria2 = None


@dataclass
class FindMatchingFilterOutput2(TcBaseObj):
    """
    'FindMatchingFilterOutput2' provides output information related to the value entered in search filter field, as
    well as the category related details.
    
    :var searchFilterMap: Contains the map (Filter category namestring, list of 'SearchFilter2' ) of category name to
    its display values.
    :var endIndex: The ending index value of the list. This field is applicable only if the 'searchFilterType' field is
    set to "StringFilter" and has list of values.
    :var endReached: If true, the last page of the results has been reached.
    """
    searchFilterMap: SearchFilterMap3 = None
    endIndex: int = 0
    endReached: bool = False


@dataclass
class FindMatchingFilterResponse2(TcBaseObj):
    """
    'FindMatchingFilterResponse' contains output categories and their display values organized based on the search sort
    criteria specified in the input.
    
    :var filterOut: A list of filter output comprising the list of categories and assocaited filter values for the
    given Awb0ProducContextInfo.
    :var serviceData: Contains the list of all BusinessObjects that make up the output, as well as any errors that
    might have ocurred as part of the service invocation.
    """
    filterOut: List[FindMatchingFilterOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class InfoForAddElemData3(TcBaseObj):
    """
    This structure contains information to identify type that can be added as child of input parentElement or
    productContext.
    
    :var parentElement: Awb0Element under which another Awb0Element to be added as child. This is specified if
    Awb0Element needs to be added under parent context.
    :var fetchAllowedOccRevTypes: If true, operation returns allowed occurrence revision (Fnd0AbstractOccRevision)
    types; otherwise, it returns allowed child Item types. The allowed occurrence revision types can be specified using
    preference TCAllowedOccRevTypes_<ParentItemType>.
    """
    parentElement: Awb0Element = None
    fetchAllowedOccRevTypes: bool = False


@dataclass
class OccurrenceConfigInput(TcBaseObj):
    """
    OccurrenceConfigInput specifies the complete set of configuration rules including RevisionRule objects ,
    Effectivity row data (this may or may not contain effectivity intents), ClosureRule and VariantRule to configure
    content.
    
    :var productContext: Awb0ProductContextInfo containing configuration information.
    :var revisionRule: RevisionRule to use in order to configure the product.
    :var occurrenceScheme: Occurrence scheme associated with product e.g CollaborativeDesign.
    :var sourceContext: Source Context (Fnd0RecipeContainer or Mdl0BaselineRevision) associated with product e.g.
    CollaborativeDesign.
    :var changeContext: Runtime Business object fnd0ChangeContext that holds the Change Context to be set and
    corresponding Change Configuration Mode.
    :var appliedArrangement: The arrangement applied on the top level product.
    :var closureRule: ClosureRule used to configure the product.
    :var viewType: Type of View Type applied to the product.
    :var serializedRevRule: Transient RevisionRule to use in order to configure the product.
    :var effectivityDate: Specifies the date effectivity to use in order to configure the product.
    :var effectivityGroups: List of Fnd0EffGrpRevision objects to configure the product.
    :var unitNo: Unit number to use to configure the product.
    :var endItem: Specifies the end Item which governs the  unit effectivity.
    :var variantRules: List of VariantRule(s) or StoredOptionSet(s) to use in order to configure the product.
    :var svrOwningProduct: This indiciates the product(ItemRevision or CollaborativeDesign) associated with saved
    VariantRule. This information is not used when there are more than one VariantRule supplied.
    :var effectivityRanges: A list of effectivity data with effectivity intents.
    """
    productContext: Awb0ProductContextInfo = None
    revisionRule: RevisionRule = None
    occurrenceScheme: BusinessObject = None
    sourceContext: WorkspaceObject = None
    changeContext: RuntimeBusinessObject = None
    appliedArrangement: AssemblyArrangement = None
    closureRule: ClosureRule = None
    viewType: PSViewType = None
    serializedRevRule: str = ''
    effectivityDate: datetime = None
    effectivityGroups: List[ItemRevision] = ()
    unitNo: int = 0
    endItem: BusinessObject = None
    variantRules: List[WorkspaceObject] = ()
    svrOwningProduct: BusinessObject = None
    effectivityRanges: List[EffectivityRange] = ()


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive. The allowed preference names are includeInterfaces. The allowed values are True/False.
"""
RequestPreference10 = Dict[str, List[str]]


"""
'SearchFilterMap3' is a map (Filter category name, string list of 'SearchFilter2') containing the list of search filters for each search filter field based on the search results.
"""
SearchFilterMap3 = Dict[str, List[SearchFilter2]]


"""
Map(WorkspaceObject, SourceContextInfo) containing pair of Source Context Object to its corresponding configuration information
"""
SourceContextToInfoMap3 = Dict[WorkspaceObject, SourceContextInfo]


"""
Map containing Awb0Element to its respective Awb0ProductContextInfo object.
"""
ElementToProductContextInfoMap4 = Dict[Awb0Element, Awb0ProductContextInfo]
