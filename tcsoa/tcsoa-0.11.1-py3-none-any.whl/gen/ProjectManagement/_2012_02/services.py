from __future__ import annotations

from tcsoa.gen.ProjectManagement._2012_02.ScheduleManagement import TaskCreateContainer, CreatedDependenciesContainer, AssignmentUpdateContainer, DeleteTaskContainer, DependencyCreateContainer, DependencyUpdateContainer, LaunchedWorkflowContainer, CriticalTasksContainer, MoveRequest, AssignmentCreateContainer, ObjectUpdateContainer, CreatedObjectsContainer
from typing import List
from tcsoa.gen.BusinessObjects import WorkspaceObject, ScheduleTask, Schedule, ResourceAssignment, TaskDependency
from tcsoa.gen.ProjectManagement._2011_06.ScheduleManagement import SchMgtOptions
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from datetime import datetime


class ScheduleManagementService(TcService):

    @classmethod
    def launchScheduledWorkflow(cls, tasks: List[ScheduleTask]) -> LaunchedWorkflowContainer:
        """
        A Teamcenter schedule  task can be configured in such a way that when certain conditions are
        met the associated workflow can be initiated. The triggering rules or conditions
        create a workflow process. If there are updates to the workflow process tasks, a
        notification is sent to the Teamcenter schedule task so that the schedule task can be
        updated. This operation launches workflows associated with the tasks .
        
        """
        return cls.execute_soa_method(
            method_name='launchScheduledWorkflow',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'tasks': tasks},
            response_cls=LaunchedWorkflowContainer,
        )

    @classmethod
    def moveTasks(cls, schedule: Schedule, moveRequests: List[MoveRequest]) -> ServiceData:
        """
        Allow schedule tasks and proxy tasks to be moved to a different location in the task hierarchy.
        The schedule task move requests are specified in the 'MoveRequest' structure, which store information about
        schedule task object, its new parent and its new previous sibling. Additional errors during this operation will
        be returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='moveTasks',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'moveRequests': moveRequests},
            response_cls=ServiceData,
        )

    @classmethod
    def recalculateScheduleNonInteractive(cls, schedule: Schedule, recalcType: int, runAsync: bool) -> ServiceData:
        """
        This operation performs the revalidation/rerunning of the business logic on the properties of the schedule and
        its child objects based on the requested properties flag or ALL. Interactive use of this operation is not
        recommended.
        """
        return cls.execute_soa_method(
            method_name='recalculateScheduleNonInteractive',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'recalcType': recalcType, 'runAsync': runAsync},
            response_cls=ServiceData,
        )

    @classmethod
    def scaleScheduleNonInteractive(cls, schedule: Schedule, scaleFactor: float, options: SchMgtOptions) -> ServiceData:
        """
        The scale schedule operation allows for the user to scale the schedule based on specified lag time.
        This operation throws a 'ServiceException' in case of failure. The service exception will contain the error
        message of the failure. Additional errors will be returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='scaleScheduleNonInteractive',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'scaleFactor': scaleFactor, 'options': options},
            response_cls=ServiceData,
        )

    @classmethod
    def shiftScheduleNonInteractive(cls, schedule: Schedule, newDate: datetime, newFinish: bool) -> ServiceData:
        """
        Shifts the schedule forward or backwards to the new provided start/finish date.
        """
        return cls.execute_soa_method(
            method_name='shiftScheduleNonInteractive',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newDate': newDate, 'newFinish': newFinish},
            response_cls=ServiceData,
        )

    @classmethod
    def updateAssignments(cls, schedule: Schedule, assignmentUpdates: List[AssignmentUpdateContainer]) -> ServiceData:
        """
        The operation updates the resource assignments in a given schedule. Only the resource load of the assignment
        can be updated with this operation. It returns the 'ServiceData' which will have information of updated
        assignment objects. This operation throws a 'ServiceException' in case of failure. The service exception will
        contain the error message of the failure. Additional errors will be returned in the list of partial errors in
        the 'ServiceData'. 
        """
        return cls.execute_soa_method(
            method_name='updateAssignments',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'assignmentUpdates': assignmentUpdates},
            response_cls=ServiceData,
        )

    @classmethod
    def updateDependencies(cls, schedule: Schedule, dependencyUpdates: List[DependencyUpdateContainer]) -> ServiceData:
        """
        This operation  updates the dependencies in a given schedule. It takes an array of 'DependencyUpdateContainer'
        objects in which the type of the dependency,  and lag time updates can be specified per dependency object.
        """
        return cls.execute_soa_method(
            method_name='updateDependencies',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'dependencyUpdates': dependencyUpdates},
            response_cls=ServiceData,
        )

    @classmethod
    def updateSchedules(cls, scheduleUpdates: List[ObjectUpdateContainer]) -> ServiceData:
        """
        Updates all the affected scheduling objects based on the initial users request to the application interface. 
        Properties on the Schedule object like object name, description, start date, finish date, status, is schedule
        template, wbsformat,  customer name, customer number , published, is public and priority etc can be updated
        with  this operation.
        """
        return cls.execute_soa_method(
            method_name='updateSchedules',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'scheduleUpdates': scheduleUpdates},
            response_cls=ServiceData,
        )

    @classmethod
    def updateTasks(cls, schedule: Schedule, updates: List[ObjectUpdateContainer]) -> ServiceData:
        """
        Updates the specified tasks in a given schedule. Task updates are specified in the 'ObjectUpdateContainer' 
        structure. All the scheduling data properties and execution data properties on the schedule task can be
        updated. Updates on the summary tasks are not allowed. This operation supports updating the custom attributes
        of OOTB schedule tasks  as well as custom schedule tasks. The updated objects are returned back in the service
        data of the response. This operation throws a 'ServiceException' in case of failure. The service exception will
        contain the error message of the failure. Additional errors will be returned in the list of partial errors in
        the 'ServiceData'.
        
        
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='updateTasks',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'updates': updates},
            response_cls=ServiceData,
        )

    @classmethod
    def createDependencies(cls, schedule: Schedule, newDependencies: List[DependencyCreateContainer]) -> CreatedDependenciesContainer:
        """
        Creates 'Dependencies' between tasks in the same schedule, between a task and a proxy task in the same
        schedule, or between a tasks in different schedules (but in the same master schedule).  It returns the created
        dependencies, created proxy tasks (if any), and the objects affected by this change. This operation throws a
        'ServiceException' in case of failure. The service exception will contain the error message of the failure.
        Additional errors will be returned in the list of partial errors in the 'ServiceData'. 
        
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='createDependencies',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newDependencies': newDependencies},
            response_cls=CreatedDependenciesContainer,
        )

    @classmethod
    def createTasks(cls, schedule: Schedule, createContainers: List[TaskCreateContainer]) -> CreatedObjectsContainer:
        """
        Creates the specified tasks in a given schedule. The information needed to create task are specified in the
        'TaskCreateContainer' structure. It returns 'CreatedObjectsContainer' which will have information of created
        tasks, updated tasks and 'ServiceData'. Throws a 'ServiceException' in case of failure. The service exception
        will contain the error message of the failure. Additional errors will be returned in the list of partial errors
        in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='createTasks',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'createContainers': createContainers},
            response_cls=CreatedObjectsContainer,
        )

    @classmethod
    def deleteAssignments(cls, schedule: Schedule, assignmentDeletes: List[ResourceAssignment]) -> ServiceData:
        """
        This operation deletes resource assignments from the tasks in the given schedule. It takes schedule from which
        assignments is to be deleted and array of resource assignments to be deleted as input.
        The deleted resource assignment objects are returned in the 'deletedObjects' of the 'ServiceData'. Operation
        throws a 'ServiceException' in case of failure. The service exception will contain the error message of the
        failure. Additional errors will be returned in the list of partial errors in the 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='deleteAssignments',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'assignmentDeletes': assignmentDeletes},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteDependencies(cls, schedule: Schedule, dependencyDeletes: List[TaskDependency]) -> ServiceData:
        """
        This operation deletes the dependencies between the tasks in a given Schedule. 
        """
        return cls.execute_soa_method(
            method_name='deleteDependencies',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'dependencyDeletes': dependencyDeletes},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteTasks(cls, schedule: Schedule, deleteTasks: List[WorkspaceObject]) -> DeleteTaskContainer:
        """
        Deletes the requested tasks along with the sub tasks, assignments, dependencies, and task deliverables.
        """
        return cls.execute_soa_method(
            method_name='deleteTasks',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'deleteTasks': deleteTasks},
            response_cls=DeleteTaskContainer,
        )

    @classmethod
    def findCriticalPathTasks(cls, schedule: Schedule) -> CriticalTasksContainer:
        """
        This operation finds and returns the tasks on the critical path of the schedule. The critical path is the task
        or tasks that would likely affect the last task in the schedule if they were completed late. The critical path
        is calculated by determining the last task in the project (time wise). Any task where a slip would delay the
        last task in the project is on the critical path. Tasks linked by dependencies have a longer critical path
        (chain of tasks). The tasks on the critical path with the longest sequence of dependent tasks merit the most
        attention to on-time completion in order to avoid delays.
        """
        return cls.execute_soa_method(
            method_name='findCriticalPathTasks',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule},
            response_cls=CriticalTasksContainer,
        )

    @classmethod
    def assignResources(cls, schedule: Schedule, createAssignments: List[AssignmentCreateContainer]) -> CreatedObjectsContainer:
        """
        This operation assigns resources (Users and Disciplines) to tasks in a given schedule. The operation returns
        the 'CreatedObjectsContainer' which will have information of created assignments, updated tasks and service
        data.The operation throws a 'ServiceException' in case of failure. The service exception will contain the error
        message of the failure. 
        
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='assignResources',
            library='ProjectManagement',
            service_date='2012_02',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'createAssignments': createAssignments},
            response_cls=CreatedObjectsContainer,
        )
