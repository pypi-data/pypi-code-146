from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Group, User, Role, TC_Project
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class UserGroupRoleInfo(TcBaseObj):
    """
    The UserGroupRoleInfo structure contains the user, the group, and the role. The group and the role are optional.
    
    :var tcUser: The User object.
    :var tcGroup: The Group object.
    :var tcRole: The Role object.
    """
    tcUser: User = None
    tcGroup: Group = None
    tcRole: Role = None


@dataclass
class UserProjects(TcBaseObj):
    """
    The structure which holds the TC_Project objects for the associated UserGroupRoleInfo structure
    
    :var userGroupRole: The UserGroupRoleInfo structure.
    :var projects: The TC_Project objects that's associated with the UserGroupRoleInfo.
    """
    userGroupRole: UserGroupRoleInfo = None
    projects: List[TC_Project] = ()


@dataclass
class UserProjectsResponse(TcBaseObj):
    """
    The structure which holds the ServiceData and all the TC_Project objects that are associated with the given
    UserGroupRoleInfo
    
    :var userProjectList: A list of UserProjects structure.
    :var serviceData: The ServiceData.
    """
    userProjectList: List[UserProjects] = ()
    serviceData: ServiceData = None


@dataclass
class ChangeOwningProgramInput2(TcBaseObj):
    """
    Contains data used for changing the owning program for the  given set of objects.
    
    :var owningProgram: The project (TC_Project) to set as the Owning Program of the target objects.
    :var inputObjects: A list of WorkspaceObject for which the Owning Program is to be changed.
    """
    owningProgram: TC_Project = None
    inputObjects: List[BusinessObject] = ()
