from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class WorkflowTaskViewModelInput(TcBaseObj):
    """
    WorkflowTaskViewModelInput stucture that represent the input EPMTask or Signoff and its properties.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var selection: The selected EPMTask or Signoff object data for which the information to be sent in a JSON format.
    :var typeToPropertiesMap: A map (string, list of strings) represents the different properties of the task with type
    name. This input specify the properties of the  task to be outputted to JSON string.
    If a client wants to get a property value of an object which can be traversed using a reference property on a given
    input task then following format need to be used :
    REF( reference_property_name, reference_object_type ).property_on_reference_object
    
    For example : If the client wants to get object_string of workflow process (EPMJob), then it has to provide the
    input data in following format : 
    "EPMTask", "REF(parent_process,EPMJob).object_string"}
    
    In above example :
    reference_property_name is the "parent_process" reference    property defined on EPMTask.
    reference_object_type is the "EPMJob" referenced by the "parent_process" property on EPMTask.
    property_on_reference_object  is the "object_string". property on EPMJob.
    
    Below are the few examples of this input:
    To get task properties: "EPMTask", {"state_value", "signoff_quorum"}
    To get task reference property :"EPMTask", {"REF(parent_process,EPMJob).object_string"}
    To get task signoff data : "Signoff", {"REF(group_member,GroupMember).group", "REF(group_member,GroupMember).user",
    "fnd0DecisionRequired" }
    To get task signoff profile data : "EPMSignoffProfile",{"REF(group,Group).name", "REF(role,Role).role_name",
    "number_of_signoffs"}
    """
    clientId: str = ''
    selection: BusinessObject = None
    typeToPropertiesMap: KeyValueMap = None


@dataclass
class WorkflowTaskViewModelOutput(TcBaseObj):
    """
    Output structure represents the task data in JSON string and the additional data if any.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var additionalData: A map (string, list of strings) represents the additional information required by client.For
    example this operation returns logical flag to specify if the complete button can be enabled for the selected task
    in the perform dialog.
    :var taskJSONStrings: A map (string, list of strings) represents the additional information required by client.For
    example this operation returns logical flag to specify if the complete button can be enabled for the selected task
    in the perform dialog.
    """
    clientId: str = ''
    additionalData: KeyValueMap = None
    taskJSONStrings: StringMap = None


@dataclass
class WorkflowTaskViewModelResponse(TcBaseObj):
    """
    response
    
    :var output: response.
    :var serviceData: Service data.
    """
    output: List[WorkflowTaskViewModelOutput] = ()
    serviceData: ServiceData = None


"""
KeyValueMap.
"""
KeyValueMap = Dict[str, List[str]]


"""
String Map.
"""
StringMap = Dict[str, str]
