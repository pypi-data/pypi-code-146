from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, ImanAliasList
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class UserGroupAliasResponse(TcBaseObj):
    """
    Lists of User, Group, and ImanAliasList objects from the operation.
    
    :var users: A list of all Teamcenter User objects
    :var groups: A list of all Teamcenter Group objects
    :var aliasLists: The list of all ImanAliasList objects
    :var serviceData: Error encountered while processing post event on element in the set is reported as partial errors
    in serviceData and processing continues for the remaining elements in the input set.
    """
    users: List[User] = ()
    groups: List[Group] = ()
    aliasLists: List[ImanAliasList] = ()
    serviceData: ServiceData = None
