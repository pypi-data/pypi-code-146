from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, Role
from typing import Dict, List
from tcsoa.gen.Internal.Administration._2011_06.OrganizationManagement import RoleUsers
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOrganizationUserMembersResponse(TcBaseObj):
    """
    A list of GroupElement objects containing group membership information in the groups.
    
    :var groupElementMap: Map of Group objects to GroupElement objects.
    :var serviceData: Object with all found GroupMember objects, corresponding Group and Role objects in plain object
    list and possible errors in finding matched GroupMember objects.
    """
    groupElementMap: GroupElementMap = None
    serviceData: ServiceData = None


@dataclass
class GroupElement(TcBaseObj):
    """
    This structure holds the group hierarchical information like the parent of a group and its child groups.
    
    :var group: The Group object of the GroupMember objects.
    :var parent: The parent group of the Group object.
    :var subGroups: The child groups of the Group object which contain matched GroupMember objects.
    :var roles: List of Role objects of the Group object containing matched GroupMember objects.
    :var members: List of GroupMember  objects for a role under the Group object.
    """
    group: Group = None
    parent: Group = None
    subGroups: List[Group] = ()
    roles: List[Role] = ()
    members: List[RoleUsers] = ()


@dataclass
class OrganizationMembersInput(TcBaseObj):
    """
    This structure hold search criteria to find the matching group members.
    
    :var userID: The user_id of User objects matching with GroupMember objects to be found. Teamcenter search  wildcard
     characters are permitted and is case insensitive.
    :var userName: The user_name of User objects matching with GroupMember objects to be found. Teamcenter search 
    wildcard  characters are permitted and is case insensitive
    :var groupName: The  name of Group objects matching with GroupMember objects to be found. Teamcenter search
    wildcard  characters are permitted and is case insensitive.
    :var roleName: The role_name of Role objects matching with GroupMember objects to be found. Teamcenter search
    wildcard  characters are permitted and is case insensitive.
    :var includeInactive: If true, inactive GroupMember objects are included.
    :var includeSubGroups: If true, GroupMember objects from subgroups of matching groups are included.
    """
    userID: str = ''
    userName: str = ''
    groupName: str = ''
    roleName: str = ''
    includeInactive: bool = False
    includeSubGroups: bool = False


"""
This map holds mapping from a Group object to a GroupElement structure.
"""
GroupElementMap = Dict[Group, GroupElement]
