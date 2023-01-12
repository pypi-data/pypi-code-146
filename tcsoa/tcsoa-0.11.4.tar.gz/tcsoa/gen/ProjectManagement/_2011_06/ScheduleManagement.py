from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0ProxyTask, WorkspaceObject, TCCalendar, ScheduleTask, Schedule, ResourceAssignment, TaskDependency, TCCalendarEvent
from typing import List
from tcsoa.gen.ProjectManagement._2008_06.ScheduleManagement import ScheduleDeepCopyinfo, StringValContainer, TypedAttributeContainer
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LoadScheduleContainer(TcBaseObj):
    """
    Contain the schedule uids and options for loading schedules
    
    :var scheduleUids: The UIDs of the schedules.
    :var schmgtOptions: The options for loading. Integer Option:
    "SM_Structure_Partial_Context"
    Values:
    0 =  load the full schedule including all sub schedules and their children .
    1 =   load only schedule summaries partially   
    
    Integer Option: 
    "SM_Structure_Load_Context"
    Values: 
    0 = loading schedule 
    1 = loading sub-schedule  
    4 = inserting sub schedule by reference
    Integer Option:
    "SM_Structure_Client_Context"
    Values:
    0 = RAC client
    1 = Server client (for Synchronous dispatcher)
    2 = MSP plugin client
    """
    scheduleUids: List[str] = ()
    schmgtOptions: SchMgtOptions = None


@dataclass
class LockRequest(TcBaseObj):
    """
    A request structure to lock the schedule.
    
    :var schedule: The schedule for which the lock request is
    :var requestLock: The request to lock (true) or unlock (false)
    """
    schedule: Schedule = None
    requestLock: bool = False


@dataclass
class LockResponse(TcBaseObj):
    """
    A Response for SOA "ManageScheduleLocks". This will indicate whether the lock request is successful or not.
    
    :var schedule: The schedule locked or unlocked
    :var lockState: The state of the lock (true=locked, false=not locked)
    :var requestSuccess: Was the request successful. True if the request was a success.
    """
    schedule: Schedule = None
    lockState: bool = False
    requestSuccess: bool = False


@dataclass
class LockResponses(TcBaseObj):
    """
    List of multiple "LockResponses".
    
    :var data: The service data
    :var responses: The individual responses
    """
    data: ServiceData = None
    responses: List[LockResponse] = ()


@dataclass
class MasterMetaData(TcBaseObj):
    """
    A container for the SubMasterMetaData.
    
    :var uid: The uid of a master schedule.
    :var start: The Start Date of that master schedule.
    :var finish: The Finish Date of that master schedule.
    """
    uid: str = ''
    start: datetime = None
    finish: datetime = None


@dataclass
class MultipleScheduleLoadResponses(TcBaseObj):
    """
    A container for load schedule responses
    
    :var scheduleData: Collection of the schedule load responses.
    :var serviceData: The ServiceData.
    """
    scheduleData: List[ScheduleLoadResponse] = ()
    serviceData: ServiceData = None


@dataclass
class ProxyTaskContainer(TcBaseObj):
    """
    Container for Proxy Task
    
    :var schedule: The schedule were the proxy is being created
    :var sublevels: Number of sublevels (if this should be mirrored in the sub schedules (-1 =  all, 0 = only this
    schedule, 1= first level, 2 = 1st and 2nd level, etc)
    :var taskTag: The real task being proxied.
    :var refTag: The reference task in the schedule
    """
    schedule: Schedule = None
    sublevels: int = 0
    taskTag: ScheduleTask = None
    refTag: WorkspaceObject = None


@dataclass
class ProxyTaskResponse(TcBaseObj):
    """
    Response for createProxyTasks call.
    
    :var schedule: The schedule of the proxy task.
    :var proxyTask: The proxy task
    :var subScheduleAdditions: A collection containing a ProxyTaskResponse for each sub schedules addition
    """
    schedule: Schedule = None
    proxyTask: Fnd0ProxyTask = None
    subScheduleAdditions: List[ProxyTaskResponse] = ()


@dataclass
class ProxyTaskResponses(TcBaseObj):
    """
    A collection of ProxyTaskResponses returned for createProxyTasks call.
    
    :var data: The service data
    :var responses: A collection of ProxyTaskResponse
    """
    data: ServiceData = None
    responses: List[ProxyTaskResponse] = ()


@dataclass
class RefreshScheduleContainer(TcBaseObj):
    """
    Container for refreshing schedule
    
    :var masterScheduleUid: The UID of the master schedule.
    :var componentUid: The UID of the object to refresh
    :var refreshOptions: The options for refresh. Integer Option:
    "SM_Structure_Partial_Context"
    Values:
    0 =  load the full schedule including all sub schedules and their children .
    1 =   load only schedule summaries partially   
    
    Integer Option: 
    "SM_Structure_Load_Context"
    Values: 
    6 = refresh the schedule
    7 = load all objects currently not in the client; compliment
    
    Integer Option:
    "SM_Structure_Client_Context"
    Values:
    0 = RAC client
    1 = Server client (for Synchronous dispatcher)
    2 = MSP plugin client
    :var clientCache: List of currently loaded components for the object being refreshed.
    :var lastModifiedDate: The last modified date for the component represented by componentUID.
    """
    masterScheduleUid: str = ''
    componentUid: str = ''
    refreshOptions: SchMgtOptions = None
    clientCache: SchmgtClientCache = None
    lastModifiedDate: datetime = None


@dataclass
class SchMgtIntegerOption(TcBaseObj):
    """
    Schedule Manager Integer Option
    
    :var name: The name of the option
    :var value: The value of the option
    """
    name: str = ''
    value: int = 0


@dataclass
class SchMgtIntegerOptionAsync(TcBaseObj):
    """
    SchMgtIntegerOptions for Async operation
    
    :var name: The name of the option
    :var value: The value of the option
    """
    name: str = ''
    value: int = 0


@dataclass
class SchMgtLogicalOption(TcBaseObj):
    """
    Schedule Manager Logical Option
    
    :var name: The name of the option
    :var value: The value of the option (True or False)
    """
    name: str = ''
    value: bool = False


@dataclass
class SchMgtLogicalOptionAsync(TcBaseObj):
    """
    SchMgtLogicalOptions for Async operation
    
    :var name: The name of the option
    :var value: The value of the option (True or False)
    """
    name: str = ''
    value: bool = False


@dataclass
class SchMgtOptions(TcBaseObj):
    """
    Schedule Management Options
    
    :var logicalOptions: Logical options
    :var integerOptions: Integer Options
    :var stringOptions: String Options
    """
    logicalOptions: List[SchMgtLogicalOption] = ()
    integerOptions: List[SchMgtIntegerOption] = ()
    stringOptions: List[SchMgtStringOption] = ()


@dataclass
class SchMgtOptionsAsync(TcBaseObj):
    """
    SchMgtOptions for Async operation
    
    :var logicalOptions: Logical options
    :var integerOptions: Integer Options
    :var stringOptions: String Options
    """
    logicalOptions: List[SchMgtLogicalOptionAsync] = ()
    integerOptions: List[SchMgtIntegerOptionAsync] = ()
    stringOptions: List[SchMgtStringOptionAsync] = ()


@dataclass
class SchMgtStringOption(TcBaseObj):
    """
    Schedule Manager String Option
    
    :var name: The name of the option
    :var value: The value of the option.
    """
    name: str = ''
    value: str = ''


@dataclass
class SchMgtStringOptionAsync(TcBaseObj):
    """
    SchMgtStringOptions for Async operation
    
    :var name: The name of the option
    :var value: The value of the option.
    """
    name: str = ''
    value: str = ''


@dataclass
class ScheduleCopyOptionsContainer(TcBaseObj):
    """
    Container for schedule copy options
    
    :var name: The name of the new schedule
    :var description: The description of the new schedule. Valid value -can be empty string.
    :var id: The ID of the new schedule.
    :var revId: The revId of the new schedule.
    :var scheduleToCopy: The tag to the schedule to copy.
    :var options: Copy schedule options 1) logical options  -{bool copyBaselines,bool loadOnResponse,bool
    resetWork,bool copyProxyTasks,bool  copycrossScheduleDependencies } 2) integerOptions -{ int ideepCopyCount } 3)
    stringOptions -{bool deepcopyrequired }
    :var stringValueContainer: Additional attributes for the new schedule.(optional)
    :var typedAttributesContainer: Additional  attributes for the new schedule.(optional)
    :var copyInfo: Additional metadata for the copy.(optional)
    """
    name: str = ''
    description: str = ''
    id: str = ''
    revId: str = ''
    scheduleToCopy: Schedule = None
    options: SchMgtOptions = None
    stringValueContainer: List[StringValContainer] = ()
    typedAttributesContainer: List[TypedAttributeContainer] = ()
    copyInfo: List[ScheduleDeepCopyinfo] = ()


@dataclass
class ScheduleCopyOptionsContainerAsync(TcBaseObj):
    """
    ScheduleCopyOptionsContainer for copySchedule
    
    :var name: The name of the new schedule
    :var description: The description of the new schedule. Valid value -can be empty string.
    :var id: The ID of the new schedule.
    :var revId: The revId of the new schedule.
    :var scheduleToCopy: The tag to the schedule to copy.
    :var options: Copy schedule options 1) logical options  -{bool copyBaselines,bool loadOnResponse,bool
    resetWork,bool copyProxyTasks,bool  copycrossScheduleDependencies } 2) integerOptions -{ int ideepCopyCount } 3)
    stringOptions -{bool deepcopyrequired }
    :var stringValueContainer: Additional  attributes for the new schedule.(optional)
    :var typedAttributesContainer: Additional  attributes for the new schedule.(optional)
    :var copyInfo: This parameter specifies any additional metadata for the copy of the schedule. This
    'ScheduleDeepCopyinfoAsync' data structure holds the relevant information regarding applicable deep copy rules.
    This is optional parameter.
    """
    name: str = ''
    description: str = ''
    id: str = ''
    revId: str = ''
    scheduleToCopy: Schedule = None
    options: SchMgtOptionsAsync = None
    stringValueContainer: List[StringValContainerAsync] = ()
    typedAttributesContainer: List[TypedAttributeContainerAsync] = ()
    copyInfo: List[ScheduleDeepCopyinfoAsync] = ()


@dataclass
class ScheduleDeepCopyinfoAsync(TcBaseObj):
    """
    ScheduleDeepCopyinfoAsync container
    
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
class ScheduleLoadResponse(TcBaseObj):
    """
    Container for the load schedules response.
    
    :var schedule: The schedule
    :var scheduleTasks: All the tasks in this schedule.
    :var resourceAssignments: All the resource assignments in this schedule.
    :var taskDependencies: All the task dependencies in this schedule.
    :var calendars: All the calendars referenced in this schedule.
    :var calendarEvents: All the calendar events referenced in the calendars.
    :var submasterdata: The metadata for master-schedules of this schedule and all sub-schedules.
    :var namedStringLists: Currently used by refresh to return deleted objects to the client.
    """
    schedule: Schedule = None
    scheduleTasks: List[ScheduleTask] = ()
    resourceAssignments: List[ResourceAssignment] = ()
    taskDependencies: List[TaskDependency] = ()
    calendars: List[TCCalendar] = ()
    calendarEvents: List[TCCalendarEvent] = ()
    submasterdata: List[SubMasterMetaData] = ()
    namedStringLists: List[SchmgtNamedStringList] = ()


@dataclass
class SchmgtClientCache(TcBaseObj):
    """
    The list of names lists.
    
    :var namedStringLists: Array of named string lists of components uid
    """
    namedStringLists: List[SchmgtNamedStringList] = ()


@dataclass
class SchmgtNamedStringList(TcBaseObj):
    """
    A vector of lists.
    
    :var name: A unique identifier for this list (possibly UID).
    :var list: The list of  UIDs contained by this object.
    :var aggregate: Not Used
    """
    name: str = ''
    list: List[str] = ()
    aggregate: float = 0.0


@dataclass
class StringValContainerAsync(TcBaseObj):
    """
    string value container for Async operation
    
    :var key: A string key identifying the attribute.
    :var value: A string representation of the value of the attribute.
    :var type: An integer to help determine the data type of the attribute. Valid values- {
    1=String_type,2=Integer_type,3=Long_type,4=Double_type,5=Float_type,6=Boolean_type,7=Date_type,8=Cal_type }
    """
    key: str = ''
    value: str = ''
    type: int = 0


@dataclass
class SubMasterMetaData(TcBaseObj):
    """
    A container for the sub-schedule master MetaData.
    
    :var subschedule: The tag of the sub schedule.
    :var masterdata: Collection of metadata for all master schedules of this schedule and it's sub-schedules.
    """
    subschedule: Schedule = None
    masterdata: List[MasterMetaData] = ()


@dataclass
class TaskExecUpdate(TcBaseObj):
    """
    The structure which would be used to send back and forth the data for execution view for tasks.
    
    :var task: The task being updated.
    :var updateAS: Must be true when updating the Actual Start Date.
    :var newAS: The new Actual Start Date to set (null is allowed). updateAS must also be to true to update this value.
    :var updateAF: Must be true when updating the Actual Finish Date.
    :var newAF: The new Actual Finish Date to set (null is allowed). updateAF must also be to true to update this value.
    :var newPC: The new percent complete for the task (0-100) (-1 for no  update)
    :var newStatus: The new status for the task. Valid values are the status strings listed in the status LOV. ("" or
    null for no update)
    :var newWC: The new work complete to set (-1 means no update)
    :var newWR: The new work remaining to set (-1 means no update)
    """
    task: ScheduleTask = None
    updateAS: bool = False
    newAS: datetime = None
    updateAF: bool = False
    newAF: datetime = None
    newPC: float = 0.0
    newStatus: str = ''
    newWC: int = 0
    newWR: int = 0


@dataclass
class TypedAttributeContainerAsync(TcBaseObj):
    """
    TypedAttributeContainerAsync conatiner for Async operation
    
    :var type: The object type
    :var attributes: A collection of updates
    """
    type: str = ''
    attributes: List[StringValContainerAsync] = ()
