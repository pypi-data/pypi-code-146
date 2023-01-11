from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, Fnd0EditContext
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReferencerEditContextsOutput(TcBaseObj):
    """
    This structure contains an input object and its referencing edit contexts.
    
    :var inputObject: The input WorkspaceObject.
    :var editContexts: The list of edit contexts referencing inputObject
    """
    inputObject: WorkspaceObject = None
    editContexts: List[Fnd0EditContext] = ()


@dataclass
class ReferencerEditContextsResponse(TcBaseObj):
    """
    This structure contains the input objects and the corresponding edit contexts that reference the input objects. Any
    partial errors that occur during the operation are returned in serviceData.
    
    :var serviceData: Contains any partial errors that occur during the operation.
    :var refnEditContextOutputs: A list of ReferencerEditContextsOutput.
    """
    serviceData: ServiceData = None
    refnEditContextOutputs: List[ReferencerEditContextsOutput] = ()
