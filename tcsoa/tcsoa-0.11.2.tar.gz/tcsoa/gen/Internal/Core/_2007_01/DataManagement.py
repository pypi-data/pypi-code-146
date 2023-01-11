from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Role
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAttributeValuesInputData(TcBaseObj):
    """
    The data structure contains class name and attribute name for 'getAttributeValue' operation.
    
    :var className: Name of class containing the attribute
    :var attributeName: Internal name of the attribute
    """
    className: str = ''
    attributeName: str = ''


@dataclass
class GetAttributeValuesOutputData(TcBaseObj):
    """
    The data structure contains class attribute names and values.
    
    :var classAttribute: Class name and attribute names
    :var values: List of string attribute values
    """
    classAttribute: GetAttributeValuesInputData = None
    values: List[str] = ()


@dataclass
class GetAttributeValuesResponse(TcBaseObj):
    """
    This data structure contains attribute values for all  instances of a class.
    
    :var output: List of class name and attribute values
    :var serviceData: serviceData
    """
    output: List[GetAttributeValuesOutputData] = ()
    serviceData: ServiceData = None


@dataclass
class GetOrganizationInformationInputData(TcBaseObj):
    """
    This structure holds the user options to retrieve the organization hierarchy.
    
    :var groupName: The name of a group. Not supported.
    :var onlyFirstLevelSubGroups: It is not supported and should not be set. All subgroups are returned.
    :var includeRoleInGroupInfo: The option to include roles in the returned group information if it is true, otherwise
    no roles of the  groups are included.
    :var includeUsersInGroupRoleInfo: The option to include users with each role belonging to a group.
    """
    groupName: str = ''
    onlyFirstLevelSubGroups: bool = False
    includeRoleInGroupInfo: bool = False
    includeUsersInGroupRoleInfo: bool = False


@dataclass
class GetOrganizationInformationResponse(TcBaseObj):
    """
    This structure holds the group hierarchical information like the parent of a group and its child groups as well as
    roles added to a group and group members if they are included.
    
    :var hierDataMap: The lookup map to find child groups for a parent group.
    :var rootLevelGroups: List of top level groups in the organization.
    :var serviceData: Object with all groups in its plain object list and possible errors in retrieving all groups,
    roles and group members.
    """
    hierDataMap: GroupHierarchyDataMap = None
    rootLevelGroups: List[GroupHierarchyData] = ()
    serviceData: ServiceData = None


@dataclass
class GroupHierarchyData(TcBaseObj):
    """
    This structure holds the group hierarchical information like the parent of a group and its child groups as well as
    roles added to a group and group members if they are included.
    
    :var group: The target group
    :var subGroups: The child groups of the target group
    :var parent: The parent group of the target group
    :var roleUsers: The  list of RoleUsers objects. Each RoleUsers object hold a role added to the target  group and
    users with the role under the target group
    """
    group: Group = None
    subGroups: List[Group] = ()
    parent: Group = None
    roleUsers: List[RoleUsers] = ()


@dataclass
class RoleUsers(TcBaseObj):
    """
    This structure contains infomariton for a role added to a group and list of users with the role under the group.
    
    :var role: The role added to a group
    :var users: The users with the role under the group
    """
    role: Role = None
    users: List[User] = ()


"""
Map of Group to 'GroupHierarchyData' '(Group, GroupHierarchyData').
"""
GroupHierarchyDataMap = Dict[Group, GroupHierarchyData]
