from __future__ import annotations

from tcsoa.gen.BusinessObjects import EPMJob, Fnd0ProxyTask, WorkspaceObject, POM_object, ScheduleTask, ResourceAssignment, TaskDependency, User, Discipline
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssignmentCreateContainer(TcBaseObj):
    """
    The information needed to create a new assignment to a task.
    
    :var task: The task to assign the resource.
    :var user: The user being assigned (or null if discipline assignment).
    :var discipline: The discipline of the assignee or the discipline for the assignment.
    :var assignedPercent: The percentage effort being assigned (I.E. 50.0 == 50%)
    """
    task: ScheduleTask = None
    user: User = None
    discipline: Discipline = None
    assignedPercent: float = 0.0


@dataclass
class AssignmentUpdateContainer(TcBaseObj):
    """
    Container for assignment updates.
    
    :var assignment: The assignment to update
    :var newEffort: The new % effort of that assignee.
    """
    assignment: ResourceAssignment = None
    newEffort: float = 0.0


@dataclass
class LaunchedWorkflowContainer(TcBaseObj):
    """
    Information about the launched workflows.
    
    :var launchedWorkflows: The launched workflow processes.
    :var serviceData: The service data.
    """
    launchedWorkflows: List[EPMJob] = ()
    serviceData: ServiceData = None


@dataclass
class MoveRequest(TcBaseObj):
    """
    The information required to move a task.
    
    :var task: The task or proxy task to move.
    :var newParent: The new parent for the task.
    :var prevSibling: The new previous sibling for the task (or the reference task in the case of a proxy).
    """
    task: WorkspaceObject = None
    newParent: ScheduleTask = None
    prevSibling: ScheduleTask = None


@dataclass
class ObjectUpdateContainer(TcBaseObj):
    """
    Information to update an object.
    
    :var object: The object being updated.
    :var updates: The updates to the main type.
    :var typedUpdates: Updates for a custom type.
    """
    object: POM_object = None
    updates: List[AttributeUpdateContainer] = ()
    typedUpdates: List[TypedAttributeUpdateContainer] = ()


@dataclass
class AttributeUpdateContainer(TcBaseObj):
    """
    Holds the name and value of an attribute.
    
    :var attrName: The name of the attribute.
    :var attrValue: The value of the attribute.
    :var attrType: An integer to help determine the data type of the attribute. Valid values- {
    1=String_type,2=Integer_type,3=Long_type,4=Double_type,5=Float_type,6=Boolean_type,7=Date_type,8=Cal_type }
    """
    attrName: str = ''
    attrValue: str = ''
    attrType: int = 0


@dataclass
class TaskCreateContainer(TcBaseObj):
    """
    The information needed to create a task.
    
    :var name: The name.
    :var desc: The description.
    :var objectType: The type to create (typically "ScheduleTask").
    :var start: The start date and time.
    :var finish: The finish date and time.
    :var workEstimate: The work estimate in minutes.
    :var parent: The summary task to create the new task under.
    :var prevSibling: The task to create this new task after.  Must currently exist under the parent.  Can be null.
    :var otherAttributes: Additional optional attributes: priority
    :var typedOtherAttributes: Other attributes required to create the objectType specified.
    """
    name: str = ''
    desc: str = ''
    objectType: str = ''
    start: datetime = None
    finish: datetime = None
    workEstimate: int = 0
    parent: ScheduleTask = None
    prevSibling: ScheduleTask = None
    otherAttributes: List[AttributeUpdateContainer] = ()
    typedOtherAttributes: List[TypedAttributeUpdateContainer] = ()


@dataclass
class TypedAttributeUpdateContainer(TcBaseObj):
    """
    Updates for a certain type of object.
    
    :var objectType: The object type containing the attributes.
    :var updates: The list of attributes and their values.
    """
    objectType: str = ''
    updates: List[AttributeUpdateContainer] = ()


@dataclass
class CreatedDependenciesContainer(TcBaseObj):
    """
    New  dependencies container
    
    :var createdDependencies: The dependencies created
    :var createdProxyTasks: The created proxy tasks
    :var updatedTasks: The tasks which were updated due to
    :var serviceData: The SOA service data
    """
    createdDependencies: List[TaskDependency] = ()
    createdProxyTasks: List[Fnd0ProxyTask] = ()
    updatedTasks: List[ScheduleTask] = ()
    serviceData: ServiceData = None


@dataclass
class CreatedObjectsContainer(TcBaseObj):
    """
    The container of created objects
    
    :var createdObjects: The objects which were created.
    :var updatedTasks: The tasks affected by the creation.
    :var serviceData: The service data.
    """
    createdObjects: List[POM_object] = ()
    updatedTasks: List[ScheduleTask] = ()
    serviceData: ServiceData = None


@dataclass
class CriticalTasksContainer(TcBaseObj):
    """
    The tasks on the critical path.
    
    :var tasks: The tasks on the critical path.
    :var proxyTasks: The proxy tasks on the critical path.
    :var serviceData: The service data.
    """
    tasks: List[ScheduleTask] = ()
    proxyTasks: List[Fnd0ProxyTask] = ()
    serviceData: ServiceData = None


@dataclass
class DeleteTaskContainer(TcBaseObj):
    """
    Information about the deleted tasks.
    
    :var orphaned: Tasks which were orphaned(as they could not be deleted).
    :var updated: Tasks updated due to the delete.
    :var serviceData: The service data.
    """
    orphaned: List[ScheduleTask] = ()
    updated: List[ScheduleTask] = ()
    serviceData: ServiceData = None


@dataclass
class DependencyCreateContainer(TcBaseObj):
    """
    Creates Dependencies between tasks in the same schedule, between a task and a proxy task in the same schedule, or
    between a tasks in different schedules (but in the same master schedule).  It returns the created dependencies,
    created proxy tasks (if any), and the objects affected by this change
    
    :var predTask: The predecessor task for the dependency.
    :var succTask: The successor task for the dependency.
    :var depType: The type of dependency: 0-FS, 1-FF, 2-SS, 3-SF
    :var lagTime: The lag time in minutes (480 ~ 1 day)
    """
    predTask: WorkspaceObject = None
    succTask: WorkspaceObject = None
    depType: int = 0
    lagTime: int = 0


@dataclass
class DependencyUpdateContainer(TcBaseObj):
    """
    Update dependency container
    
    :var dependency: The dependency to update.
    :var newType: The new type for the dependency.
    :var newLag: The new lag for the dependnecy.
    """
    dependency: TaskDependency = None
    newType: int = 0
    newLag: int = 0
