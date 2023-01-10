from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ScheduleTask, Schedule, BillRate
from tcsoa.gen.ProjectManagement._2008_06.ScheduleManagement import FixedCostContainer
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FailedObjectContainer(TcBaseObj):
    """
    FailedObjectContainer will hold the Schedule Task and an error message of the operation that failed.
    
    :var tasks: A vector of Schedule Tasks
    :var errorMsgs: A vector of strings that have the error messages.
    :var serviceData: The service data
    """
    tasks: List[ScheduleTask] = ()
    errorMsgs: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class AnalyticsMultipleResourceAssignmentStacks(TcBaseObj):
    """
    Reponse container for resource graph data request that contains one or more resources.
    
    :var stacksVector: Multiple resource stacks container.
    """
    stacksVector: List[AnalyticsResourceAssignmentStacks] = ()


@dataclass
class AnalyticsResourceAssignmentDayStack(TcBaseObj):
    """
    Holds data for all the assigned tasks for the day. 
    
    :var numElements: Number of elements that makeup the stack for the day.
    :var stack: Stack/pile of assigned tasks for the day.
    """
    numElements: int = 0
    stack: List[AnalyticsResourceAssignmentSingleTask] = ()


@dataclass
class AnalyticsResourceAssignmentSingleTask(TcBaseObj):
    """
    Information on single task assignment for the day.
    
    :var day: Date of assignments.
    :var userUid: Uid of the business object
    :var taskEndDate: ScheduleTask end date.
    :var taskMinutes: Amount of work on the task.
    :var resourceMinutes: Day's work performed on the task.
    :var stackBase: Where to place the next element in the day's stack of work.
    :var taskMinutesOverLoad: Amount of day's work over and above what the user's calendar indicates.
    :var userData: Descriiption of the data to provide tooltip information.
    :var calUid: Uid of user calendar
    :var schUid: Uid of Schedule to which task assignment belongs.  
    :var schTaskUid: The scheduleTask from which the assignment is assigned. 
    :var schName: Name of the schedule
    :var schStartDate: Schedule start date
    :var schEndDate: Schedule end/finish date. 
    :var taskName: Name of the scheduleTask from which the assignment was made.
    :var taskstartDate: ScheduleTask start date.
    """
    day: datetime = None
    userUid: str = ''
    taskEndDate: datetime = None
    taskMinutes: float = 0.0
    resourceMinutes: float = 0.0
    stackBase: float = 0.0
    taskMinutesOverLoad: float = 0.0
    userData: str = ''
    calUid: str = ''
    schUid: str = ''
    schTaskUid: str = ''
    schName: str = ''
    schStartDate: datetime = None
    schEndDate: datetime = None
    taskName: str = ''
    taskstartDate: datetime = None


@dataclass
class AnalyticsResourceAssignmentStacks(TcBaseObj):
    """
    Holds stack of tasks for each day and for all days between the start and finish dates.
    
    :var userName: Name of the reesource
    :var numDays: Numebr of days between the start and finish range.The range represent when the graph starts and ends.
    :var stacks: Holds data for all the days that falls between start and finish dates. 
    """
    userName: str = ''
    numDays: int = 0
    stacks: List[AnalyticsResourceAssignmentDayStack] = ()


@dataclass
class InsertScheduleContainer(TcBaseObj):
    """
    Contains the information of the schedule being inserted, the master schedule, the task in the master schedule below
    which the sub-schedule is inserted and the Boolean to adjust the master dates
    
    :var subSchedule: The schedule that is being inserted in the master schedule.
    :var masterSchedule: The schedule in which the subSchedule is being inserted.
    :var masterScheduleTask: The task in the master schedule below which the subSchedule is being inserted.
    :var adjustMasterDates: Boolean value of true will allow the master start and/or end date to automatically adjust
    if the sub schedule start and/or finish date do not lie between the master dates.
    """
    subSchedule: Schedule = None
    masterSchedule: Schedule = None
    masterScheduleTask: ScheduleTask = None
    adjustMasterDates: bool = False


@dataclass
class LoadResourceGraphContainer(TcBaseObj):
    """
    A container representing the Query input for the resource load.
    
    :var resources: The user Tags.
    :var startDate: An optional Start Date to filter with requires endDate.
    :var endDate: An optional Finish Date to filter with requires startDate.
    """
    resources: List[BusinessObject] = ()
    startDate: datetime = None
    endDate: datetime = None


@dataclass
class CostDetailContainer(TcBaseObj):
    """
    The container that has the details of the cost attributes of schedule or task 
    
    :var totalEstimatedMinutes: The total estimated minutes of schedule or collection of selected schedule tasks or
    individual task
    :var totalAccruedMinutes: The total accrued minutes of schedule or collection of selected schedule tasks or
    individual task .
    :var numchildren: the number of children associated with the summary tasks or schedule
    :var fixedCostData: Fixed cost container
    :var taskCostDetails: the cost details of each sub-task
    :var totalEstimatedCost: The total estimated cost of schedule task
    :var totalAccruedCost: The total estimated cost of schedule task
    :var billCode: The bill code for task. Valid values are determined by the LOV. Valid values are {unassigned,
    General, Management, ProjectMgmt, Sales, Training, Travel, ProductDev, SoftwareDev}. 
    :var billSubCode: The bill subcode for the task. Valid values are determined by the LOV. Valid value are following
    groups depending upon billcode.eg. If billcode is General then you can mentioned subcode as either of following set
    (unassigned, Billable, Billed, Standard, Unbillable}
    :var billingType: The billing type of the task. Valid values are determined by the LOV. Valid value are {
    unassigned, Billable, Billed, Standard, Unbillable}.
    :var billRate: The name of the bill rate associated with the task. Valid value can be empty string
     
    
    :var currency: The currency used in the cost for schedule or task.
    :var task: The task which contains the total costs (sum of fixed costs and variable costs) 
    """
    totalEstimatedMinutes: int = 0
    totalAccruedMinutes: int = 0
    numchildren: int = 0
    fixedCostData: List[FixedCostContainer] = ()
    taskCostDetails: List[CostDetailContainer] = ()
    totalEstimatedCost: float = 0.0
    totalAccruedCost: float = 0.0
    billCode: str = ''
    billSubCode: str = ''
    billingType: str = ''
    billRate: BillRate = None
    currency: str = ''
    task: ScheduleTask = None


@dataclass
class CostDetailResponse(TcBaseObj):
    """
    The response of the get cost roll up data
    
    :var costDetails: The response of the get cost roll up data
    :var costServiceData: Service data
    """
    costDetails: List[CostDetailContainer] = ()
    costServiceData: ServiceData = None


@dataclass
class DetachScheduleContainer(TcBaseObj):
    """
    DetachScheduleContainer    Contains the information of the schedule being detached, the master schedule.
    
    :var subSchedule: The schedule that is being detached from the master schedule.
    :var masterSchedule: The master schedule from which the subSchedule is being detached.
    """
    subSchedule: Schedule = None
    masterSchedule: Schedule = None


@dataclass
class EVMDataRequest(TcBaseObj):
    """
    Earned Value Data Request of schedule or task 
    
    :var taskVector: The tag of a task
    :var calcBasisSelected: To view the earned value data of schedule or task by cost , use the boolean value as false
    . To view the earned value data of schedule or task by duration , use the boolean value as true and the default
    option .
    :var calcWorkComplete: To view the earned value data based on work complete of schedule's or tasks's percentage
    complete used, use the boolean value as true and the default option .To view the earned value data based on the
    work complete of schedule's task's actual hours used , use the boolean value as false . 
    :var selectedLabel: To view the earned value data based on the schedule's or task's earned value management labels
    , use the boolean value as true and the default option . To view the earned value data based on the schedule's or
    task's Cost/Schedule control systems criteria labels , use the boolean value as false.
    """
    taskVector: List[ScheduleTask] = ()
    calcBasisSelected: bool = False
    calcWorkComplete: bool = False
    selectedLabel: bool = False


@dataclass
class EVMResultsContainer(TcBaseObj):
    """
    The container that contains the task&apos;s or schedule&apos;s earned value data.
    
    :var task: The tag of a task 
    :var evmResults: The evm results that holds the earned value calculations of schedule or task
    """
    task: ScheduleTask = None
    evmResults: EVMResults = None


@dataclass
class EVMResultsResponse(TcBaseObj):
    """
    The response that contains the evm results 
    
    :var evmData: The container that holds the earned value data of the schedule or task
    :var evmServiceData: The service data 
    """
    evmData: EVMResultsContainer = None
    evmServiceData: ServiceData = None


"""
The earned value map holds the data of each earned value paramater used in earmed valued calculation of schedule or task .Planned value(PV) is the total budgeted costs for the project that is scheduled to be doneuntil now
"""
EVMResults = Dict[str, float]
