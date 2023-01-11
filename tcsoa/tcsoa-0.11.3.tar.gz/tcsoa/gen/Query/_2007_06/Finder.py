from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindWorkspaceObjectsOutput(TcBaseObj):
    """
    FindWorkspaceObjectsOutput
    
    :var findSetIndex: The index of FindSet that generated the output.
    :var foundObjects: The WorkspaceObject business objects matching the search criteria.
    """
    findSetIndex: int = 0
    foundObjects: List[WorkspaceObject] = ()


@dataclass
class FindWorkspaceObjectsResponse(TcBaseObj):
    """
    FindWorkspaceObjectsResponse
    
    :var outputList: A list of found workspace objects.
    :var serviceData: The service data.
    """
    outputList: List[FindWorkspaceObjectsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class WSOFindCriteria(TcBaseObj):
    """
    WSOFindCriteria
    
    :var objectType: If set, must be set to the corresponding class name . If not set, this criteria will be ignored by
    the search.
    :var objectName: Name of object 
    Can contain wild card characters. 
    The percent sign and underscore are the only valid wild card characters, 
    where: 
    % Represents any set of characters in the substring. 
    _ (Underscore) Represents any single character in the substring.
    :var scope: Scope of search,  WSO_scope_All = entire database,  WSO_search_Approved = searches for objects that
    have at least  one status of approval.
    :var owner: The owning User to limit found objects for. A null value will expand the search to all users.
    :var group: The owning Group to limit found objects for. A null value will expand the search to all groups.
    :var createdBefore: The maximum creation date to limit found objects. A null value will not limit the results.
    :var modifiedBefore: The maximum last modified date to limit found objects. A null value will not limit the results.
    :var releasedBefore: The maximum released date to limit found objects. A null value will not limit the results.
    :var createdAfter: The minimum creation date to limit found objects. A null value will not limit the results.
    :var modifiedAfter: The minimum last modified date to limit found objects. A null value will not limit the results.
    :var releasedAfter: The minimum released date to limit found objects. A null value will not limit the results.
    """
    objectType: str = ''
    objectName: str = ''
    scope: WSOscopeType = None
    owner: BusinessObject = None
    group: BusinessObject = None
    createdBefore: datetime = None
    modifiedBefore: datetime = None
    releasedBefore: datetime = None
    createdAfter: datetime = None
    modifiedAfter: datetime = None
    releasedAfter: datetime = None


@dataclass
class WSOFindSet(TcBaseObj):
    """
    WSOFindSet
    
    :var criterias: A list of FindCriteria to search with.
    """
    criterias: List[WSOFindCriteria] = ()


class WSOscopeType(Enum):
    """
    Scope of search:  WSO_scope_All = entire database,  WSO_scope_Approved = searches for objects that have at least
    one approval status.oval status.
    """
    WSO_scope_All = 'WSO_scope_All'
    WSO_scope_Approved = 'WSO_scope_Approved'
