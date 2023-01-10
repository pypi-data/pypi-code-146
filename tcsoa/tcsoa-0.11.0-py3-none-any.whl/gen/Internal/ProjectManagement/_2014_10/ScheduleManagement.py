from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, ScheduleTask, Schedule, ResourceAssignment, TaskDependency
from tcsoa.gen.Internal.ProjectManagement._2008_06.ScheduleManagement import GenericAttributesContainer
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PasteTaskContainer(TcBaseObj):
    """
    This Container will hold information required for cut paste or copy paste of Task object.
     Teamcenter::WorkspaceObject sourceTask --> source task
     Teamcenter::WorkspaceObject prevSibling --> destination task under which copied or cut task will be pasted.
     Teamcenter::WorkspaceObject newParent --> parent task
     int flag ---> 0= copy operation 1= cut operation
    
    
    
    :var sourceTask: The  task to copy or cut.
    :var prevSibling: The task above the requested location.
    :var newParent: The new parent of the Task.
    :var flag: flag =0 copy operation
    flag =1 cut operation
    """
    sourceTask: WorkspaceObject = None
    prevSibling: WorkspaceObject = None
    newParent: WorkspaceObject = None
    flag: int = 0


@dataclass
class DeferredSaveOption(TcBaseObj):
    """
    This will have information about schedule and deferred options as below
    -1 = Start deferred session and continue.
    0 = Save deferred session and continue.
    1= Save deferred session and exit.
    2= Cancel deferred session and exit.
    
    :var schedule: schedule tag which is in deferred mode.
    :var deferredOption: -1 = start deferred session and continue.
    0 = Save deferred session and continue.
    1= Save deferred session and exit.
    2= Cancel deferred session and exit.
    """
    schedule: Schedule = None
    deferredOption: int = 0


@dataclass
class DeferredSaveResponse(TcBaseObj):
    """
    Deferred save response  will have the information of updated a schedule.  It contains new, updated, and deleted
    tasks, resource assignments, and task dependencies information for a schedule.
    
    :var schedule: Schedule tag which is in deferred mode.
    :var scheduleUpdates: the schedule updates- GenericAttributesContainer{ object-schedule object
    tag,keyValContainer(can be empty),StringValContainer(can be empty),typedAttributeContainer(can be empty) }
    :var deletedAssignments: The deleted assignments
    :var newProxyTasks: The information of new ProxyTask created in this schedule
    :var proxyTaskUpdates: A list of known updated proxy tasks.
    :var deletedProxyTasks: A list of proxy tasks to be deleted.
    :var serviceData: The service data.
    :var newTasks: The new tasks to add
    :var newDependencies: The new dependencies
    :var newAssignments: The new assignments
    :var taskUpdates: The existing tasks update
    :var dependencyUpdates: The existing dependencies updates
    :var assignmentUpdates: The existing assignments update
    :var deletedTasks: The deleted tasks
    :var deletedDependencies: The deleted dependencies
    """
    schedule: Schedule = None
    scheduleUpdates: GenericAttributesContainer = None
    deletedAssignments: List[ResourceAssignment] = ()
    newProxyTasks: List[GenericAttributesContainer] = ()
    proxyTaskUpdates: List[GenericAttributesContainer] = ()
    deletedProxyTasks: List[BusinessObject] = ()
    serviceData: ServiceData = None
    newTasks: List[GenericAttributesContainer] = ()
    newDependencies: List[GenericAttributesContainer] = ()
    newAssignments: List[GenericAttributesContainer] = ()
    taskUpdates: List[GenericAttributesContainer] = ()
    dependencyUpdates: List[GenericAttributesContainer] = ()
    assignmentUpdates: List[GenericAttributesContainer] = ()
    deletedTasks: List[ScheduleTask] = ()
    deletedDependencies: List[TaskDependency] = ()
