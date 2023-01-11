from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GroupMembershipInput2(TcBaseObj):
    """
    A structure containing input to retrieve group membership information.
    
    :var userId: The string specifies the user_id to search for within the organization. An example is: User wants to
    search for GroupMember objects which have a User with user_id equal to this input. Partial string supported. This
    is an optional input.
    :var userName: The string specifies the user_name to search for within the organization. An example is: User wants
    to search for GroupMember objects which have a User with user_name equal to this input. Partial string supported.
    This is an optional input.
    :var groupName: The string specifies the Group name to search within the organization. An example is: User wants to
    search for GroupMember objects which have a Group with name equal to this input. Partial string supported. This is
    an optional input.
    :var roleName: The string specifies the Role name to search within the organization. An example is: User wants to
    search for GroupMember objects which have a Role with role_name equal to this input. Partial string supported. This
    is an optional input.
    :var searchForSubGroup: A flag input to specify whether to search for sub-group of given group in groupName input.
    If the groupName is empty or contains  wild card( "*" ), then this input will be ignored. This is an optional input.
    :var startIndex: This input is used for pagination. User can specify the the start index of the next chunk of
    objects to return. An example of this input is: This operation finds 100 GroupMember objects. User want to get
    first 50 searched objects. So here the startIndex would be 0. For next chunk of searched objects this input would
    be 51.
    Note: Value for this input should be a positive integer. If the value is negative number then it is considered as 0.
    
    :var maxToReturn: This input is used for pagination. This input specifies the maximum number of found objects to
    return.
    Note: Value for this input should be a positive integer. If the value is 0 or negative number then this input will
    be ignored and all the found objects will be returned.
    
    :var maxToLoad: This input is used for pagination. This input specifies the maximum number of found objects to load.
    Note: Value for this input should be a positive integer. If the value is 0 or negative number then this input will
    be ignored and all the found objects will be loaded.
    """
    userId: str = ''
    userName: str = ''
    groupName: str = ''
    roleName: str = ''
    searchForSubGroup: bool = False
    startIndex: int = 0
    maxToReturn: int = 0
    maxToLoad: int = 0
