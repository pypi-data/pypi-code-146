from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, VariantRule, Effectivity, RevisionRule, Awb0Element, Awb0ProductContextInfo, ItemRevision
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_07.OccurrenceManagement import EffectivityRange, OccurrenceFilterInput
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OccurrenceInfo5(TcBaseObj):
    """
    OccurrenceInfo5 is the information about one occurrence that is returned as part of the result. It contains an
    occurrence that is part of the configured structure being queried and that passes the filter criteria, as well as
    the attachments requested.
    
    :var occurrence: Instance of the Awb0Element.
    :var productContext: The Awb0ProductContextInfo for the occurrence. If NULL then configuration context is same as
    that of nearest parent occurrence having non-null value.
    """
    occurrence: Awb0Element = None
    productContext: Awb0ProductContextInfo = None


@dataclass
class PagedOccurrencesInfo6(TcBaseObj):
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
    childOccurrences: List[OccurrenceInfo5] = ()
    focusOccurrence: Awb0Element = None
    productContext: Awb0ProductContextInfo = None
    cursor: ChildOccsLoadNxtCursor5 = None
    startReached: bool = False
    endReached: bool = False


@dataclass
class ChildOccsLoadNxtCursor5(TcBaseObj):
    """
    The cusor has the information about loading the next set of child occurrences for given parents. It also has
    Awb0ProductContextInfo and input context which captures the product and configuration information.
    
    :var pageSize: This indicate the number of occurrences needs to be returned.
    :var productContext: The product context associated with the occurrence.
    :var firstLevelOnly: If true, retrieve first level occurrences only.Otherwise occurrences from multiple level to be
    retreived.
    :var parentOccurrences: Parent occurrences for which children were desired.
    :var inputCtxt: Common input context including filter, configuration, attached data criteria, page size and
    structure context object. If structure context object info is given then configuration information is not required.
    :var startIndex: Cursor start position for the result occurrences returned so far.
    :var endIndex: Cursor end position for the result occurrences returned so far.
    :var cursorData: Cursor data
    :var startOccUid: UID of the first object of the result occurrences. This is used for flat mode.
    :var endOccUid: UID of the last object of the result occurrences. This is used for flat mode.
    """
    pageSize: int = 0
    productContext: Awb0ProductContextInfo = None
    firstLevelOnly: bool = False
    parentOccurrences: List[BusinessObject] = ()
    inputCtxt: InputContext5 = None
    startIndex: int = 0
    endIndex: int = 0
    cursorData: List[str] = ()
    startOccUid: str = ''
    endOccUid: str = ''


@dataclass
class UserContextState(TcBaseObj):
    """
    This structure contains the current user's client state information for the opened object.
    
    :var openedObject: The opened object. It can be the ItemRevision, Cpd0CollaborativeDesign) or Awb0SavedBookmark
    object. The client state information like active tab, selected Awb0Element will be persisted for this object and
    the current user.
    :var sublocationAttributes: Map (string, list of strings) of client state attribute name and value pairs. At this
    time only one (key) attribute name is supported: "activeSublocation". Supported  values are:  (tab names like)
    "overview", "viewer". Keys and values are case in-sensitive. Content sublocation client state attributes that need
    to be persisted will be send to the client using this map.
    """
    openedObject: BusinessObject = None
    sublocationAttributes: SublocationAttributes = None


@dataclass
class EffectivityCreateInput(TcBaseObj):
    """
    This structure contains input to create Effectivity object for the 'element'.
    
    :var element: Awb0Element to which effectivity to be associated.
    :var effectivityInfo: Information to create Effectivity object.
    """
    element: Awb0Element = None
    effectivityInfo: EffectivityInfo = None


@dataclass
class EffectivityEditInput(TcBaseObj):
    """
    This structure contains input to update Effectivity object for the 'element'.
    
    :var element: Awb0Element to which effectivity to be associated.
    :var effectivity: The effectivity object to be updated.
    :var effectivityInfo: Information to update Effectivity object.
    """
    element: Awb0Element = None
    effectivity: Effectivity = None
    effectivityInfo: EffectivityInfo = None


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    This structure contains the information required to create Effectivity.
    
    :var name: Name of the Effectivity or empty string when Effectivity should not be shared.
    :var endItemRev: Effectivity end ItemRevision.
    :var unitRangeText: Effectivity unit range, a valid range of unit numbers. Always specified in the context of the
    end Item to which the units apply. It can be a discrete, noncontinuous range.
    Valid ranges are:
      StartUnit
      StartUnit - EndUnit
      StartUnit - SO
      StartUnit - UP
            Where, StartUnit < EndUnit.
      StartUnit1 - EndUnit1, StartUnit2 - EndUnit2 (Ex. 10-12, 15-20)
            Where StartUnit2 > EndUnit1.
    All units are positive integers.
    :var dateRange: The array of effectivity date range, a valid range of dates.
    Valid ranges are:
     StartDate - EndDate
     StartDate - UP
     StartDate - SO
            Where, StartDate < EndDate and EndDate != NULL.
     StartDate1 - EndDate1, StartDate2 - EndDate2 (Ex. 01 January 2016 - 30 April 2016, 1 May 2016 - 30 July 2016)
            Where, StartDate2 > EndDate1
    :var openEndedStatus: Effectivity open ended status, 
    0 for EFFECTIVITY_closed,  
    1 for EFFECTIVITY_open_ended, 
    2 for EFFECTIVITY_stock_out.
    :var isProtected: If true, the new range is added to existing ranges, no overwrite is allowed; otherwise overwrite
    to existing ranges is allowed.
    :var isShared: If true the new Effectivity object can be shared across the different Awb0Element(s); otherwise it
    is unnamed effectivity and cannot be shared.
    """
    name: str = ''
    endItemRev: ItemRevision = None
    unitRangeText: str = ''
    dateRange: List[datetime] = ()
    openEndedStatus: int = 0
    isProtected: bool = False
    isShared: bool = False


@dataclass
class InputContext5(TcBaseObj):
    """
    'InputContext5' specifies the input information to apply to the structure from which the occurrences are to be
    retrieved. This includes configuration rules, page size of number of occurrences to fetch,  filtering and sorting
    criteria as well as criteria to fetch atachments.
    
    :var pageSize: Number of occurrences to be fetched per call.
    :var productContext: Busines Object Awb0ProductContextInfo that contains the product as well as all the
    configuration information that was passed as input to the service.
    :var configuration: A list of configuration rules to apply to the product before returning the resulting
    occurrences.
    :var filterIn: A recipe to search and filter occurrences and sort the results.
    :var occurrenceScheme: Occurrence scheme associated with product e.g Collaborative Design.
    :var changeContext: Holds the Runtime Business Object created by Server during setChangeContext2() SOA operation.
    This holds the Change Context applied and the Change Configuration Mode.
    :var requestPref: Map of preference names and value pairs (string/string). Allowed preference names are 
    includeInterfaces and includeUnconfigured. Allowed values are True/False. Keys and values are case sensitive.
    """
    pageSize: int = 0
    productContext: Awb0ProductContextInfo = None
    configuration: OccurrenceCnfgInfo5 = None
    filterIn: OccurrenceFilterInput = None
    occurrenceScheme: BusinessObject = None
    changeContext: RuntimeBusinessObject = None
    requestPref: RequestPreference5 = None


@dataclass
class OccurrenceCnfgInfo5(TcBaseObj):
    """
    OccurrenceCnfgInfo5 specifies the complete set of configuration rules including RevisionRule , Effectivity
    (provides range support) and VarianRule that need to be applied to the input product to configure it in order to
    retrieve the requested occurrence data.
    
    :var revisionRule: RevisionRule to use in order to configure the product.
    :var now: If true, specifies that the product be configure by the date that is now.
    :var effectivityDate: Specifies the date Effectivity to use in order to configure the product.
    :var unitNo: Unit number to use in order to configure the product.
    :var endItem: Specifies the endItem which governs the  unit effectivity.
    :var variantRule: VariantRule to use in order to configure the product.
    :var svrOwningProduct: This indicates the product ( ItemRevision or CollaborativeDesign ), associated with the
    saved VariantRule.
    :var effectivityRanges: List of range effectivity related data.
    """
    revisionRule: RevisionRule = None
    now: bool = False
    effectivityDate: datetime = None
    unitNo: int = 0
    endItem: BusinessObject = None
    variantRule: VariantRule = None
    svrOwningProduct: BusinessObject = None
    effectivityRanges: List[EffectivityRange] = ()


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive. The allowed preference names are includeInterfaces. The allowed values are True/False.
"""
RequestPreference5 = Dict[str, List[str]]


"""
Map (string, list of string) of client state attribute name and value pairs. At this time only one (key) attribute name is supported: "activeSublocation". Supported  values are:  (tab names like) "overview", "viewer" . Keys and values are case in-sensitive.
"""
SublocationAttributes = Dict[str, List[str]]
