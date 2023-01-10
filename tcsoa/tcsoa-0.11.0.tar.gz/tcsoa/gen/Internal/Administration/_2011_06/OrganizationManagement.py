from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, Role, GroupMember
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetGroupsForRoleInput(TcBaseObj):
    """
    This structure hold a Role business object to find the matching groups and a boolean flag. Each matching groups
    should have this role in its role list.
    
    :var role: The given Role to find matching groups.
    :var includeOrgTree: Flag to indicate if an optional matched group tree structure would be returned. Set it to true
    if  the group tree structure should be sent back, false otherwise.
    """
    role: Role = None
    includeOrgTree: bool = False


@dataclass
class GetOrganizationGroupOutput(TcBaseObj):
    """
    Organization Group Ouput.
    
    :var groups: List of matched groups.
    :var orgTree: Tree structure of the matched groups and their parent groups. It could be null if optional input flag
    is set to not return this tree.
    """
    groups: List[Group] = ()
    orgTree: OrganizationTree = None


@dataclass
class GetOrganizationGroupResponse(TcBaseObj):
    """
    A list of GetOrganizationGroupOutput objects for each of the given Role object.
    
    :var outputs: List of GeyOrganizationGroupOutput objects, one for each GetGroupsForRoleInput object.
    :var serviceData: Object with all matched groups in plain object list and possible errors in finding matched groups.
    """
    outputs: List[GetOrganizationGroupOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GroupStructure(TcBaseObj):
    """
    This structure holds the group hierarchical information like the parent of a group and its child groups.
    
    :var group: A Group object which has the given role directly or through its descendent groups.
    :var parent: The parent group of the Group object.
    :var subgroups: Child groups of the Group object which contain the role directly or through their descendent groups.
    :var groupRoles: A List of roles for Group.
    """
    group: Group = None
    parent: Group = None
    subgroups: List[Group] = ()
    groupRoles: List[RoleUsers] = ()


@dataclass
class OrganizationTree(TcBaseObj):
    """
    This structure holds the list of top level groups and corresponding subgroups.
    
    :var rootLevelGroups: A list of  top level Group objects which have  the given role by itself or by their
    descendent groups.
    :var groupStructureMap: A lookup map to find corresponding GroupStructure for a given group. The key for the map 
    is BusinessObjectRef<Teamcenter::Group> and value is GroupStructure.
    """
    rootLevelGroups: List[GroupStructure] = ()
    groupStructureMap: GroupStructureMap = None


@dataclass
class RoleUsers(TcBaseObj):
    """
    This structure holds role and a list of  associated group members .
    
    :var role: The Role of a group member.
    :var members: List of group members for given role.
    """
    role: Role = None
    members: List[GroupMember] = ()


"""
A lookup map to find corresponding GroupStructure for a given group. The key for the map  is BusinessObjectRef<Teamcenter::Group> and value is GroupStructure.
"""
GroupStructureMap = Dict[Group, GroupStructure]
