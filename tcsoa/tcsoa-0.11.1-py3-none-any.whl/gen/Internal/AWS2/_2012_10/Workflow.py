from __future__ import annotations

from tcsoa.gen.BusinessObjects import EPMTaskTemplate
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetTaskResultsResponse(TcBaseObj):
    """
    Response from GetTaskResults SOA
    
    :var output: Output of GetTaskResults method
    :var serviceData: Service data
    """
    output: List[TaskResultsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class TaskResultsOutput(TcBaseObj):
    """
    Output of GetTaskResults method
    
    :var taskTemplate: Task template object
    :var taskResults: Task results
    """
    taskTemplate: EPMTaskTemplate = None
    taskResults: List[str] = ()
