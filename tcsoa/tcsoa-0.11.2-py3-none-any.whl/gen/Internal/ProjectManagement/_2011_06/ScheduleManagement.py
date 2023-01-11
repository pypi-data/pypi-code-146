from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0ProxyTask, ScheduleTask, ResourceAssignment, TaskDependency
from tcsoa.gen.Internal.ProjectManagement._2008_06.ScheduleManagement import GenericAttributesContainer
from typing import List
from tcsoa.gen.ProjectManagement._2011_06.ScheduleManagement import SchMgtOptions
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LoadProgramViewContainer(TcBaseObj):
    """
    An input container containing the list of schedules and filter conditions.
    
    :var schedules: The UIDs of the Schedules which are included in this program view.
    :var loadProgramViewSets: The collection of filters to be applied.
    """
    schedules: List[str] = ()
    loadProgramViewSets: List[LoadProgramViewSet] = ()


@dataclass
class LoadProgramViewFilter(TcBaseObj):
    """
    The represents the a single input filter in the query for loading the program view.
    
    :var field: The integer value of property to filter out tasks or schedules.
    :var value: The value of the property to filter out schedules or tasks.
    :var condition: The condition: greater-than, less-than etc.
    """
    field: str = ''
    value: str = ''
    condition: int = 0


@dataclass
class LoadProgramViewSet(TcBaseObj):
    """
    The collection of input filters.
    
    :var loadProgramViewFilters: The filters.
    """
    loadProgramViewFilters: List[LoadProgramViewFilter] = ()


@dataclass
class ScheduleModifyContainer(TcBaseObj):
    """
    The information to update a schedule.  It contains new, updated, and deleted tasks, resource assignments, and task
    dependencies information for a schedule.
    
    :var scheduleUid: the schedule internal name (uid)
    :var scheduleUpdates: the schedule updates- GenericAttributesContainer{ object-schedule object
    tag,keyValContainer(can be empty),StringValContainer(can be  empty),typedAttributeContainer(can be empty)  }
    :var deletedDependencies: The deleted dependencies
    :var deletedAssignments: The deleted assignments
    :var newProxyTasks: The information to create new ProxyTask in this schedule
    :var proxyTaskUpdates: A list of known updated proxy tasks.
    :var deletedProxyTasks: A list of proxy tasks to be deleted.
    :var insertedSubSchedules: inserted schedules
    :var detachedSubSchedules: detatched sub schedules
    :var options: Schedule modification options
    1) logical Options (can be empty)
    2) Integer Options (can be empty)
    3) String Options (can be empty)
    :var newTasks: The new tasks to add
    :var newDependencies: The new dependencies
    :var newAssignments: The new assignments
    :var taskUpdates: The existing tasks update
    :var dependencyUpdates: The existing dependencies updates
    :var assignmentUpdates: The existing assignments update
    :var deletedTasks: The deleted tasks
    """
    scheduleUid: str = ''
    scheduleUpdates: GenericAttributesContainer = None
    deletedDependencies: List[TaskDependency] = ()
    deletedAssignments: List[ResourceAssignment] = ()
    newProxyTasks: List[GenericAttributesContainer] = ()
    proxyTaskUpdates: List[GenericAttributesContainer] = ()
    deletedProxyTasks: List[BusinessObject] = ()
    insertedSubSchedules: List[GenericAttributesContainer] = ()
    detachedSubSchedules: List[BusinessObject] = ()
    options: SchMgtOptions = None
    newTasks: List[GenericAttributesContainer] = ()
    newDependencies: List[GenericAttributesContainer] = ()
    newAssignments: List[GenericAttributesContainer] = ()
    taskUpdates: List[GenericAttributesContainer] = ()
    dependencyUpdates: List[GenericAttributesContainer] = ()
    assignmentUpdates: List[GenericAttributesContainer] = ()
    deletedTasks: List[ScheduleTask] = ()


@dataclass
class ScheduleModifyResponse(TcBaseObj):
    """
    The response of the schedule modification.
    
    :var newTasks: A list of new tasks.
    :var newProxyTasks: A list of new proxytasks.
    :var newDependencies: A list of new dependencies.
    :var newAssignments: A list of new assignments.
    """
    newTasks: List[ScheduleTask] = ()
    newProxyTasks: List[Fnd0ProxyTask] = ()
    newDependencies: List[TaskDependency] = ()
    newAssignments: List[ResourceAssignment] = ()


@dataclass
class ScheduleModifyResponses(TcBaseObj):
    """
    A collection of responses.
    
    :var serviceData: The service data
    :var responses: A collection of reponses.
    """
    serviceData: ServiceData = None
    responses: List[ScheduleModifyResponse] = ()
