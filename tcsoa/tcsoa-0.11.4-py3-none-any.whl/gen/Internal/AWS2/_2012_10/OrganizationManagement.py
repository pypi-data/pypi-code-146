from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, GroupMember, Person, User, Role
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GroupMembershipInput(TcBaseObj):
    """
    A structure containing input to retrieve group membership information.
    
    :var searchString: The string to search for within the group membership.
    :var startIndex: The index from which to start the search.
    :var maxToReturn: The maximum number of objects to return.
    :var maxToLoad: The maximum number of objects to load.
    """
    searchString: str = ''
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0


@dataclass
class GroupMembershipOutput(TcBaseObj):
    """
    Structure that contains a list of groupMember objects with same group and role
    
    :var group: Group object
    :var role: Role object
    :var groupMembers: Group member objects
    """
    group: Group = None
    role: Role = None
    groupMembers: List[GroupMember] = ()


@dataclass
class GroupMembershipResponse(TcBaseObj):
    """
    A service response structure containing group membership information.
    
    :var groupMembers: The list which contains a list of GroupMember business objects with same group and role, the
    outer list is sorted first by group name, then by role name, the inner list is sorted by user name
    :var userToPersonMap: The map that contains a mapping from a User business object to a Person business object.
    :var totalFound: The total number of GroupMember business objects found.
    :var totalLoaded: The total number of GroupMember business objects loaded.
    :var serviceData: The service data object.
    """
    groupMembers: List[GroupMembershipOutput] = ()
    userToPersonMap: UserToPersonMap = None
    totalFound: int = 0
    totalLoaded: int = 0
    serviceData: ServiceData = None


"""
A map that contains a mapping from a User business object to a Person business object.
"""
UserToPersonMap = Dict[User, Person]
