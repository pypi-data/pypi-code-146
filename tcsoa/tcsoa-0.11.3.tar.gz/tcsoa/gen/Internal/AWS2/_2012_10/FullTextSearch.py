from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awp0FullTextSavedSearch
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FullTextSavedSearchInput(TcBaseObj):
    """
    Input structure of createFullTextSavedSearch SOA
    
    :var clientId: Client Id
    :var savedSearchName: Saved search name
    :var searchString: Search string
    :var searchFilterMap: Search filter map
    """
    clientId: str = ''
    savedSearchName: str = ''
    searchString: str = ''
    searchFilterMap: SearchFilterMap = None


@dataclass
class FullTextSearchInput(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var searchString: The string to search for.
    :var startIndex: The index from which to start the search.
    :var maxToReturn: The maximum number of objects to return.
    :var maxToLoad: The maximum number of objects to load.
    :var searchFilterMap: The map containing the list of search filters for each search filter field.
    :var searchSortCriteria: The criteria to use to sort the results.
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response. The
    acceptable values are: "Alphabetical", "Priority".
    :var attributesToInflate: The list of attributes to inflate.
    """
    searchString: str = ''
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: SearchFilterMap = None
    searchSortCriteria: List[SearchSortCriteria] = ()
    searchFilterFieldSortType: SearchFilterFieldSortType = None
    attributesToInflate: List[str] = ()


@dataclass
class FullTextSearchResponse(TcBaseObj):
    """
    A service response structure containing search results.
    
    :var searchResults: The list of business objects obtained after performing a search.
    :var totalFound: The total number of business objects found.
    :var totalLoaded: The total number of business objects loaded.
    :var searchFilterMap: The map containing the list of search filters for each search filter field based on the
    search results.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var serviceData: The service data object.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap: SearchFilterMap = None
    searchFilterCategories: List[SearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    serviceData: ServiceData = None


@dataclass
class GetAddedObjectsToUpdateIndexResponse(TcBaseObj):
    """
    The service response structure containing UIDs of added objects to update the full text search index.
    
    :var uidsAddedObjects: The list containing UIDs of added objects to update the full text search index.
    :var serviceData: The service data object.
    """
    uidsAddedObjects: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetAddedObjectsToUpdateIndexResponse1(TcBaseObj):
    """
    The service response structure containing UIDs of added objects to update the full text search index. Also includes
    the date and time at which the query is executed to find the data.
    
    :var uidsAddedObjects: The list containing UIDs of added objects to update the full text search index.
    :var queriedDateTime: The data and time at which the added objects are queried for. Require this to keep track of
    sync case.
    :var serviceData: the service data object.
    """
    uidsAddedObjects: List[str] = ()
    queriedDateTime: datetime = None
    serviceData: ServiceData = None


@dataclass
class GetDatasetIndexableFilesInfoResponse(TcBaseObj):
    """
    The response structure with dataset(s) file information map.
    
    :var dsFileInfosMap: Map conatining datasets file information.
    :var serviceData: Service Data
    """
    dsFileInfosMap: DatasetFileTicketInfosMap = None
    serviceData: ServiceData = None


@dataclass
class GetDeletedObjectsToUpdateIndexResponse(TcBaseObj):
    """
    The service response structure containing UIDs of deleted objects to update the full text search index.
    
    :var uidsDeletedObjects: The list containing UIDs of deleted objects to update the full text search index.
    :var serviceData: The service data object.
    """
    uidsDeletedObjects: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetDeletedObjectsToUpdateIndexResponse1(TcBaseObj):
    """
    The service response structure containing UIDs of deleted objects to update the full text search index.  Also
    contains the date and time at which the deleted objects are queried for.
    
    :var uidsDeletedObjects: List of UIDs of deleted objects to update the full text search index.
    :var queriedDateTime: Date including time at which the deleted objects are queried for. This value will be used for
    sync use cases.
    :var serviceData: The service data object.
    """
    uidsDeletedObjects: List[str] = ()
    queriedDateTime: datetime = None
    serviceData: ServiceData = None


@dataclass
class GetImpactedItemRevsForReIndexResponse(TcBaseObj):
    """
    The service response structure holds the impacted ItemRevision UIDs for which the revision rule selectors
    information need to be updated in full text search index.
    
    :var impactedObjectsUIDs: List that contains the impacted ItemRevision UIDs due to adds/modify/deletes that
    happened after last time index.
    :var serviceData: The Service Data
    """
    impactedObjectsUIDs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class GetObjectsToIndexResponse(TcBaseObj):
    """
    A response structure containing a list of objects to index.
    
    :var objectsToIndexResults: The list of objects to index.
    :var serviceData: The service data object.
    """
    objectsToIndexResults: List[ObjectsToIndexResult] = ()
    serviceData: ServiceData = None


@dataclass
class GetTcObjectsToIndexInput(TcBaseObj):
    """
    The input to get the objects to index.
    
    :var dateTimeRanges: The date/time ranges to query on.
    """
    dateTimeRanges: List[DateTimeRange] = ()


@dataclass
class ObjectsToIndexResult(TcBaseObj):
    """
    A structure containing the list of objects to index within a date/time range.
    
    :var dateTimeRange: The date/time range for the list of objects returned.
    :var objectUIDsForRange: The list of object UIDs within a specific date/time range.
    """
    dateTimeRange: DateTimeRange = None
    objectUIDsForRange: List[str] = ()


@dataclass
class PreFiltersProperty(TcBaseObj):
    """
    Pre filters property internal, display name and its values.
    
    :var internalName: PreFilter Property internal name.
    :var displayName: PreFilters property display name.
    :var values: Vector of PreFilter values
    """
    internalName: str = ''
    displayName: str = ''
    values: List[PreFiltersValue] = ()


@dataclass
class PreFiltersResponse(TcBaseObj):
    """
    List of PreFilters and their values.
    
    :var properties: Vector of PreFilter properties.
    :var serviceData: The service data object.
    """
    properties: List[PreFiltersProperty] = ()
    serviceData: ServiceData = None


@dataclass
class PreFiltersValue(TcBaseObj):
    """
    Internal and display value of the prefilter.
    
    :var internalName: Filter value internal name.
    :var displayName: Filter value display name.
    """
    internalName: str = ''
    displayName: str = ''


@dataclass
class SearchFilter(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
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
    A structure containing details about a search filter field.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0


@dataclass
class SearchSortCriteria(TcBaseObj):
    """
    The criteria to use to sort the results.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be perfomed - ascending or descending.
    """
    fieldName: str = ''
    sortDirection: SortDirection = None


@dataclass
class SearchSuggestionsInput(TcBaseObj):
    """
    A structure containing input data to retrieve search suggestions.
    
    :var searchString: The string to search for.
    :var maxCount: The maximum number of suggestions to return.
    """
    searchString: str = ''
    maxCount: int = 0


@dataclass
class SearchSuggestionsResponse(TcBaseObj):
    """
    A response structure containing a list of suggestions.
    
    :var suggestions: The list of search suggestions.
    :var serviceData: The service data object.
    """
    suggestions: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateIndexerStatusInput(TcBaseObj):
    """
    Input required to keep track of the exported data for further sync cases.
    
    :var applicationId: Application ID used to perform the action during Export/Sync process.
    :var lastProcessedDate: Last proceesed date of the action.
    """
    applicationId: str = ''
    lastProcessedDate: datetime = None


@dataclass
class CreateFullTextSavedSearchResponse(TcBaseObj):
    """
    Response from createFullTextSavedSearch SOA
    
    :var output: Map from client Id to created FullTextSavedSearch object
    :var serviceData: Service data
    """
    output: CreateFullTextSavedSearchOutput = None
    serviceData: ServiceData = None


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    Structure containing the datasets file information.
    
    :var fileUID: Unique Identifier of the file.
    :var fmsFileTicket: FMS read file ticket for the file to be downloaded.
    :var fileName: Original File name
    :var isText: Flag to indicate of the file is text(TRUE) or binary (FALSE) file type.
    """
    fileUID: str = ''
    fmsFileTicket: str = ''
    fileName: str = ''
    isText: bool = False


@dataclass
class DateTimeRange(TcBaseObj):
    """
    A pair of DateTime objects representing the start and end date/time.
    
    :var startDate: The starting date/time value.
    :var endDate: Then ending date/time value.
    """
    startDate: datetime = None
    endDate: datetime = None


@dataclass
class FindFullTextSavedSearchesResponse(TcBaseObj):
    """
    Response from FindFullTextSavedSearches SOA
    
    :var mySavedSearches: My saved searches
    :var sharedSavedSearches: Shared saved searches
    :var serviceData: Service data
    """
    mySavedSearches: List[Awp0FullTextSavedSearch] = ()
    sharedSavedSearches: List[Awp0FullTextSavedSearch] = ()
    serviceData: ServiceData = None


class SearchFilterFieldSortType(Enum):
    """
    An enumeration to determine how fields used in filters need to be sorted. The fields can be sorted alphabetically
    in ascending order or in priority order from highest to lowest.
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
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap = Dict[str, List[SearchFilter]]


"""
Map from Client Id to created FullTextSavedSearch object
"""
CreateFullTextSavedSearchOutput = Dict[str, Awp0FullTextSavedSearch]


"""
Map whoose key is the dataset UID and value is the vector of DatasetFileInfo objects.
"""
DatasetFileTicketInfosMap = Dict[str, List[DatasetFileInfo]]
