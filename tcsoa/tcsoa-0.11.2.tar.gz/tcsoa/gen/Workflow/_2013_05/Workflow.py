from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, EPMTaskTemplate
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetWorkflowTemplatesInputInfo(TcBaseObj):
    """
    Structure to define input for workflow Templates
    
    :var clientId: Client Id.
    :var includeUnderConstruction: If set to true, the operation will return Under construction templates for
    administrative users only.  Otherwise only available workflow templates are returned.
    :var getFiltered: If set to true, the operation will return assigned or filtered list of workflow templates based
    on Target Objects and Object Types.
    :var targetObjects: List of target objects to be used for getting the filtered list of workflow templates.
    :var objectTypes: List of target object types to be used for getting the filtered list of workflow templates. This
    argument is not required if targetObjects are specified.
    :var group: User group to get the filtered list of  workflow templates.
    """
    clientId: str = ''
    includeUnderConstruction: bool = False
    getFiltered: bool = False
    targetObjects: List[WorkspaceObject] = ()
    objectTypes: List[str] = ()
    group: str = ''


@dataclass
class GetWorkflowTemplatesOutput(TcBaseObj):
    """
    Structure to define output for workflow Templates
    
    :var clientId: Client Id.
    :var workflowTemplates: A list of output workflow Templates.
    """
    clientId: str = ''
    workflowTemplates: List[EPMTaskTemplate] = ()


@dataclass
class GetWorkflowTemplatesResponse(TcBaseObj):
    """
    Structure to define response for workflow Templates
    
    :var serviceData: ServiceData contains any partial errors.
    :var templatesOutput: Complete list of workflow Templates Output.
    """
    serviceData: ServiceData = None
    templatesOutput: List[GetWorkflowTemplatesOutput] = ()
