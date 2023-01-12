from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ScheduleMember, WorkspaceObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, BillRate, TCCalendarEvent, TaskDependency, SchedulingFixedCost
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FixedCostContainer(TcBaseObj):
    """
    The information need to create/update a Fixed Cost.
    
    :var name: The name of fixed cost.
    :var estimate: The estimated cost. Valid value can be empty string
    :var actual: The actual cost. Valid value can be empty string.
    :var currency: ISO-4217 code for currency of the costs.
    :var useActual: Should accrual calculations use the "actual" cost?
    :var billCode: The billing code. Valid values are determined by the LOV  {unassigned, General, Management,
    ProjectMgmt, Sales, Training, Travel, ProductDev, SoftwareDev}
    :var subCode: The billing subcode. Valid values are determined by the LOV. Values are following groups depending
    upon billcode.eg. If billcode is General then you can mentioned subcode as either of following set (unassigned,
    Accounting, Clerical, CorpAdmin, IT, Meetings, Other)                                             Following are the
    list of billcode and corresponsing valid values for sub code.  For BillCode 'unassigned' = { unassigned } For
    BillCode 'General' ={ unassigned, Accounting, Clerical, CorpAdmin, IT, Meetings, Other },
    For Bill code Management = { unassigned, Executive, ProjMgmt, Design/Plan, Meetings, Training, Other}
    For BillCode 'ProiectMgmt' ={ unassigned, Management, Meetings, Design/Plan, Training, Teaching, Clerical, Email,
    Other }
    For BillCode 'Sales' ={ unassigned, MajorAccts, General, Admin, Training, Other }
    For BillCode 'Training' ={ unassigned, Billable, Customer1, Customer2, Customer3, Region1, Region2, Region3, Other }
    For BillCode 'Travel' ={ unassigned, Billable, Region1, Region2, Region3, Other }
    For BillCode 'ProductDev' ={ unassigned, Planning, Design, Development, ProcessMgt, Validation, Other }
    For BillCode 'SoftwareDev' ={unassigned, Concept, Defination, Development, Introduction, Training, Other }
    :var billingType: The billing type. Valid value are
    { unassigned, Billable, Billed, Standard, Unbillable}
    :var accrualType: The cost accrual type (0=start, 1=prorated, 2=end).
    :var fixedCost: A reference to the cost being updated (or null when newCost).
    """
    name: str = ''
    estimate: str = ''
    actual: str = ''
    currency: str = ''
    useActual: bool = False
    billCode: str = ''
    subCode: str = ''
    billingType: str = ''
    accrualType: int = 0
    fixedCost: SchedulingFixedCost = None


@dataclass
class MembershipData(TcBaseObj):
    """
    The information needed to create a new member in a schedule.
    
    :var schedule: The schedule for the new membership. Valid value- tag of the schedule.
    :var resource: The resource to add.  (This can be a User, Group, or Discipline).valid value- tag of the resource
    :var membershipLevel: The membership level in that schedule. Valid values
    are-{0-observer,1-participant,2-coordinator}
    :var cost: The cost value (n.nnn (15.3 max))
    :var currency: The ISO-4217 currency code.
    """
    schedule: Schedule = None
    resource: BusinessObject = None
    membershipLevel: int = 0
    cost: str = ''
    currency: str = ''


@dataclass
class NewScheduleContainer(TcBaseObj):
    """
    The container for a new schedule.
    
    :var name: The name. Valid value can not be null
    :var description: The description. Valid value can be empty string
    :var taskFixedType: Task fixed type. Valid values - FIXED_WORK = 0, FIXED_DURATION = 1, FIXED_RESOURCES=2
    :var published: Indicates whether the schedule is published. Valid values - true or false
    :var notificationsEnabled: notificationsEnabled. Indicates whether notifications should be enabled. Valid values -
    true or false
    :var percentLinked: isPercentLinked? Indicates whether percentage complete should be linked to work complete. Valid
    values - true, false
    :var isTemplate: isTemplate? Indicates whether the schedule is a template. Valid values - true, false
    :var isPublic: Indicates whether the schedule is public. Valid values - true, false"
    :var type: type. This is the object_type of the schedule being created. It could be "Schedule" or any of the custom
    types created by the customer.
    :var billCode: The billCode. Valid value can be empty string
    :var billSubCode: The bill sub code. Valid value can be empty string
    :var billType: The bill type. Valid value can be empty string
    :var id: id. Valid value can not be null
    :var billRate: The bill rate. Valid value can be NULLTAG
    :var stringValueContainer: A collection of additional attributes (Optional)
    :var typedAttributesContainer: typedAttributesContainer. A container with type attribute -(optional)
    :var revID: revID. Valid value can not be null
    :var customerName: The customer's name. Valid value can be empty string
    :var customerNumber: The customer's ID. Valid value can be empty string
    :var startDate: The start Date. Valid value can not be null
    :var finishDate: The finishDate. Valid value can not be null
    :var priority: The priority. Valid values are {0-lowest,1-low,2-MediumLow,3-Medium,4-High,5-VeryHigh,6-Highest}
    :var status: The status. Valid values are  {0-Not started,1-In Progress,2-Needs
    Attention,3-Complete,4-Abandoned,5-Late}
    """
    name: str = ''
    description: str = ''
    taskFixedType: int = 0
    published: bool = False
    notificationsEnabled: bool = False
    percentLinked: bool = False
    isTemplate: bool = False
    isPublic: bool = False
    type: str = ''
    billCode: str = ''
    billSubCode: str = ''
    billType: str = ''
    id: str = ''
    billRate: BusinessObject = None
    stringValueContainer: List[StringValContainer] = ()
    typedAttributesContainer: List[TypedAttributeContainer] = ()
    revID: str = ''
    customerName: str = ''
    customerNumber: str = ''
    startDate: datetime = None
    finishDate: datetime = None
    priority: int = 0
    status: int = 0


@dataclass
class ScheduleCopyOptionsContainer(TcBaseObj):
    """
    The input information necessary to copy a schedule.
    
    :var name: The name of the new Schedule to be created.The name cannot be 'NULL' 
    
    :var description: The description text for the new Schedule to be created.
    :var typedAttributesContainer: This parameter specifies  any additional attribute values to be set on the newly
    created Schedule,scheduleRevision.
    :var copyinfo: This parameter specifies any additional metadata for the copy of the schedule. This 'DeepCopyData'
    data structure holds the relevant information regarding applicable deep copy rules.
    :var id: The id of the new Schedule to be created. The id value cannot be NULL.
    :var revId: The 'revID' of the new ScheduleRevision that will be created along with the new schedule.
    The 'revID' value cannot be NULL.
    
    :var scheduleToCopy: The tag to the schedule to copy.
    :var resetWork: This is the flag to indicate whether or not to reset the tasks' execution data (%, status, work
    complete, etc)
    :var copyBaselines: Flag to indicate whether or not to copy baselines.
    :var loadOnResponse: Flag to indicate whether or not to load the schedule in the response.
    :var iDeepCopyCount: This parameter stores the number of deep copied objects.
    :var stringValueContainer: This parameter is  to collect additional attributes for the new schedule. The container
    represents a single attribute's value.
    """
    name: str = ''
    description: str = ''
    typedAttributesContainer: List[TypedAttributeContainer] = ()
    copyinfo: List[ScheduleDeepCopyinfo] = ()
    id: str = ''
    revId: str = ''
    scheduleToCopy: Schedule = None
    resetWork: bool = False
    copyBaselines: bool = False
    loadOnResponse: bool = False
    iDeepCopyCount: int = 0
    stringValueContainer: List[StringValContainer] = ()


@dataclass
class ScheduleCopyResponse(TcBaseObj):
    """
    The response from a schedule copy call.  It includes all the data necessary to load that schedule.
    
    :var schedule: The schedule.
    :var scheduleTask: The schedule tasks.
    :var resourceAssignment: The task assignments.
    :var taskDependency: The task dependencies.
    :var calendar: The calendars asssociated with the schedule and its members.
    :var calendarEvent: The calendar events associated with the calendars.
    """
    schedule: Schedule = None
    scheduleTask: List[ScheduleTask] = ()
    resourceAssignment: List[ResourceAssignment] = ()
    taskDependency: List[TaskDependency] = ()
    calendar: List[TCCalendar] = ()
    calendarEvent: List[TCCalendarEvent] = ()


@dataclass
class ScheduleCopyResponses(TcBaseObj):
    """
    Container to hold multiple ScheduleCopyResponse objects.
    
    :var scheduleResponse: A collection of ScheduleCopyResponses.
    :var serviceData: The ServiceData.
    """
    scheduleResponse: List[ScheduleCopyResponse] = ()
    serviceData: ServiceData = None


@dataclass
class ScheduleDeepCopyinfo(TcBaseObj):
    """
    The DeepCopyData data structure holds the relevant information regarding applicable deep copy rules.
    
    :var objectComp: A tag representing object on which the
    deep copy action need to be performed.
    :var relation: A string representing the name the relation  that need to be deep copied. Valid value can be
    IMANRelation.
    :var objName: A string representing the new name for the new copy.
    of the object represented by otherSideObjectTag. The value for
    the newName will be null if the 'action' is not CopyAsObject or
    ReviseAndRelateToLatest.
    :var operationType: An integer representing the action to be performed on the object represented by
    'otherSideObjectTag'.
    The values for action are:
    CopyAsObjectType = 0,
    CopyAsRefType = 1,
    DontCopyType =2,
    RelateToLatest = 3,
    ReviseAndRelateToLatest = 4
    :var isTargetPrimary: A Boolean representing whether the given item
    revision is a primary object in the relation that need
    to be deep copied.
    :var isRequired: A Boolean representing whether the deep information is from a mandatory deep copy rule configured
    by the administrator or not.
    """
    objectComp: BusinessObject = None
    relation: str = ''
    objName: str = ''
    operationType: int = 0
    isTargetPrimary: bool = False
    isRequired: bool = False


@dataclass
class ScheduleDeliverableData(TcBaseObj):
    """
    A container for a new Schedule Deliverable.
    
    :var schedule: The schedule to contain this deliverable.
    :var deliverableType: The type of the deliverable.
    :var deliverableName: The name of the deliverable.
    :var deliverableReference: A reference to the deliverable.(optional)
    """
    schedule: Schedule = None
    deliverableType: str = ''
    deliverableName: str = ''
    deliverableReference: WorkspaceObject = None


@dataclass
class BillRateContainer(TcBaseObj):
    """
    The container for a BillRate.
    
    :var type: The type: (0-Multiplier, 1-Custom Rate).
    :var name: The name of the bill rate.
    :var rate: The new hourly rate or multiplier in the format *n.nnn (15.3  max).
    :var currency: The ISO 4217 currency rate.
    """
    type: int = 0
    name: str = ''
    rate: str = ''
    currency: str = ''


@dataclass
class StringValContainer(TcBaseObj):
    """
    The container represents a single attribute's value. 
    The name of the attribute is represented by the key field. 
    The data type of the attribute is represented by the type field. The type field can be one of the following;
    char = 0;
    date = 1;
    double = 2;
    float = 3;
    int = 4;
    bool = 5;
    short = 6;
    string = 7;
    ModelObject = 8;
    
    :var key: A string key identifying the attribute.
    :var value: A string representation of the value of the attribute.
    :var type: An integer to help determine the data type of the attribute. Valid values- {
    1=String_type,2=Integer_type,3=Long_type,4=Double_type,5=Float_type,6=Boolean_type,7=Date_type,8=Cal_type }
    """
    key: str = ''
    value: str = ''
    type: int = 0


@dataclass
class TaskCostUpdate(TcBaseObj):
    """
    The request container for fixed cost and costing meta data updates.
    
    :var task: The task which contains or will contain the fixed costs.
    :var newCosts: The information needed to create new fixed costs.
    :var updatedCosts: The information needed to update existing fixed costs.
    :var deletedCosts: A list of fixed costs to delete.
    :var billCode: The bill code for the task. Valid values are determined by the LOV. Valid values are {unassigned,
    General, Management, ProjectMgmt, Sales, Training, Travel, ProductDev, SoftwareDev}
    :var subCode: The bill subcode for the task. Valid values are determined by the LOV. Valid value are following
    groups depending upon billcode.eg. If billcode is General then you can mentioned subcode as either of following set
    (unassigned, Accounting, Clerical, CorpAdmin, IT, Meetings, Other)                    Following are the list of
    billcode and corresponsing valid values for sub code.
    For BillCode 'unassigned' = { unassigned }
    For BillCode 'General' ={ unassigned, Accounting, Clerical, CorpAdmin, IT, Meetings, Other },
    For Bill code Management = { unassigned, Executive, ProjMgmt, Design/Plan, Meetings, Training, Other}
    For BillCode 'ProiectMgmt' ={ unassigned, Management, Meetings, Design/Plan, Training, Teaching, Clerical, Email,
    Other }
    For BillCode 'Sales' ={ unassigned, MajorAccts, General, Admin, Training, Other }
    For BillCode 'Training' ={ unassigned, Billable, Customer1, Customer2, Customer3, Region1, Region2, Region3, Other }
    For BillCode 'Travel' ={ unassigned, Billable, Region1, Region2, Region3, Other }                                  
        For BillCode 'ProductDev' ={ unassigned, Planning, Design, Development, ProcessMgt, Validation,Other}          
                                               For BillCode 'SoftwareDev' ={unassigned, Concept, Defination,
    Development, Introduction, Training, Other }
    :var billingType: The billing type of the task. Valid values are determined by the LOV. Valid value are {
    unassigned, Billable, Billed, Standard, Unbillable}
    :var billRate: The name of the bill rate associated with the task.
    Valid value can be empty string
    :var rate: A tag to the bill rate to associate with this task.
    Valid value can be NULLTAG
    """
    task: ScheduleTask = None
    newCosts: List[FixedCostContainer] = ()
    updatedCosts: List[FixedCostContainer] = ()
    deletedCosts: List[SchedulingFixedCost] = ()
    billCode: str = ''
    subCode: str = ''
    billingType: str = ''
    billRate: str = ''
    rate: BillRate = None


@dataclass
class TaskCostUpdateResponse(TcBaseObj):
    """
    The response container for fixed cost update.
    
    :var updatedTask: The updated task.
    :var newCosts: The list of new fixed costs.
    """
    updatedTask: ScheduleTask = None
    newCosts: List[SchedulingFixedCost] = ()


@dataclass
class TypedAttributeContainer(TcBaseObj):
    """
    A container which is used to update custom properties.
    
    :var type: The object type. Valid values are { 
    ScheduleType,ScheduleRevisionType,ScheduleTaskType,ScheduleTaskRevisionType}
    :var attributes: A collection of updates.(optional)
    """
    type: str = ''
    attributes: List[StringValContainer] = ()


@dataclass
class UpdateTaskCostDataResponse(TcBaseObj):
    """
    The response to the cost update.
    
    :var responses: The collection of individual task cost changes.
    :var serviceData: The ServiceData.
    """
    responses: List[TaskCostUpdateResponse] = ()
    serviceData: ServiceData = None


@dataclass
class CreateBillRateResponse(TcBaseObj):
    """
    The response when BillRates are created.
    
    :var serviceData: The ServiceData.
    :var rates: The added BillRates.
    """
    serviceData: ServiceData = None
    rates: List[BillRate] = ()


@dataclass
class AddMembershipResponse(TcBaseObj):
    """
    The response when schedule members are added.
    
    :var data: The ServiceData.
    :var addedMembers: The added members.
    """
    data: ServiceData = None
    addedMembers: List[ScheduleMember] = ()


@dataclass
class CreateScheduleResponse(TcBaseObj):
    """
    The response when new Schedule is created
    
    :var serviceData: The ServiceData
    :var schedules: The created Schedules
    """
    serviceData: ServiceData = None
    schedules: List[Schedule] = ()
