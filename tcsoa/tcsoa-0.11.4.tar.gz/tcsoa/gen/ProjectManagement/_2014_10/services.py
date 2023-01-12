from __future__ import annotations

from tcsoa.gen.ProjectManagement._2014_10.ScheduleManagement import FailedObjectContainer, EVMDataRequest, AnalyticsMultipleResourceAssignmentStacks, InsertScheduleContainer, LoadResourceGraphContainer, EVMResultsResponse, DetachScheduleContainer, CostDetailResponse
from tcsoa.gen.ProjectManagement._2012_09.ScheduleManagement import AssignmentCreateContainer
from tcsoa.gen.ProjectManagement._2012_02.ScheduleManagement import CreatedObjectsContainer, TaskCreateContainer
from typing import List
from tcsoa.gen.BusinessObjects import ScheduleTask, Schedule, ResourceAssignment
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def getResourceGraphData(cls, loadResourceGraphContainer: LoadResourceGraphContainer) -> AnalyticsMultipleResourceAssignmentStacks:
        """
        The operation calculates the resource load information of one or more users assigned to ScheduleTask. The
        operation takes in a list of User objects as the input for whom the resource graph data is generated. You can
        specify the start date and end date to get the resource loading over the period of time specified by the start
        and end dates. The operation takes into account all the ScheduleTask objects in the system where the User is
        assigned to compute the resource load.
        
        Use cases:
        Create resource assignments histogram in Schedule Manager and Teamcenter Organization.
        
        Exceptions:
        >Error Severity: 
        Information - User has no task assignments.
        Error - User Uid is not valid
        """
        return cls.execute_soa_method(
            method_name='getResourceGraphData',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'loadResourceGraphContainer': loadResourceGraphContainer},
            response_cls=AnalyticsMultipleResourceAssignmentStacks,
        )

    @classmethod
    def insertSchedule(cls, insertScheduleContainer: List[InsertScheduleContainer]) -> ServiceData:
        """
        This operation inserts one or more Schedule specified in the input in a master Schedule. 
        You can specify in the input an optional parameter which if true, the operation will adjust the master Schedule
        start date and end date to be the same as the sub Schedule start date and end date. By default, the operation
        does not adjust the dates of the master Schedule to be the same as the sub Schedule dates.
        """
        return cls.execute_soa_method(
            method_name='insertSchedule',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'insertScheduleContainer': insertScheduleContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def replaceAssignment(cls, schedule: Schedule, newAssignments: List[AssignmentCreateContainer], assignmentDeletes: List[ResourceAssignment]) -> CreatedObjectsContainer:
        """
        This operation replaces a specified list of existing ResourceAssignment objects on a ScheduleTask with a
        specified list of new ResourceAssignment. The orginal ResourceAssignment specified in the input are deleted and
        new ResourceAssignment specified in the input are created on the ScheduleTask
        
        
        Use cases:
         In Schedule Manager, right click tasks and select Assignments->Replace Assignments.
        A dialogue will appear with current resources on the left hand side and the list of resources on the right hand
        side to replace the existing ones with. Select the resources on both the sides and click OK.
        
        Exceptions:
        >Service Exception when the resource assignments cannot be added on the task due to workflow process being
        already initiated on the ScheduleTask or there is no access privilege on the ScheduleTask
        
        230065     Resource assignments cannot be added, updated or deleted, and privileged user cannot be changed
        since the workflow process has been triggered at another site.
        230045     The user does not have the correct access privileges to modify one or more objects.
        230061     The schedule has been deleted and cannot be accessed.
        """
        return cls.execute_soa_method(
            method_name='replaceAssignment',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'schedule': schedule, 'newAssignments': newAssignments, 'assignmentDeletes': assignmentDeletes},
            response_cls=CreatedObjectsContainer,
        )

    @classmethod
    def verifySchedule(cls, schedule: Schedule) -> FailedObjectContainer:
        """
        This operation will verify the input Schedule for integrity of the scheduling data. The operation validates all
        the ScheduleTask, ResourceAssignment objects, TaskDependency, constraints in the Schedule for their effort
        driven scheduling values. It is recommended to use this operation to verify the integrity and data correctness
        of the Schedule before publishing the Schedule for execution.
        
        Use cases:
         
        
        Exceptions:
        >Service Exception when there are failures in retrieving the properties of the ScheduleTask or failures in
        retrieving the ScheduleTask of the Schedule.
        
        230040  Getting task properties failed. See system log for details.
        230041  Getting tasks in schedule failed. See system log for details.
        """
        return cls.execute_soa_method(
            method_name='verifySchedule',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'schedule': schedule},
            response_cls=FailedObjectContainer,
        )

    @classmethod
    def createPhaseGateTask(cls, taskInputContainer: TaskCreateContainer) -> CreatedObjectsContainer:
        """
        This operation creates a phase gate structure inside a Schedule. A phase gate structure comprises of a phase
        task, two milestones, a gate task and a finish to start TaskDependency between the phase and the gate tasks.
        The operation takes the start date,  finish date, work estimate of the phase task as input and computes the
        start and finish dates of the milestones and the gate task. The name sent in the input will be used for the
        names of the phase and gate tasks with the string "Phase" and "Gate" appended.
        """
        return cls.execute_soa_method(
            method_name='createPhaseGateTask',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'taskInputContainer': taskInputContainer},
            response_cls=CreatedObjectsContainer,
        )

    @classmethod
    def detachSchedule(cls, detachScheduleContainer: List[DetachScheduleContainer]) -> ServiceData:
        """
        This operation removes specified sub Schedule from a given master Schedule. It takes in as input the the sub
        Schedule that needs to be removed and the master Schedule from where the sub Schedule needs to be removed.
        """
        return cls.execute_soa_method(
            method_name='detachSchedule',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'detachScheduleContainer': detachScheduleContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def getCostRollupData(cls, costDetailRequest: List[ScheduleTask]) -> CostDetailResponse:
        """
        The operation calculates the total cost associated with either a Schedule or ScheduleTask. The total cost of a
        Schedule or ScheduleTask is calculated as below
        1) The total of the fixed costs specified on the Schedule or ScheduleTask
        2) The total of the costs of each ResourceAssignment based on the work hours and resource rate reported against
        the ScheduleTask.
        If there are any child ScheduleTask below the input ScheduleTask, the costs of the child ScheduleTask are
        accumulated into the costs of the parent ScheduleTask.
        """
        return cls.execute_soa_method(
            method_name='getCostRollupData',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'costDetailRequest': costDetailRequest},
            response_cls=CostDetailResponse,
        )

    @classmethod
    def getEVMResults(cls, inputEVMData: EVMDataRequest) -> EVMResultsResponse:
        """
        The operation calculates the earned valued results for Schedule or ScheduleTask. The operation takes in input
        the Schedule or ScheduleTask  on which the earned value calculated data is sought and the criteria for the
        calculations. The earned value is calculated for the following labels -
        Planned Value (PV), Earned Value (EV), Actual Cost (AC) or Actual Cost of Work Performed, (ACWP) (Actual
        Effort), Cost Variance (CV), Budget at Completion (BAC), Forecast at Completion (FAC), Estimate at Completion
        (EAC), Schedule Variance (SV), Schedule Performance Index (SPI),Cost Performance Index (CPI)
        """
        return cls.execute_soa_method(
            method_name='getEVMResults',
            library='ProjectManagement',
            service_date='2014_10',
            service_name='ScheduleManagement',
            params={'inputEVMData': inputEVMData},
            response_cls=EVMResultsResponse,
        )
