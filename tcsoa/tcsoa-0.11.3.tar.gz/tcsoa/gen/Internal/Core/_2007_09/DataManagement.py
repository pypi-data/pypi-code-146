from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class WhereUsedOutputOccGroup(TcBaseObj):
    """
    This structure contains information for Where Used Output (unpublished for the case of Occurrence Group).
    
    :var inputObject: Input WorkspaceObject object reference for mapping to the output
    :var info: List of 'WhereUsedParentInfoOccGroup' structures
    """
    inputObject: WorkspaceObject = None
    info: List[WhereUsedParentInfoOccGroup] = ()


@dataclass
class WhereUsedParentInfoOccGroup(TcBaseObj):
    """
    This structure contains Where Used Parent Information (unpublished for the case of Occurrence Group).
    
    :var parentOccGroup: parentOccGroup
    :var level: The level at which the parent ItemRevision was found
    """
    parentOccGroup: WorkspaceObject = None
    level: int = 0


@dataclass
class WhereUsedResponseOccGroup(TcBaseObj):
    """
    Where Used Response (unpublished for the case of Occurrence Group)
    
    :var output: List of WhereUsedOutputOccGroup structures
    :var serviceData: Standard ServiceData member
    """
    output: List[WhereUsedOutputOccGroup] = ()
    serviceData: ServiceData = None
