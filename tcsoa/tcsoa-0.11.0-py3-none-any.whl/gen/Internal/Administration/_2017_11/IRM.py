from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AccessorInformation(TcBaseObj):
    """
    Information about the Accessor.
    
    :var accessorType: The type of the Accessor.
    :var accessorName: The name of the Accessor.
    :var accessorObject: Accessor Objects for which Accessor Information is requested. Accessor object can be instance
    of POM_accessor, AM_named_tag, Group, Role, User, RoleInOwningGroup, RoleInProject, RoleInProjectsOfObject,
    RoleInSchedule.
    """
    accessorType: str = ''
    accessorName: str = ''
    accessorObject: BusinessObject = None


@dataclass
class AccessorsInfoResponse(TcBaseObj):
    """
    This structure holds a list of Accessor Information for a given input accessors.
    
    :var accessorInformations: List of AccessorInformations for each given accessor.
    :var serviceData: Object that holds the partial errors occurred while deriving the accessor information of any of
    the given business objects.
    """
    accessorInformations: List[AccessorInformation] = ()
    serviceData: ServiceData = None
