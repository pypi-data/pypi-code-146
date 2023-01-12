from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, VariantRule, RevisionRule, Awb0Element, Item, Awb0ProductContextInfo
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OccurrenceFilter(TcBaseObj):
    """
    'OccurrenceFilter' specifies the search filtering and sorting criteria if filtering and sorting of the resulting
    occurrences is desired.
    
    :var searchInput: Full Text Filter information
    """
    searchInput: SearchInput = None


@dataclass
class OccurrenceInfo(TcBaseObj):
    """
    'OccurrenceInfo' is the information about one occurrence that is returned as part of the result. It contains an
    occurrence that is part of the configured structure being queried and that passes the filter criteria, as well as
    the attachments requested.
    
    :var occurrence: Instance of the Awb0Element.
    :var attachedObjects: A list of attached objects if attachments were requested as part of the
    'AttachedDataCriteria' in the input. This list will be empty if no attachments were requested.
    """
    occurrence: Awb0Element = None
    attachedObjects: List[AttachedObjectInfo] = ()


@dataclass
class AttachedDataCriteria(TcBaseObj):
    """
    'AttachedDataCriteria' specifies which atachments of occurrences or the attachments of the underlying persisted
    occurrence model, to return with each resulting occurrence. The TC_relation objects specified here are traversed to
    retrieved attached objects for each occurrence.
    
    :var relationName: The relation to traverse from the Archetype for fetching attached data
    :var attachedObjectType: The type of the attached object to traverse to using the above relation
    :var namedReferences: Specific Named Reference to return in the attached object. Applies only if the attached
    object is an Dataset. If not named references are specified, all named references are returned.
    :var returnAttachedObject: If true, the attached object is returned in output.
    :var returnNamedRefObject: If true, the named reference object is returned as part of output.
    :var returnFileTickets: If true, the file tickets for the given named ref object is returned in the output.
    """
    relationName: str = ''
    attachedObjectType: str = ''
    namedReferences: List[str] = ()
    returnAttachedObject: bool = False
    returnNamedRefObject: bool = False
    returnFileTickets: bool = False


@dataclass
class AttachedObjectInfo(TcBaseObj):
    """
    'AttachedObjectInfo' returns attached objects as requested by the 'AttachedDataCriteria'.
    
    :var relationName: Relation for the attached object
    :var attachedObject: Attached Object. Null if this was not requested in the criteria
    :var namedReferenceName: Named Reference Name. This will be empty if the attached object is not an dataset or if
    named references were not requested.
    :var namedRefObject: Named Reference Object. This will be null if the attached object is not an dataset or if the
    named reference object was not requested.
    :var fileTicket: File Ticket for the Named Reference Object. This will be empty if the attached object is not an
    dataset or if the named reference object is not an ImanFile.
    """
    relationName: str = ''
    attachedObject: BusinessObject = None
    namedReferenceName: str = ''
    namedRefObject: BusinessObject = None
    fileTicket: str = ''


@dataclass
class ProductInfoData(TcBaseObj):
    """
    This structure contains the Awb0ProductContextInfo and the root Awb0Element for the product.
    
    :var productCtxInfo: The configuration of the product saved in the Awb0SavedBookmark or Awb0AutoBookmark.
    :var rootElement: The root Awb0Element of the product.
    """
    productCtxInfo: Awb0ProductContextInfo = None
    rootElement: Awb0Element = None


@dataclass
class ProductOccurrencesInput(TcBaseObj):
    """
    The 'GetOccurrencesInProduct' supplies the product and the configuration rules to use to configure the product and
    get back a page of occurrences. Optionally, filters and sorting criteria may be provided to filter or sort the
    resulting occurrences. You may also optionally supply criteria to bring back attachments that may be attached to
    occurrences with a TC_relation.
    
    :var product: The product which needs to be configured. Could be an ItemRev, CollaborativeDesign or a
    StructureContextObject.
    
     If Structure Context is passed in, the configuration below need not be specified ( the configuration information
    is ignored if this is specified ).
    :var inputCtxt: Common input context including filter, configuration, attached data criteria and page size.
    :var firstLevelOnly: If true, only the first level instances are returned.
    """
    product: BusinessObject = None
    inputCtxt: InputContext = None
    firstLevelOnly: bool = False


@dataclass
class SearchFilter(TcBaseObj):
    """
    'SearchFilter' specifies the details of a filter. It indicates if it is a string type, date type or numeric type of
    search filter that is to be applied to the occurrences of the requested product.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var endDateValue: The ending value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: A flag that indicates if the filter was previously selected and used to filter the search results.
    This field is populated on the service response and is ignored on the service input.
    :var startEndRange: The 'gap' used to generate the start and end values
    """
    searchFilterType: SearchFilterType = None
    stringValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class SearchFilterField(TcBaseObj):
    """
    'SearchFilterField' returns the resulting configured products found, that contain the queried object. This data
    structure also returns a cursor which can be sent back to a call to in order to rerieve more pages of results.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0


@dataclass
class SearchInput(TcBaseObj):
    """
    'SearchInput' contains input filtering criteria that will be used to filter and sort the occurrences in the
    requested product.
    
    :var searchString: The string to search for.
    :var searchFilterMap: The map containing the list of search filters for each search filter field.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response. The
    acceptable values are: "Alphabetical", "Priority".
    """
    searchString: str = ''
    searchFilterMap: SearchFilterMap = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: SearchFilterFieldSortType = None


@dataclass
class SearchSortCriteria(TcBaseObj):
    """
    'SearchSortCriteria' specifies the criteria to use to sort the results that are retrieved. It provides the field to
    sort and the direction to sort it in.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be performed - ascending or descending.
    """
    fieldName: str = ''
    sortDirection: SortDirection = None


@dataclass
class ChildOccsLoadNxtCursor(TcBaseObj):
    """
    The cusor has the information about loading the next set of child occurrences for given parents. It also has
    Awb0ProductContextInfo and input context which captures the product and configuration information.
    
    :var contextInfo: The product context associated with the occurrence.
    :var parentOccurrences: Parent occurrences for which children were desired
    :var inputCtxt: Common input context including filter, configuration, attached data criteria, page size and
    structure context object. If structure context object info given then configuration information is not required.
    :var firstLevelOnly: Return first level instances only
    :var startIndex: Cursor start position for the result occurrences returned so far
    :var endIndex: Cursor end position for the result occurrences returned so far
    :var pageSize: This indicate the number of occurrences needs to be returned.
    :var cursorData: DEPRECATED: Cursor data
    """
    contextInfo: Awb0ProductContextInfo = None
    parentOccurrences: List[Awb0Element] = ()
    inputCtxt: InputContext = None
    firstLevelOnly: bool = False
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0
    cursorData: List[str] = ()


@dataclass
class ChildOccurrenceInfo(TcBaseObj):
    """
    The list of child occurrences for a given parent. It also has the information about the paging position of the
    given list of occurrences. The paging position has values 'startReached', 'endReached' to identify the position and
    supports two way scrolling. Optionally the 'focusOccurrence' used to search a particular object of Awb0Element.
    
    :var contextInfo: The product context info associated with the occurrence.
    :var parent: Parent occurrence for which children were desired.
    :var startReached: Reached the first page of occurrences
    :var endReached: Reached the last page of occurrences
    :var childOccurrences: One page of child occurrences.
    :var focusOccurrence: The Awb0Element objects for given focussedOccurrence or for gievn focussedOccId.
    """
    contextInfo: Awb0ProductContextInfo = None
    parent: Awb0Element = None
    startReached: bool = False
    endReached: bool = False
    childOccurrences: List[OccurrenceInfo] = ()
    focusOccurrence: Awb0Element = None


@dataclass
class ChildOccurrenceInfoList(TcBaseObj):
    """
    The list of child Awb0Element along with Awb0ProductContextInfo containing top level product configuration
    information along with next level cursor.
    
    :var contextInfo: The product context info associated with the occurence.
    :var childOccInfos: Vector of child occurrence information for parents in a product context.
    :var cursor: Cursor that represents point to which results have been retrieved
    """
    contextInfo: Awb0ProductContextInfo = None
    childOccInfos: List[ChildOccurrenceInfo] = ()
    cursor: ChildOccsLoadNxtCursor = None


@dataclass
class ChildOccurrencesData(TcBaseObj):
    """
    The information required to get  the child occurrences including list of parent occurrences, input context and flag
    to indicate one level or all levels.
    
    :var parentOccurrences: Occurrences for which children are desired.
    :var inputCtxt: Common input context including filter, configuration, attached data criteria and page size.
    :var firstLevelOnly: If true, only the first level instances are returned.
    :var startFreshNavigation: When set to true Awb0Element with latest information is retrieved. Otherwise existing
    information at Teamcenter server is used.
    :var cloneStableIdChains: List of clone stable id in top-down fashion.  The chain is separated by "/". This field
    is considered only when parentOccurrences is empty.
    """
    parentOccurrences: List[Awb0Element] = ()
    inputCtxt: InputContext = None
    firstLevelOnly: bool = False
    startFreshNavigation: bool = False
    cloneStableIdChains: List[str] = ()


@dataclass
class ChildOccurrencesResp(TcBaseObj):
    """
    The list of child occurrences along with the product context information.
    
    :var output: Vector of child occurrence information for given parents.
    :var serviceData: Service Data
    """
    output: List[ChildOccurrenceInfoList] = ()
    serviceData: ServiceData = None


@dataclass
class InfoForAddElemData(TcBaseObj):
    """
    This structure contains information to identify type that can be added as child of input parentElement or
    productContext.
    
    :var parentElement: Awb0Element under which another Awb0Element to be added as child. This is specified if
    Awb0Element needs to be added under parent context. This is optional parameter.
    :var productContext: Awb0ProductContextInfo of the product in which Awb0Element to be added.
    :var configurationInfo: Configuration information containing RevisionRule, VariantRule, Effectivity information.
    This is used to identify adapter to use for request.
    """
    parentElement: Awb0Element = None
    productContext: Awb0ProductContextInfo = None
    configurationInfo: OccurrenceCnfgInfo = None


@dataclass
class InfoForAddElemResp(TcBaseObj):
    """
    This structure contains allowable child type name, mapped Awb0Element type name and type name to be searched
    through Full Text Search.
    
    :var preferredTypeInfo: Prefrred type information to create Awb0Element.
    :var allowedTypeInfos: List of all allowed types to create and add Awb0Element as child.
    :var preferredExists: true if preferred type is found for input Awb0Element or Awb0ProductContextInfo, false
    otherwise.
    :var serviceData: The service data containing partial error if any.
    """
    preferredTypeInfo: InfoForElementCreation = None
    allowedTypeInfos: List[InfoForElementCreation] = ()
    preferredExists: bool = False
    serviceData: ServiceData = None


@dataclass
class InfoForAddToBookmarkResp(TcBaseObj):
    """
    This structure contains reference to the list of allowable types for creating a product in a Awb0SavedBookmark.
    
    :var allowedTypeInfos: List of all allowed types.
    :var serviceData: The ServiceData containing partial error if any.
    """
    allowedTypeInfos: List[InfoForElementCreation] = ()
    serviceData: ServiceData = None


@dataclass
class InfoForElementCreation(TcBaseObj):
    """
    Object contains allowable business object type name, its mapped Awb0Element type name and type name to be searched
    through Full Text Search.
    
    :var objectTypeName: Awb0Element type name corresponding to objectTypeName.
    :var elementTypeName: Type name for which Awb0Element is instance of in product.
    :var isSearchable: Indicates if the object can be searched through Full Text Search.
    :var searchTypeName: Type name to used to search in Full Text Search. Empty in case if isSearchable is false.
    """
    objectTypeName: str = ''
    elementTypeName: str = ''
    isSearchable: bool = False
    searchTypeName: str = ''


@dataclass
class InputContext(TcBaseObj):
    """
    'InputContext' contains criteria to configure product and retrieve associated data.  This includes occurrence
    filters, configuration info which includes revision and variant configurations product context info, which is
    passed as input from the user if exist. Optionally user can pass StructureContext, which encapsulate product and
    configuration information. If structure context  object given as input then the product and configuration
    information from occurrence configuration is ignored.
    
    :var filter: Specifies a way to filter occurrences in the Product
    :var configuration: Configuration to apply to the product while fetching occurrences.
    :var attachedDataCriteria: Specifies the objects attached to the archetype that need to be returned along with the
    occurrences.
    :var pageSize: Number of occurrences to be fetched per call
    :var structureContextObject: This holds reference to structure context object, which further references
    configuration context and content objects which could be Item, ItemRevision or AppearanceGroup.
    If structureContextObject object is given in input the product and configuration context are optional.
    :var productContext: This indiactes the productContext information, this represent the product along with the
    configuration information.
    :var requestPref: Map of preference names and value pairs (string/string). Allowed preference names are
    includeInterfaces, includeUnconfigured, depthFirst and useGlobalRevRule. Allowed values are true/false. Keys and
    values are case sensitive.
    :var updateAutoBookmark: Update the bookmark state based on the input from this service.
    """
    filter: OccurrenceFilter = None
    configuration: OccurrenceCnfgInfo = None
    attachedDataCriteria: List[AttachedDataCriteria] = ()
    pageSize: int = 0
    structureContextObject: BusinessObject = None
    productContext: Awb0ProductContextInfo = None
    requestPref: RequestPreference = None
    updateAutoBookmark: bool = False


@dataclass
class InsertLevelInputData(TcBaseObj):
    """
    Structure represents the parameters required to insert a parent for the given set of objects.
    
    :var clientId: A unique string supplied by the caller. This is used to identify return data elements and partial
    errors associated with this input structure.
    :var elements: List of Awb0Element objects which the user intends to group and create a new parent for.
    :var object: Business object for which a Awb0Element is to be created and inserted as parent of the given
    Awb0Element objects.
    """
    clientId: str = ''
    elements: List[Awb0Element] = ()
    object: Item = None


@dataclass
class InsertLevelResponse(TcBaseObj):
    """
    Structure represents the output of the operation.
    
    :var output: A list of InsertLevelResponseData structures.
    :var serviceData: The Service Data.
    """
    output: List[InsertLevelResponseData] = ()
    serviceData: ServiceData = None


@dataclass
class InsertLevelResponseData(TcBaseObj):
    """
    Structure represents the output of the operation.
    
    :var clientId: The clientId from the input InsertLevelInputData element. This value is unchanged from the input,
    and can be used to identify this response element with the corresponding input element.
    :var newParent: The Awb0Element  object which is the new inserted parent object of the given set of objects.
    :var newElements: The list of newly created Awb0Element objects as a result of the insertion operation.
    """
    clientId: str = ''
    newParent: Awb0Element = None
    newElements: List[Awb0Element] = ()


@dataclass
class NxtChildOccurrencesData(TcBaseObj):
    """
    The information required to get  the next or previous set of child occurrences of an given parent occurrence(s).
    
    :var cursor: Cursor that represents point to which results have been retrieved
    :var goForward: Direction to navigate to fetch the next page of occurrences
    """
    cursor: ChildOccsLoadNxtCursor = None
    goForward: bool = False


@dataclass
class NxtOccsInProdData(TcBaseObj):
    """
    The 'NxtOccsInProdData' supplies the cursor from a previous call, as input to get the next page of result
    occurrences data. The cursor may have been received from a previous call to either get a first page using
    'getOccurrencesInProduct', or a subsequent page by calling 'getNextOccurrencesInproduct'. The same cursor must be
    passed in as input, as part of 'NxtOccsInProdData' in the subsequent call to  'getNextOccurrencesInproduct'. The
    cursor received from that subsequent call must be passed in to the following invocation to get the following page
    of occurrences, and so on until there is no more data to fetch.
    
    :var cursor: Cursor that represents point to which search results have been retrieved
    :var goForward: Direction to navigate to fetch the next page of occurrences
    """
    cursor: OccsInProdLoadNxtCursor = None
    goForward: bool = False


@dataclass
class OccsInProdLoadNxtCursor(TcBaseObj):
    """
    'OccsInProdLoadNxtCursor' is a cursor that is returned for use as input in calls to 'getNextOccurrencesInProduct'
    to retrieve the next page of search results. This data structure must not be modified by the caller, but passed
    back as is, to the next service call to 'getNextOccurrencesInProduct'. This cursor is received as output inside
    'OccsInProdResp' when a call to 'getNextOccurrencesInProduct' or 'getNextOccurrencesInProduct' is made.
    
    :var contextInfo: The product context info associated with the occurence.
    :var product: End product where the input archetype is used or in context of which the search was performed
    :var inputCtxt: Common input context including filter, configuration, attached data criteria and page size.
    :var firstLevelOnly: Return first level instances only
    :var cursorData: DEPRECATED: Cursor data
    :var startIndex: Cursor start position for the result occurrences returned so far
    :var endIndex: Cursor end position for the result occurrences returned so far
    :var pageSize: This indicate the number of occurrences needs to be returned.
    """
    contextInfo: Awb0ProductContextInfo = None
    product: BusinessObject = None
    inputCtxt: InputContext = None
    firstLevelOnly: bool = False
    cursorData: List[str] = ()
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0


@dataclass
class OccsInProdResp(TcBaseObj):
    """
    'OccsInProdResp' contains the resulting occurrences found for each product from which retrieval was requested. This
    data structure also returns a cursor for each product, which can be sent back to the subsequent call to
    'getNextOccurrencesInProduct' in order to rerieve more pages of results.
    
    :var data: Response data for each input.
    :var serviceData: Service data
    """
    data: List[OccsInProdRespData] = ()
    serviceData: ServiceData = None


@dataclass
class OccsInProdRespData(TcBaseObj):
    """
    'OccsInProdRespData' contains the resulting occurrences found in the configured product, filtered and sorted by the
    criteria requested in the input to the service. This data structure also returns a cursor which can be sent back to
    a call to in order to rerieve more pages of results.
    
    :var productContextInfo: The Occurrence Context Information
    :var occurrences: One page of occurrences in the product.
    :var rootOccurrence: The information on the root occurrence in the product. This occurrence is only returned if all
    occurrences are requested in the product.
    :var cursor: Cursor that represents point to wich the search results have been fetched.
    :var startReached: Reached the first page of occurrences
    :var endReached: Reached the last page of occurrences
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var searchFilterMap: The map containing the list of search filters for each search filter field based on the
    search results.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    """
    productContextInfo: Awb0ProductContextInfo = None
    occurrences: List[OccurrenceInfo] = ()
    rootOccurrence: OccurrenceInfo = None
    cursor: OccsInProdLoadNxtCursor = None
    startReached: bool = False
    endReached: bool = False
    searchFilterCategories: List[SearchFilterField] = ()
    searchFilterMap: SearchFilterMap = None
    defaultFilterFieldDisplayCount: int = 0


@dataclass
class OccurrenceCnfgInfo(TcBaseObj):
    """
    'OccurrenceCnfgInfo' specifies the complete set of configuration rules including RevisionRule objects , Effectivity
    and VariantRule that need to be applied to the input product to configure it in order to retrieve the requested
    occurrence data.
    
    :var revisionRule: Revision Rule
    :var effectivityDate: Effectivity Date to use.
    :var now: Use Now for Effectivity Date Configuration.
    :var endItem: End Item to use for Unit Effectivity
    :var unitNo: Unit Effectivity
    :var variantRule: Variant Rule.
    :var configurationObject: Configuration Object like Configuration Context.  The other configuration information
    above is ignored if this is specified.
    :var svrOwningProduct: This indicates the product ( ItemRevision or CollaborativeDesign ), associated with the
    saved VariantRule.
    """
    revisionRule: RevisionRule = None
    effectivityDate: datetime = None
    now: bool = False
    endItem: BusinessObject = None
    unitNo: int = 0
    variantRule: VariantRule = None
    configurationObject: BusinessObject = None
    svrOwningProduct: BusinessObject = None


class SearchFilterFieldSortType(Enum):
    """
    'SearchFilterFieldSortType' is an enumeration to determine how fields used in filters need to be sorted. The fields
    can be sorted alphabetically in ascending order or in priority order from highest to lowest.
    """
    Alphabetical = 'Alphabetical'
    Priority = 'Priority'


class SearchFilterType(Enum):
    """
    An enumeration for different types of search filters like string, date, numeric.
    """
    StringFilter = 'StringFilter'
    DateFilter = 'DateFilter'
    NumericFilter = 'NumericFilter'


class SortDirection(Enum):
    """
    An enumeration indicating whether the sorting needs to be performed in ascending or descending order.
    """
    ASC = 'ASC'
    DESC = 'DESC'


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive. The allowed preference names are 'includeInterfaces, depthFirst'. The allowed values are 'True/False'.
"""
RequestPreference = Dict[str, List[str]]


"""
'SearchFilterMap' is a map containing the list of search filters for each search filter field based on the search results.
"""
SearchFilterMap = Dict[str, List[SearchFilter]]
