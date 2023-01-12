from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Role, GroupMember
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetUserGroupMembersInputData(TcBaseObj):
    """
    This structure holds the input data to retrieve the group member information of a given user.
    
    :var user: The given user object.
    :var includeInactive: The option flag to include inactive group memers in returned group members data.
    :var includeUser: The option flag to include User objects in returned group member data.
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    """
    user: User = None
    includeInactive: bool = False
    includeUser: bool = False
    clientId: str = ''


@dataclass
class GetUserGroupMembersOutput(TcBaseObj):
    """
    This structure holds all user group member data for a given user.
    
    :var clientId: Unmodified value from the GetUserGroupMembersInputData.clientId. This can be used by the caller to
    indentify this data structure with the source input data.
    :var memebrs: All user group member data for a specific user.
    """
    clientId: str = ''
    memebrs: List[UserGroupMemberData] = ()


@dataclass
class GetUserGroupMembersResponse(TcBaseObj):
    """
    A list of user group members outputs, one for each of the given User object.
    
    :var outputs: List of group member information, one for each User object.
    :var serviceData: The object which holds the partial errors that occurred during retrieving user group member data.
    """
    outputs: List[GetUserGroupMembersOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GroupMemberInput(TcBaseObj):
    """
    This structure holds a GroupMember object, whose properties need to be updated and a map of property names and
    their corresponding values.
    
    :var groupMember: The GroupMember business object whose propeties  need to be updated.
    :var groupMemberPropValuesMap: A map of  property names and desired value(string/string).
    """
    groupMember: GroupMember = None
    groupMemberPropValuesMap: GroupMemberPropValuesMap = None


@dataclass
class RoleUser(TcBaseObj):
    """
    This structure holds role, user, group member status, default role flag and group admin privilege for a group
    member.
    
    :var role: The Role of a group member.
    :var user: The User of a group member.
    :var isActive: True if the group member is active.
    :var isDefaultRole: True if the this Role is the default in the group member.
    :var isGroupAdmin: True if the group member has administrative privilege
    """
    role: Role = None
    user: User = None
    isActive: bool = False
    isDefaultRole: bool = False
    isGroupAdmin: bool = False


@dataclass
class UserGroupMemberData(TcBaseObj):
    """
    This structure holds the all group member data under a group for the given user.
    
    :var group: The group of the group members in the RoleUser list.
    :var roleUsers: The list of RoleUser objects which belong to the same group.
    """
    group: Group = None
    roleUsers: List[RoleUser] = ()


"""
A map of property names and desired values (string/string).
"""
GroupMemberPropValuesMap = Dict[str, List[str]]
