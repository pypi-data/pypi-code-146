from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, Role
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RoleGroupStructure(TcBaseObj):
    """
    A structure of Role objects and the associated Group object.
    
    :var roles: A list of Role objects to be removed.
    :var grp: The Group object from which Role objects are to be removed.
    """
    roles: List[Role] = ()
    grp: Group = None


@dataclass
class RoleStructure(TcBaseObj):
    """
    Properties for the new Role to be created and added to the Group.
    
    :var roleName: Name of the Role to be created.
    :var roleDescription: The Role description.
    """
    roleName: str = ''
    roleDescription: str = ''


@dataclass
class AddRolesToGroupStructure(TcBaseObj):
    """
    Roles to be added to a Group object.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var rolesToAdd: A list of Role objects to be added to the Group.
    :var rolesToCreateAndAdd: A list of Role properties. A new Role will be created for each RoleStructure in the list
    and added to the Group.
    :var grp: Group for the roles to be added to.
    """
    clientId: str = ''
    rolesToAdd: List[Role] = ()
    rolesToCreateAndAdd: List[RoleStructure] = ()
    grp: Group = None
