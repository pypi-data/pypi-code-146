from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_imc, User
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateRemoteWkfInput(TcBaseObj):
    """
    A structure containing information used for workflow replication (e.g. the name of the process template, workflow
    owner, responsible party, export site, attachments, and attachment relations).
    
    :var processName: Workflow process name.
    :var processDescription: Workflow process description.
    :var attachmentRelationTypes: A list of relation type names to use while attaching the attachments to the workflow
    process (e.g. CMHasProblemItem, CMHasSolutionItem, Fnd0EPMTarget).
    :var processTemplate: Name of the workflow process template used for creating the workflow process. This template
    should exist at the site where the workflow is created.
    :var workflowOwner: Owner of the workflow process.
    :var responsibleParty: Responsible party (Users or ResourcePool) of the root task.
    :var assignedUserList: Users or ResourcePool objects to be used for task assignment.
    :var dueDate: The due date of the source object (e.g. Schedule Task).
    :var sourceObject: Source object (e.g. ScheduleTask).
    :var site: The site where the workflow needs to be created.
    :var attachments: A list of attachments to the workflow process (e.g. ItemRevision, Dataset).
    """
    processName: str = ''
    processDescription: str = ''
    attachmentRelationTypes: List[str] = ()
    processTemplate: str = ''
    workflowOwner: User = None
    responsibleParty: BusinessObject = None
    assignedUserList: List[str] = ()
    dueDate: datetime = None
    sourceObject: BusinessObject = None
    site: POM_imc = None
    attachments: List[BusinessObject] = ()


@dataclass
class CreateWkfInput(TcBaseObj):
    """
    A structure containing the process template name ,workflow process owner, responsible party, attachments, and
    attachment relations. Intent of structure is to hold input data that is required to create a workflow process.
    
    :var processName: Workflow process name.
    :var processDescription: Workflow process description.
    :var processTemplate: Name of the workflow process template used for creating the workflow process.
    :var workflowOwner: User assigned as the owner of the workflow process.
    :var responsibleParty: Responsible party of the workflow process root task. Responsible party can be a User or a
    ResourcePool.
    :var assignedUserList: A list of Users or ResourcePool objects  to be used for task assignment.
    :var dueDate: Task due date.
    :var attachments: A list of attachments to the workflow process (e.g. ItemRevision, Dataset).
    :var attachmentRelationTypes: A list of relation type names to use while attaching the attachment objects to the
    workflow process (e.g. CMHasProblemItem, CMHasSolutionItem, Fnd0EPMTarget).
    """
    processName: str = ''
    processDescription: str = ''
    processTemplate: str = ''
    workflowOwner: User = None
    responsibleParty: BusinessObject = None
    assignedUserList: List[BusinessObject] = ()
    dueDate: datetime = None
    attachments: List[BusinessObject] = ()
    attachmentRelationTypes: List[str] = ()


@dataclass
class CreateWkfOutput(TcBaseObj):
    """
    A structure containing the UID of the workflow root task, a NameValuePairs data type that holds root task property
    names and values, and service data. Intent of structure is to be an output parameter used to hold data pertaining
    to a newly created workflow process following the creation of the workflow process.
    
    :var workflowTask: Workflow root task.
    :var attributes: A map (string/string) of workflow root task property names and values. (e.g. status, process
    instructions, task_result).
    :var serviceData: Service data.
    """
    workflowTask: BusinessObject = None
    attributes: NameValuePairs = None
    serviceData: ServiceData = None


"""
A map (string/string) of attributes names and initial value pairs.
"""
NameValuePairs = Dict[str, str]
