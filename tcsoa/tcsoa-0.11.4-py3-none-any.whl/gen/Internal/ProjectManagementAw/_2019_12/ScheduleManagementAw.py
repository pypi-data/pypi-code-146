from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.ProjectManagementAw._2016_12.ScheduleManagementAw import EventDateRanges
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ManageProgramViewResponse(TcBaseObj):
    """
    Response containing the ProgramView data comprising the new ProgramView created for 'create' operation, the list of
    ScheduleTask objects. The day and event ranges are returned for 'load' operation.
    
    :var programView: The context ProgramView object.
    :var configuration: The ProgramView data containing the list of Schedule UIDs, filters and groups. This is
    populated only if the input options in 'ProgramViewInfo' contain 'returnProgramViewConfig' entry.
    :var dayRanges: The list of Structure (int, list of string) containing the ranges for each day in a week. Maps the
    days of the week to their ranges. The valid values for days are 0 to 6 which represents Sunday through Saturday in
    the respective order. A range is a pair of start and end time of working hours mentioned in 24-hour format. A day
    can have multiple ranges with breaks in-between in a working day. This is populated only if the input options in
    'ProgramViewInfo' contain 'returnProgramViewConfig' entry.
    :var eventDateRanges: The event dates and their respective ranges. The events are exceptions where the working
    hours are different from the default working hours. This is populated only if the input options in
    'ProgramViewInfo' contain 'returnProgramViewConfig' entry.
    :var options: It represents any additional information to be returned in the response. Valid values are: 
    hasMore : true/false (Set to true if there are more objects to be loaded; false otherwise.)
    :var programViewNodes: The list of ProgramView nodes loaded.
    :var programViewNodesJson: The list of ProgramView nodes loaded in JSON format.
    :var serviceData: The service data containing the ProgramView object in the created or updated list based on the
    operationType and ScheduleTask objects in the plain objects list.
    """
    programView: BusinessObject = None
    configuration: ProgramViewConfiguration = None
    dayRanges: List[DayRanges3] = ()
    eventDateRanges: EventDateRanges = None
    options: List[NameValueStringPair] = ()
    programViewNodes: List[ProgramViewNode] = ()
    programViewNodesJson: str = ''
    serviceData: ServiceData = None


@dataclass
class NameValueStringPair(TcBaseObj):
    """
    Structure containing a pair(string,string) of name and value respectively.
    
    :var name: The name of key in Pair.
    :var stringValue: The value of key in Pair.
    """
    name: str = ''
    stringValue: str = ''


@dataclass
class ProgramViewConfiguration(TcBaseObj):
    """
    Contains the configuration data used for managing a ProgramView.
    
    :var scheduleUIDs: List of Schedule UIDs of the ProgramView.
    :var columns: List of ProgramView columns. The columns specify the ProgramView properties to be loaded.
    :var groups: List of ProgramView groups. The ProgramView nodes are grouped based on the properties specified in
    each group.
    :var filterSets: List of ProgramView filter set. Each FilterSet is an array of filters to be applied to the
    ProgarmView. The results of each FilterSet are combined together to build the final ProgramView structure.
    """
    scheduleUIDs: List[str] = ()
    columns: List[Column] = ()
    groups: List[ProgramViewGroup] = ()
    filterSets: List[FilterSet] = ()


@dataclass
class ProgramViewGroup(TcBaseObj):
    """
    Contains information about the Group modifier to be applied to the ProgramView.
    
    :var attributeName: The name of the grouping attribute in a ProgramView. This should be in the format of
    'Type.property'. For example, ScheduleTask.start_date.
    :var range: The range to be used for grouping the values.
    :var color: The color to be used for the group node.
    :var order: The order of the groups in a ProgramView. Valid values are: "none", "ascending", "descending"
    :var rollups: List of rollups for a group with rollup name as the key and value as the option. The rollup name
    should be in the format of 'Type.property'. For example, ScheduleTask.start_date. Valid values for rollup option
    are 'minimum', 'maximum', 'count', 'median', 'sum', 'average'.
    """
    attributeName: str = ''
    range: str = ''
    color: str = ''
    order: str = ''
    rollups: List[NameValueStringPair] = ()


@dataclass
class ProgramViewInfo(TcBaseObj):
    """
    Contains information about the operation to perform on the ProgramView and the configuration to use. The context
    node and reference node is provided in case of load operation
    
    :var programView: The ProgramView object in context. This will be NULL for &rsquo;create&rsquo; operation and a new
    ProgramView will be created.
    :var operationType: The operation to perform on the ProgramView. Valid values are:
    create : Creates a new ProgramView using the input programViewConfiguration.
    load : Loads the ProgramView
    loadUsingInputConfig : Loads the ProgramView using the input programViewConfiguration.
    save : Saves the ProgramView using the input programViewConfiguration.
    :var contextNodeId:  The unique identifier of the parent context node to load the child nodes. This input is
    applicable only for 'load' and &rsquo; loadUsingInputConfig&rsquo; operation types.
    :var referenceNodeId: The unique identifier of the reference node to be used for pagination. This input is
    applicable only for 'load' and &lsquo; loadUsingInputConfig&rsquo; operation types.
    :var inputOptions:  A list of options used for the ProgramView operation.
    Valid options and values are:
    returnProgramViewConfig : true/false ( Set true to return the current ProgramView configuration; false otherwise )
    returnResponseAsJSON : true/false ( Set true to return the ProgramView nodes in JSON format; false otherwise )
    :var programViewConfiguration: The ProgramView configuration containing Schedule UIDs, filters and group modifiers.
    This input is applicable only for ' loadUsingInputConfig&rsquo; and 'save' operation types.
    """
    programView: BusinessObject = None
    operationType: str = ''
    contextNodeId: str = ''
    referenceNodeId: str = ''
    inputOptions: List[NameValueStringPair] = ()
    programViewConfiguration: ProgramViewConfiguration = None


@dataclass
class ProgramViewNode(TcBaseObj):
    """
    Contains information about a ProgramView node.
    
    :var isTcObject: Set to true if the node represents a Teamcenter business object; false otherwise.
    :var nodeProperties: A list of Structure(string,string) of property names and its values for a ProgramView node.
    """
    isTcObject: bool = False
    nodeProperties: List[NameValueStringPair] = ()


@dataclass
class Column(TcBaseObj):
    """
    It specifies a column and it&rsquo;s sort order in a ProgramView.
    
    :var columnName: The name of the column in a ProgramView. This should be in the format of 'Type.property'. For
    example, ScheduleTask.start_date.
    :var order: The sorting order of the column. Valid values are: "none", "ascending", "descending".
    """
    columnName: str = ''
    order: str = ''


@dataclass
class DayRanges3(TcBaseObj):
    """
    Maps the weekdays to their ranges. The valid values for the days are 0 to 6 which represents Sunday through
    Saturday in the respective order. A range is a pair of start and end time of working hours. A day can have multiple
    ranges with breaks in-between in a working day.
    
    :var day: The event day.
    :var ranges: An array of ranges for the event day.
    """
    day: int = 0
    ranges: List[str] = ()


@dataclass
class Filter(TcBaseObj):
    """
    Contains information about a ProgramView filter.
    
    :var attributeName: The name of the filter. This should be in the format of 'Type.property'. For example,
    ScheduleTask.start_date.
    :var criteria: The filter criteria. Valid values are: 'equal','notEqual','greaterThan',
    'lessThan','greaterThanOrEqualTo','lessThanOrEqualTo', &lsquo;between'
    :var filterValue: The value of the ProgramView object property used for filtering.
    """
    attributeName: str = ''
    criteria: str = ''
    filterValue: str = ''


@dataclass
class FilterSet(TcBaseObj):
    """
    Contains a list of ProgramView filters. A FilterSet is an array of filters to be applied to the ProgramView.
    
    :var filters: List of ProgramView filters.
    """
    filters: List[Filter] = ()
