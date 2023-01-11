from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0ProductContextInfo
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OccurrenceFilterInput(TcBaseObj):
    """
    'OccurrenceFilterInput' specifies the information about recipe to search and filter the result.
    
    :var recipe: Recipe to provide search criteria.
    :var searchFilterCategories: A list of search filter categories.
    :var searchFilterMap: A map (string,list of SearchFilter)  containing the list of search filters for each search
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
    searchFilterCategories: List[SearchFilterField2] = ()
    searchFilterMap: SearchFilterMap2 = None
    searchSortCriteria: List[SearchSortCriteria2] = ()
    searchFilterFieldSortType: str = ''
    fetchUpdatedFilters: bool = False


@dataclass
class OccurrenceFilterOutput(TcBaseObj):
    """
    OccurrenceFilterOutput specifies the output search criteria and updated filters.
    
    :var recipe: Updated recipe including the user specified filters that were provided in OccurrenceFilterInput.
    :var searchFilterCategories: A list of search filter categories.
    :var searchFilterMap: A map ( String, list of SearchFilter2 ) of search filter categories ( String ) with their
    corrosponding list of search filters ( SearchFilter2 ). Valid keys are' Ptn0PartitionScheme' and 'Design Component'.
    :var defaultCategoryDisplayCount: Number of categories display count.
    """
    recipe: List[Criteria] = ()
    searchFilterCategories: List[SearchFilterField2] = ()
    searchFilterMap: SearchFilterMap2 = None
    defaultCategoryDisplayCount: int = 0


@dataclass
class SearchFilter2(TcBaseObj):
    """
    'SearchFilter2' specifies the details of a filter. It indicates if it is a string, date or numeric type of search
    filter that is to be applied to the occurrences of the requested product.
    
    :var searchFilterType: The type of search filter to apply. Valid values are "StringFilter", "DateFilter",
    "NumericFilter" and  "HeirarchialFilter".
    :var stringValue: This specifies the internal text string value to filter by.
    :var startEndRange: The 'gap' used to generate the start and end values
    :var stringDisplayValue: This specifies the display value of the filter.
    :var startDateValue: The starting value for a date filter. This field is applicable only if the 'searchFilterType'
    field is set to "DateFilter".
    :var endDateValue: The ending value for a date filter. This field is applicable only if the 'searchFilterType'
    field is set to "DateFilter".
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    'searchFilterType' field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the
    'searchFilterType' field is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: A flag that indicates if the filter was previously selected and used to filter the search results.
    This field is populated on the service response and is ignored on the service input.
    :var hasChildren: A flag indicating if the filter has children.
    """
    searchFilterType: str = ''
    stringValue: str = ''
    startEndRange: str = ''
    stringDisplayValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    hasChildren: bool = False


@dataclass
class SearchFilterField2(TcBaseObj):
    """
    'SearchFilterField2' contains the resulting configured products found, that contain the queried object. This data
    structure also returns a cursor which can be sent back to a call to in order to rerieve more pages of results.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    :var editable: If true, UI renders an editable text box instead of filter values. E.g. when 'categoryType' is
    "Attribute", in UI instead of displaying filter value a text field should be rendered.
    :var quickSearchable: If true, UI rendes a quick search text box. E.g. when 'categoryType' is "Partition", in UI a
    quick search text box is rendered along with all filter values.
    :var categoryType: The type of the filter category. Valid values are "StringMatch",  "Partition", "Attribute" 
    ,"ClosureRule", "SelectedElement"," BoxZone", "Proximity"," PlaneZone"
    :var isHierarchical: A boolean to indicate if hiearchical display is required for the filter values that belong to
    this categroy. If true, the filter values must have a hiearchical display in the client. Otherwise the filter
    values are shown as a flat list. Default value of this parameter is false.
    :var isMultiSelect: If true, multiple filters can be selected within this category. Otherwise only single filter
    can be selected. Default value of this parameter is true.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0
    editable: bool = False
    quickSearchable: bool = False
    categoryType: str = ''
    isHierarchical: bool = False
    isMultiSelect: bool = False


@dataclass
class SearchSortCriteria2(TcBaseObj):
    """
    'SearchSortCriteria2' specifies the criteria to use to sort the results that are retrieved. It provides the field
    to sort and the direction to sort it in.
    
    :var fieldName: The name of the field to perform the sorting on. This has to be the name of a property of an
    Awb0Element or its subtype on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be perfomed. It could be ascending or descending.
    Valid values are "ASC" and "DESC".
    """
    fieldName: str = ''
    sortDirection: str = ''


@dataclass
class SubsetResponse(TcBaseObj):
    """
    SubsetResponse contains a output subset recipe and filters for every given product context input.
    
    :var filterOut: A list of filter comprising the recipes and filters for the given Awb0ProducContextInfo.
    :var serviceData: Contains the list of all BusinessObject(s) that make up the output, as well as any errors that
    might have ocurred as part of the service invocation.
    """
    filterOut: List[OccurrenceFilterOutput] = ()
    serviceData: ServiceData = None


@dataclass
class Criteria(TcBaseObj):
    """
    'Criteria' provides information about recipe to search occurrences in a product.
    
    :var criteriaType: The type of search criteria represented in this structure. The list of valid values are: 
    - Attribute: Indicates a property based search term
    - BoxZone: Indicates a type of spatial search term
    - PlaneZone: Indicates a type of spatial search term
    - Proximity: Indicates a type spatial search term
    - ClosureRule: Indicates a closure rule search term
    - Group: Indicates a groups of multiple search terms
    - Partition: Indicates a partition based search term
    
    
    :var criteriaValues: A list of internal values used within this search term.
    :var criteriaDisplayValue: A user-friendly string representation of this search term.
    :var criteriaOperatorType: The search term operator indicating the logic for combining this search term. The list
    of valid values are:
    - Include (OR)
    - Filter (AND)
    - Exclude (NOT)
    
    
    :var subCriteria: A grouping of multiple search terms. This will be empty if the recipe contains no groups.
    """
    criteriaType: str = ''
    criteriaValues: List[str] = ()
    criteriaDisplayValue: str = ''
    criteriaOperatorType: str = ''
    subCriteria: List[Criteria] = ()


@dataclass
class EffectivityRange(TcBaseObj):
    """
    Structure to hold a row of effectivity data.
    
    :var unitIn: Unit at which this validity range starts. Valid value is non zero positive integer number.
    :var unitOut: Unit at which this validity range ends. Valid value is non zero positive integer number. Maximum
    value can be 2147483646 ( SO ) or 2147483647 ( UP ).
    :var dateIn: Date at which this validity range starts.
    :var dateOut: Date at which this validity range ends. Maximum value can be 26th Dec 9999 00:00:00 ( SO ) or 30th
    Dec 9999 00:00:00 ( UP ) in UTC timezone.
    """
    unitIn: int = 0
    unitOut: int = 0
    dateIn: datetime = None
    dateOut: datetime = None


@dataclass
class FilterSearchCriteria(TcBaseObj):
    """
    'FilterSearchCriteria' provides information related to the value entered in search filter field, as well as the
    category related details.
    
    :var categoryType: The category type under which search is requested. Valid values are:" Partition", "Attribute" ,
    "ClosureRule", "SelectedElement", "BoxZone", "Proximity", "PlaneZone"," StringMatch".
    :var categoryInternalName: The name of the category.
    :var searchString: User entered search text for finding the filters.
    """
    categoryType: str = ''
    categoryInternalName: str = ''
    searchString: str = ''


@dataclass
class FindMatchingFilterInput(TcBaseObj):
    """
    Input for 'findMatchingFilters'.
    
    :var productInfo: product context info.
    :var appliedCriteria: List of criteria which are already applied. This list is used to set selected parameter in
    returned SearchFilter2.
    :var searchCriteria: search criteria
    """
    productInfo: Awb0ProductContextInfo = None
    appliedCriteria: List[Criteria] = ()
    searchCriteria: FilterSearchCriteria = None


@dataclass
class FindMatchingFilterOutput(TcBaseObj):
    """
    'FindFilterOutput' provides output information related to the value entered in search filter field, as well as the
    category related details.
    
    :var searchFilterMap: Contains the map  (Filter category namestring, list of 'SearchFilter2' ) of category name to
    its display values.
    """
    searchFilterMap: SearchFilterMap2 = None


@dataclass
class FindMatchingFilterResponse(TcBaseObj):
    """
    'FindFilterResponse' contains output categories and their display values organized based on the search sort
    criteria specified in the input.
    
    :var filterOut: A list of filter output comprising the list of categories and assocaited filter values  for the
    given Awb0ProducContextInfo.
    :var serviceData: Contains the list of all BusinessObjects that make up the output, as well as any errors that
    might have ocurred as part of the service invocation.
    """
    filterOut: List[FindMatchingFilterOutput] = ()
    serviceData: ServiceData = None


"""
'SearchFilterMap2' is a map  (Filter category name, string  list of 'SearchFilter2' ) containing the list of search filters for each search filter field based on the search results.
"""
SearchFilterMap2 = Dict[str, List[SearchFilter2]]
