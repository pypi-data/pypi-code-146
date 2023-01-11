from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindObjectsCriteria(TcBaseObj):
    """
    Criteria to find objects
    
    :var className: Class name to search by.
    :var searchAttributes: Attributes and values to search by.
    """
    className: str = ''
    searchAttributes: FindObjectsAttrAndValueMap = None


@dataclass
class FindObjectsInput2(TcBaseObj):
    """
    Input structure for FindObjectsByClassAndAttributes2
    
    :var clientId: Client unque id.
    :var startIndex: The start index
    :var maxLoad: Maximum objects to load.
    :var maxToReturn: Maximum uids to return.
    :var searchCriteria: Search criteria
    :var searchMode: Type of search.
    :var uids: A list of object uids to inflate.
    :var attributes: A set of attributes to inflate.
    """
    clientId: str = ''
    startIndex: int = 0
    maxLoad: int = 0
    maxToReturn: int = 0
    searchCriteria: List[FindObjectsCriteria] = ()
    searchMode: SearchMode = None
    uids: List[BusinessObject] = ()
    attributes: List[str] = ()


@dataclass
class FindObjectsResponse2(TcBaseObj):
    """
    Returns a structure of data.
    
    :var result: The list of business objects
    :var totalLoaded: Total number of objects loaded.
    :var totalFound: Total number of objects found.
    :var thumbnailMap: A map containing the thumbnail file tickets.
    :var serviceData: The service data.
    """
    result: List[BusinessObject] = ()
    totalLoaded: int = 0
    totalFound: int = 0
    thumbnailMap: ThumbnailMap = None
    serviceData: ServiceData = None


@dataclass
class FindUsersTasksResponse(TcBaseObj):
    """
    A structure containing the user's tasks.
    
    :var tasksToPerform: A list of tasks to perform.
    :var tasksToTrack: A list of tasks to track.
    :var serviceData: Service data.
    """
    tasksToPerform: List[BusinessObject] = ()
    tasksToTrack: List[BusinessObject] = ()
    serviceData: ServiceData = None


class SearchMode(Enum):
    """
    Type of search to perform.
    """
    GeneralInListQuery = 'GeneralInListQuery'
    GeneralQuery = 'GeneralQuery'
    SavedQuery = 'SavedQuery'


"""
Attribute and value map
"""
FindObjectsAttrAndValueMap = Dict[str, str]


"""
Used to keep track of a group of business objects and thumbnail file tickets.
"""
ThumbnailMap = Dict[BusinessObject, str]
