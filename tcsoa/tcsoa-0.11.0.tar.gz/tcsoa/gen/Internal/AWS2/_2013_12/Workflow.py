from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TaskSearchFilter(TcBaseObj):
    """
    A structure representing a string, date or numeric type of Task search filter.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter".
    An example for this input:
    
    StringFilter - User wants to search all the tasks based on any string property on EPMtask like object_type etc.
    
    DateFilter - User wants to search all the tasks based on any date property on EPMTask like due_date etc.
    
    NumericFilter - User wants to search all the tasks based on any numeric property on EPMTask like task_duration etc.
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
    :var startEndRange: The 'gap' used to generate the start and end values.
    """
    searchFilterType: str = ''
    stringValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


@dataclass
class TaskSearchFilterField(TcBaseObj):
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
class TaskSearchInput(TcBaseObj):
    """
    A structure containing input search criteria.
    
    :var startIndex: This input is used for pagination. User can specify the the start index of the next chunk of tasks
    to return. An example of this input is : User has 100 tasks in inbox and want to get tasks from 51 onwards. So here
    the startIndex would be 51.
    :var maxToReturn: This input is used for pagination. This input specifies the maximum number of found tasks to
    return.
    :var maxToLoad: This input is used for pagination. This input specifies the he maximum number of tasks to load.
    :var searchFilterMap: The map containing the list of search filters for each search filter field.This is a map of
    (string, list(TaskSearchFilter)).
    :var searchSortCriteria: The criteria to use to sort the results. Use this input to specify the EPMTask property to
    be used for sorting the search result. An example for this input is : User wants to sort the output result based on
    "last_mod_date" property etc.
    :var searchSortDirection: The criteria to decide the sort direction of the results.Valid values are "ASC", "DESC".
    :var searchFilterFieldSortType: The sorting type to use to order the search filter categories in the response.
    Valid values are "Alphabetical", "Priority".
    :var searchInboxContentType: The criteria to decide the Inbox content type for searching the tasks. Valid values
    are "AllTasks", "MyTasks" and "TasksToTrack".
    """
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
    searchFilterMap: TaskSearchFilterMap = None
    searchSortCriteria: str = ''
    searchSortDirection: str = ''
    searchFilterFieldSortType: str = ''
    searchInboxContentType: str = ''


@dataclass
class TaskSearchResponse(TcBaseObj):
    """
    A service response structure containing search results.
    
    :var searchResults: The list of business objects obtained after performing a search.
    :var totalFound: The total number of business objects found.
    :var totalLoaded: The total number of business objects loaded.
    :var searchFilterMap: The map containing the list of search filters for each search filter field based on the
    search results. This is a map of (string, list(TaskSearchFilter)).
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var serviceData: Service data containing found objects, errors, etc.
    """
    searchResults: List[BusinessObject] = ()
    totalFound: int = 0
    totalLoaded: int = 0
    searchFilterMap: TaskSearchFilterMap = None
    searchFilterCategories: List[TaskSearchFilterField] = ()
    defaultFilterFieldDisplayCount: int = 0
    serviceData: ServiceData = None


"""
TaskSearchFilterMap is a map of search filter name (key) and TaskSearchFilter structure(values).
"""
TaskSearchFilterMap = Dict[str, List[TaskSearchFilter]]
