from __future__ import annotations

from tcsoa.gen.Administration._2015_07.UserManagement import CreateOrUpdateUserInputs
from tcsoa.gen.BusinessObjects import User, Group, Role
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExistingUserDetailsForGroupMember(TcBaseObj):
    """
    A structure of User object and its attributes.
    
    :var user: Existing User to be added. This User will be added to the Group with the specified Role.
    :var userAttributes: List of userAttributes associated with each User.
    """
    user: User = None
    userAttributes: UserAttributesStructure = None


@dataclass
class NewUserDetailsForGroupMember(TcBaseObj):
    """
    A structure of new User to be created with its attributes.
    
    :var user: A list of User properties . Using these properties a new User will be created and added to the Group
    with specified Role.
    :var userAttributes: Additional GroupMember proeprties for the new User.
    """
    user: CreateOrUpdateUserInputs = None
    userAttributes: UserAttributesStructure = None


@dataclass
class UserAttributesStructure(TcBaseObj):
    """
    A structure of User attributes.
    
    :var isGroupAdmin: If true, user will be the group administrator; otherwise, user will not be the group
    administrator.
    :var status: If true, user will be active GroupMember; otherwise, user will not be active GroupMember.
    :var isDefaultRole: If true, the given role will be the default role for the user; otherwise the given role will
    not be the default role for the user.
    """
    isGroupAdmin: bool = False
    status: bool = False
    isDefaultRole: bool = False


@dataclass
class UserManagementResponse(TcBaseObj):
    """
    This structure holds a structure of User and associated Role and Group objects along with ServiceData.
    
    :var userRoleGrpStructs: A list of structures of User and associated Role and Group objects.
    :var serviceData: The Service Data with the partial error information.
    """
    userRoleGrpStructs: List[UserRoleGroupStructure] = ()
    serviceData: ServiceData = None


@dataclass
class UserRoleGroupStructure(TcBaseObj):
    """
    A structure of User and associated Role and Group objects.
    
    :var users: A list of User objects to be removed from given Group and Role.
    :var grp: A Group object from which User is to be removed.
    :var role: A Role object from which User is to be removed.
    """
    users: List[User] = ()
    grp: Group = None
    role: Role = None


@dataclass
class AddUsersAsGroupMembersStructure(TcBaseObj):
    """
    A structure of User object and the associated Role and Group objects.
    
    :var clientId: Identifier that helps the client to track the object(s) created and modified, required; should be
    unique for the input set.
    :var usersToAdd: A list of existing users to be added to the Group with specified Role.
    :var usersToCreateAndAdd:  A list of users to be created and added to the Group with specified Role.
    :var grp: Group for the group members.
    :var role: The Role for the group members.
    """
    clientId: str = ''
    usersToAdd: List[ExistingUserDetailsForGroupMember] = ()
    usersToCreateAndAdd: List[NewUserDetailsForGroupMember] = ()
    grp: Group = None
    role: Role = None
