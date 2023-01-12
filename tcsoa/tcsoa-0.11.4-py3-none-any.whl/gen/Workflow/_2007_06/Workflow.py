from __future__ import annotations

from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class ReleaseStatusInput(TcBaseObj):
    """
    ReleaseStatus input
    
    :var operations: Operations to perform ( Currently only Append is supported )
    :var objects: Objects to modify
    """
    operations: List[ReleaseStatusOption] = ()
    objects: List[WorkspaceObject] = ()


@dataclass
class ReleaseStatusOption(TcBaseObj):
    """
    ReleaseStatus option
    
    :var newReleaseStatusTypeName: Name of release type to instantiate and assign
    :var operation: Operation to perform
    :var existingreleaseStatusTypeName: Name of old release type to delete or replace
    """
    newReleaseStatusTypeName: str = ''
    operation: releaseStatusOperation = None
    existingreleaseStatusTypeName: str = ''


@dataclass
class SetReleaseStatusResponse(TcBaseObj):
    """
    service data
    
    :var serviceData: serviceData
    """
    serviceData: ServiceData = None


class releaseStatusOperation(Enum):
    """
    releaseStatusOperation
    """
    Append = 'Append'
    Delete = 'Delete'
    Rename = 'Rename'
    Replace = 'Replace'
