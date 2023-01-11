from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Workflow._2008_06.Workflow import Resources
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetRegisteredHandlerResponse(TcBaseObj):
    """
    Returns list of registered action and rule handler names.
    
    :var actionHandlers: A list of names of registered action handlers.
    :var ruleHandlers: A list of names of registered rule handlers.
    :var serviceData: The service data.
    """
    actionHandlers: List[str] = ()
    ruleHandlers: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateHandlerResponse(TcBaseObj):
    """
    Response of createOrUpdateHandler operation.
    
    :var createdorUpdatedObjects: A list of CreateUpdateHandlerOutput structure.
    :var serviceData: The service data.
    """
    createdorUpdatedObjects: List[CreateUpdateHandlerOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdatePALResponse(TcBaseObj):
    """
    Response structure returned by createOrUpdatePAL operation.
    
    :var createdorUpdatedObjects: A list of CreateUpdatePALOutput structure.
    :var serviceData: The service data.
    """
    createdorUpdatedObjects: List[CreateUpdatePALOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateTemplateResponse(TcBaseObj):
    """
    Response of createOrupdate operation.
    
    :var createdorUpdatedObjects: A list of CreateUpdateTemplateOutput structure.
    :var serviceData: The service data.
    """
    createdorUpdatedObjects: List[CreateUpdateTemplateOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateUpdateHandlerInput(TcBaseObj):
    """
    Input structure to pass requried data for create or update handler.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var handlerName: Name of the handler to be created. This name represents registered workflow handlers only. For
    example: If User want to create a new action handler named "EPM-set-status" then user need to pass same name in
    this input.This input is required for create case.
    :var taskTemplate: UID of EPMTaskTemplate object on which handler is to be created or updated.
    :var businessRule: UID of EPMBusinessRule object.This object represents the workflow business rule.This input is
    required for create case ( creating new Rule Handler). For create case if the handlerType input is set to "Rule" (
    user is creating new Rule Handler ) then user don&rsquo;t need to pass this input and SOA operation will create its
    own new object of EPMBusinessRule and newly created workflow handler instance ( EPMHandler ) will be attached to it.
    :var handlerType: Type of the handler to be created. Required input for create and the supported values are:
    "Rule"    : Creates rule handler.
    "Action" : Creates action handler.
    :var handlerToUpdate: UID of the EPMHandler object to be updated. If this  input is provided then it will be
    considered as update case.
    :var action: The action of the workflow task on which new handler will be added. Required for create.
    Supported values are:
     Action    Value
    Assign          1
    Start              2
    Complete  4
    Promote      5
    Suspend      6
    Resume      7
    Undo          8
    Abort          9
    Perform     100
    :var ruleQuorum: The rule quorum value to specify whether one rule, all rules, or a number of rules must be
    satisfied for the task to progress. Below are the accepted values :
     -1 :  means all. In this case, every rule must pass to meet the quorum.
    A number greater than 1, but less than the number of already added Rule handler in the Rule container. Any invalid
    input will be ignored.
    :var changeExecutionOrder: The position of the handler in added handler(s) array on particularaction of the
    EPMTaskTemplate. For example specifying the -1 position moves the given handler (handlerToUpdate input) up in a
    handler array. Similarly specifying the 1 position moves the given handler down in a handler array. Any invalid
    input will be ignored.
    :var additionalData: A map (string, list of strings) to send additional information. This map is used to pass
    argument data to the handler to be created or updated.Handler arguments varies from handler to handler. User need
    to pass the requried/optional arguments as documented in Teamcenter workflow handler document. Below is an example
    of EPM-set-status handler:
    
    Key : -action     
    Values : {"append"}
    Description : Support values are:"append", "rename", "replace", or delete.
    
    Key : -status     
    Values : {"name_of_status"}
    Description : Specifies the name of the release status.
    """
    clientID: str = ''
    handlerName: str = ''
    taskTemplate: str = ''
    businessRule: str = ''
    handlerType: str = ''
    handlerToUpdate: str = ''
    action: int = 0
    ruleQuorum: int = 0
    changeExecutionOrder: int = 0
    additionalData: KeyValuesMap = None


@dataclass
class CreateUpdateHandlerOutput(TcBaseObj):
    """
    Structure represents the output of createOrUpdateHandler operation.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify  return data elements and
    partial errors associated with the input  structure.
    :var handlerObject: Updated or created EPMHandler object.
    :var ruleObject: Updated or created EPMBusinessRule object.
    """
    clientID: str = ''
    handlerObject: BusinessObject = None
    ruleObject: BusinessObject = None


@dataclass
class CreateUpdatePALInput(TcBaseObj):
    """
    Input stucture used to update or copy EPMAssignmentList or to create a new EPMAssignmentList.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var palName: Name of the EPMAssignmentList to be updated or newly created . In case of copy operation, this is the
    name of new EPMAssignmentList to be created.
    :var workflowTemplate: UID of EPMTaskTemplate object for which process assignment list is to be created or updated
    or copied.
    :var palDescription: Description of process assignment list.
    :var resourceLists: A list of Resources to be assigned.
    :var additionalData: A map (string, list of strings) to send additional information. Currently supported keys and
    values are:
    
    - Key:  "isShared"
    - Values :  {"true", "false"}
    - Description: If true, a shared assignment list is created or updated. If this key values pair is not passed or
    &lsquo;false&rsquo;                                                 value is passed then the assignment list is not
    shared.
    
    
    
    - Key:  "palToUpdate"
    - Values : {"palUIDToUpdate"}
    - Description: &lsquo;palUIDToUpdate&rsquo; is the UID of EPMAssignmentList which has to be updated.
    
    
    
    - Key:  "palToCopy"
    - Values : {"palUIDToCopy"}
    - Description: &lsquo;palUIDToCopy&rsquo; is the UID of EPMAssignmentList which has to be copied.
    
    
    
    Keys &lsquo;palToUpdate&rsquo; and &lsquo;palToCopy&rsquo; are supported mutually exclusively. If both keys are
    provided, then error #219031 is returned. If none of the keys, &lsquo;palToUpdate&rsquo; and
    &lsquo;palToCopy&rsquo; are provided; then a new assignment list is created.
    """
    clientID: str = ''
    palName: str = ''
    workflowTemplate: str = ''
    palDescription: List[str] = ()
    resourceLists: List[Resources] = ()
    additionalData: KeyValuesMap = None


@dataclass
class CreateUpdatePALOutput(TcBaseObj):
    """
    CreateUpdatePALOutput structure.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var palObject: Updated or created EPMAssignmentList object.
    """
    clientID: str = ''
    palObject: BusinessObject = None


@dataclass
class CreateUpdateTemplateInput(TcBaseObj):
    """
    Input structure used for passing requried data for create or update template object.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var templateName: Name of the task template to be created or updated.
    :var templateDesc: Description of the task template to be created or updated.
    :var baseTemplate: UID of EPMTaskTemplate object which will be used as a base template.Basically new template to be
    created will be a exact copy of this template. This is requried for create operation.
    :var parentTemplate: UID of EPMTaskTemplate object represents the parent object. New template will be created as a
    child or sub template of this parent template input. This is requried for create operation.
    :var templateToUpdate: UID of the EPMTaskTemplate object to be updated. If this input is provided then this
    operation will be considered as update case.
    :var additionalData: A map (string, list of strings) to send additional data. This input is reserverd for future
    use.
    """
    clientID: str = ''
    templateName: str = ''
    templateDesc: str = ''
    baseTemplate: str = ''
    parentTemplate: str = ''
    templateToUpdate: str = ''
    additionalData: KeyValuesMap = None


@dataclass
class CreateUpdateTemplateOutput(TcBaseObj):
    """
    Struture holds the created or updated template object.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with the input structure.
    :var templateObject: Updated or created EPMTaskTemplate object.
    """
    clientID: str = ''
    templateObject: BusinessObject = None


"""
A map (string, list of strings) to send additional information.
"""
KeyValuesMap = Dict[str, List[str]]
