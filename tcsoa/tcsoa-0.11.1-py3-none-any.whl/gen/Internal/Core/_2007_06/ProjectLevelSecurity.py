from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import WorkspaceObject, TC_Project
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Filter(TcBaseObj):
    """
    This is a list of strings to support both single valued and multi valued properties of any type. The calling client
    is responsible for converting the different property types (like integer, double, date etc...) to a string using
    the appropriate toXXXString functions in the Services client framework's Property class.
    
    :var sourceTypeName: The name of the WorkspaceObject and or any of its subtype  on which filter is to be performed.
    :var name: The name of the attribute on a given type.
    :var value: The value of the attribute.
    """
    sourceTypeName: str = ''
    name: str = ''
    value: str = ''


@dataclass
class GetFilteredProjectDataInputData(TcBaseObj):
    """
    Object that holds project id and a list  of filters.
    
    :var projectID: The project id of the  TC_Project object.
    :var filters: A list of Filter critera objects.
    """
    projectID: str = ''
    filters: List[Filter] = ()


@dataclass
class GetFilteredProjectDataOutput(TcBaseObj):
    """
    Object that holds project ID and filtered data.
    
    :var projectID: The project id of  the TC_Project object.
    :var filteredData: A list of filtered project  data.
    """
    projectID: str = ''
    filteredData: List[WorkspaceObject] = ()


@dataclass
class GetFilteredProjectDataResponse(TcBaseObj):
    """
    Object that holds vector of GetFilteredProjectDataOutput and standard ServiceData.
    
    :var output: A list of  GeFilteredProjectDataOutput objects one for each project.
    :var serviceData: A standard ServiceData.
    """
    output: List[GetFilteredProjectDataOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ProjectSmartFolderHierarchyOutput(TcBaseObj):
    """
    This structure holds the project ID of the project and a list of SmartFolderOutputInfo structures.
    
    :var projectID: The project id of TC_Project object.
    :var projectSmartFolderHierarchy: A list containing information about smart folder hierarchies associated with the
    project ids.
    """
    projectID: str = ''
    projectSmartFolderHierarchy: List[SmartFolderOutputInfo] = ()


@dataclass
class ProjectSmartFolderHierarchyOutputResponse(TcBaseObj):
    """
    This structure contains the list of ProjectSmartFolderHierarchyOutput objects and standard ServiceData.
    
    :var output: A list of ProjectSmartFolderHierarchyOutput objects which contains  project IDs and Smart folder
    hierarchy information.
    :var serviceData: Holds the error list corresponding to the project ids for which smart folder hierarchy retrieval
    failed.
    """
    output: List[ProjectSmartFolderHierarchyOutput] = ()
    serviceData: ServiceData = None


@dataclass
class SmartFolderOutputInfo(TcBaseObj):
    """
    This structure holds the information retrieved corresponding to one top level smart folder.
    
    :var parentName: The name of the parent node of the current smart folder hierarchy .
    :var name: The name of the current node.
    :var filters: A list of filters for this hierarchy.
    :var isLeaf: The flag indicating if this is the last child of the hierarchy.
    """
    parentName: str = ''
    name: str = ''
    filters: List[Filter] = ()
    isLeaf: bool = False


@dataclass
class TopLevelHierarchyOutputResponse(TcBaseObj):
    """
    This structure contains the top-level hierarchy as a flat list in vector format but in a depth first manner. Each
    SmartFolderOutputInfo in the vector would correspond to a node in the hierarchy and would have a parent smart
    folder name under which it belongs.
    
    :var topHierarchy: List of SmartFolderOutputInfo structures.
    :var userProjects: List of UserProjectsOutput structures.
    :var serviceData: A  standard ServiceData which contains unknown errors.
    """
    topHierarchy: List[SmartFolderOutputInfo] = ()
    userProjects: List[UserProjectsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class UserProjectsOutput(TcBaseObj):
    """
    This structure would contain the current logged in users project along with the filters defined on those projects.
    
    :var project: The TC_Project for the current user.
    :var filters: A list of filters for the project.
    """
    project: TC_Project = None
    filters: List[Filter] = ()
