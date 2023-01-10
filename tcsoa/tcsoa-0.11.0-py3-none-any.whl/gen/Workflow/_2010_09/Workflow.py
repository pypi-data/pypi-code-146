from __future__ import annotations

from tcsoa.gen.BusinessObjects import EPMJob, EPMTaskTemplate
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyTemplateInput(TcBaseObj):
    """
    New versions of the workflow templates that needs to be applied including the corresponding client ids.
    
    :var clientId: client id
    :var processTemplate: Process template to be applied
    """
    clientId: str = ''
    processTemplate: EPMTaskTemplate = None


@dataclass
class ApplyTemplateOutput(TcBaseObj):
    """
    Results from applying a template to its corresponding active processes.
    
    :var clientId: client id
    :var updatedProcesses: Active processes that were updated successfully
    :var failedProcesses: Active processes that could not be updated
    """
    clientId: str = ''
    updatedProcesses: List[EPMJob] = ()
    failedProcesses: List[EPMJob] = ()


@dataclass
class ApplyTemplateResponse(TcBaseObj):
    """
    Information about active processes that were updated with template changes
    
    :var applyTemplateOutput: List of processes that were updated and list of processes that failed.
    :var serviceData: Service Data
    """
    applyTemplateOutput: List[ApplyTemplateOutput] = ()
    serviceData: ServiceData = None
