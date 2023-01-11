from __future__ import annotations

from tcsoa.gen.Workflow._2008_06.Workflow import AttachmentInfo, ProcessTemplates, ChangeStateInputInfo, AuditFile, ChangeStateOutput, InstanceInfo, Resources, Templates, SoaEPMSupportingValues, ContextData, GroupRoleRef, CreateSignoffs, AssignmentLists, AllOrAssigned, Tasks, GetResourcePoolOutput, SoaEPMAction, RemoveSignoffsInfo
from tcsoa.gen.BusinessObjects import BusinessObject, Signoff, EPMJob, WorkspaceObject, EPMAssignmentList, EPMTask
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def getResourcePool(cls, groupRoleRef: List[GroupRoleRef]) -> GetResourcePoolOutput:
        """
        getResourcePool - Returns regular or all member ResourcePools corresponding
        to the list of GroupRoleRef (group and role)
        """
        return cls.execute_soa_method(
            method_name='getResourcePool',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'groupRoleRef': groupRoleRef},
            response_cls=GetResourcePoolOutput,
        )

    @classmethod
    def getWorkflowTemplates(cls, targets: List[WorkspaceObject], allOrAssignedCriteria: AllOrAssigned) -> Templates:
        """
        Get the list of workflow templates given the list of target workspace objects and the All or Assigned criteria.
        
        Description
        This SOA will return all the ready to use and under construction templates if the allorAssined criteria is
        SOA_EPM_ALL.
        If the allOrAssignedCriteria is set to SOA_EPM_Assigned, this SOA will get the group information and the
        configured filtering criteria from the session
        and using the list of target objects, return the filtered list of workflow templates.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowTemplates',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'targets': targets, 'allOrAssignedCriteria': allOrAssignedCriteria},
            response_cls=Templates,
        )

    @classmethod
    def addAttachments(cls, task: EPMTask, attachments: AttachmentInfo) -> ServiceData:
        """
        addAttachments - Add attachments to a task.
        """
        return cls.execute_soa_method(
            method_name='addAttachments',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'task': task, 'attachments': attachments},
            response_cls=ServiceData,
        )

    @classmethod
    def listDefinitions(cls, name: str, templatestatus: int) -> ProcessTemplates:
        """
        Gets a list of process templates based on the criteria passed.
        
        Description
        if name and status are specified, all the templates matching the name and the status are returned.
        If only name is specified, only the available templates matching the name will be returned
        If only status is specified, all the templates with the specified status is returned.
        If both are not specified, all the available templates will be returned for a non-Dba
        """
        return cls.execute_soa_method(
            method_name='listDefinitions',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'name': name, 'templatestatus': templatestatus},
            response_cls=ProcessTemplates,
        )

    @classmethod
    def performAction(cls, task: EPMTask, action: SoaEPMAction, comments: str, password: str, supportingValue: SoaEPMSupportingValues, supportingObject: BusinessObject) -> ServiceData:
        """
        Performs workflow actions on a task.
        The actions that can be performed using this operation are :
        assign, start, complete, skip, suspend, resume, undo, perform, approve, reject, promote and demote.
        Note: Special case
        This operation can be used to set only comments without changing the decision for perform signoff task.
        To do that, use the 'EPM_no_action' as input for action argument and use the current decision for the
        supportingValue argument.
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='performAction',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'task': task, 'action': action, 'comments': comments, 'password': password, 'supportingValue': supportingValue, 'supportingObject': supportingObject},
            response_cls=ServiceData,
        )

    @classmethod
    def removeAttachments(cls, task: EPMTask, attachments: List[BusinessObject]) -> ServiceData:
        """
        removeAttachments - Remove attachments to a task.
        """
        return cls.execute_soa_method(
            method_name='removeAttachments',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'task': task, 'attachments': attachments},
            response_cls=ServiceData,
        )

    @classmethod
    def removeSignoffs(cls, signoffs: List[RemoveSignoffsInfo]) -> ServiceData:
        """
        addSignoffs - Add/remove and update signoffs on a task
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='removeSignoffs',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'signoffs': signoffs},
            response_cls=ServiceData,
        )

    @classmethod
    def viewAuditFile(cls, auditedObject: BusinessObject, isSignoffReport: bool) -> AuditFile:
        """
        viewAuditFile - get audit information on the selected object when stored in a file.
        By default, audit info is stored in a file in teamcenter.  This operation cannot be used to get audit
        info when audit manager is turned on.
        """
        return cls.execute_soa_method(
            method_name='viewAuditFile',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'auditedObject': auditedObject, 'isSignoffReport': isSignoffReport},
            response_cls=AuditFile,
        )

    @classmethod
    def createInstance(cls, startImmediately: bool, observerKey: str, name: str, subject: str, description: str, contextData: ContextData) -> InstanceInfo:
        """
        Workflow processes are the instantiations from workflow templates. This operation can be used to create a
        workflow process or sub process at a local or a remote site from a given workflow template. 
        """
        return cls.execute_soa_method(
            method_name='createInstance',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'startImmediately': startImmediately, 'observerKey': observerKey, 'name': name, 'subject': subject, 'description': description, 'contextData': contextData},
            response_cls=InstanceInfo,
        )

    @classmethod
    def addSignoffs(cls, signoffs: List[CreateSignoffs]) -> ServiceData:
        """
        addSignoffs : Add signoffs on a task
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='addSignoffs',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'signoffs': signoffs},
            response_cls=ServiceData,
        )

    @classmethod
    def delegateSignoff(cls, delegatee: BusinessObject, signoff: Signoff) -> ServiceData:
        """
        Delegate a signoff to a different groupmember or a resourcepool.
        """
        return cls.execute_soa_method(
            method_name='delegateSignoff',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'delegatee': delegatee, 'signoff': signoff},
            response_cls=ServiceData,
        )

    @classmethod
    def assignAllTasks(cls, process: EPMJob, assignmentList: EPMAssignmentList, resources: List[Resources]) -> ServiceData:
        """
        Assign a process assignment list to a process.
        Description:
        If the assignment list is given, it will use it to apply the assignment list to the
        process.  If the assignment is not given, it will loop through the Resources structure and create the list
        of task templates and list of resources, profiles and other information to apply the resources to
        the process. Thus at a given time either assignmentList and resources both cannot be null. either one of them
        can be null
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='assignAllTasks',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'process': process, 'assignmentList': assignmentList, 'resources': resources},
            response_cls=ServiceData,
        )

    @classmethod
    def getAllTasks(cls, process: EPMJob, state: int) -> Tasks:
        """
        Gets all the tasks in a process
        """
        return cls.execute_soa_method(
            method_name='getAllTasks',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'process': process, 'state': state},
            response_cls=Tasks,
        )

    @classmethod
    def getAssignmentLists(cls, names: List[str]) -> AssignmentLists:
        """
        Gets the process assignment list given the process assignment list names
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='getAssignmentLists',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'names': names},
            response_cls=AssignmentLists,
        )

    @classmethod
    def changeState(cls, stateInput: ChangeStateInputInfo) -> ChangeStateOutput:
        """
        changeState - Change the state of a process or a task at a remote site.
        """
        return cls.execute_soa_method(
            method_name='changeState',
            library='Workflow',
            service_date='2008_06',
            service_name='Workflow',
            params={'stateInput': stateInput},
            response_cls=ChangeStateOutput,
        )
