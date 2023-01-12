from __future__ import annotations

from tcsoa.gen.Internal.Core._2007_06.ProjectLevelSecurity import Filter
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProjectSmartFolderHierarchyOutput2(TcBaseObj):
    """
    This structure holds smart folder hierarchy information and a project ID of one TC_Project object.
    
    :var projectID: The unique identifier of the TC_Project object.
    :var projectSmartFolderHierarchy: A list  of SmartFolderOutputInfo2 objects.
    """
    projectID: str = ''
    projectSmartFolderHierarchy: List[SmartFolderOutputInfo2] = ()


@dataclass
class ProjectSmartFolderHierarchyOutputResponse2(TcBaseObj):
    """
    This structure contains a list of ProjectSmartFolderHierarchyOutput2 structures and a standard ServiceData
    element.If the project id does not exist in the system then error code 101007: the project ID is invalid is
    returned.
    
    :var output: List of ProjectSmartFolderHierarchyOutput2 structures.
    :var serviceData: A  standard ServiceData.
    """
    output: List[ProjectSmartFolderHierarchyOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class SmartFolderOutputInfo2(TcBaseObj):
    """
    This structure holds smart folder hierarchy information.
    
    :var parentName: The name of the parent smart folder node of the current hierarchy.
    :var parentInternalName: The internal name of the parent smart folder node of the current hierarchy.
    :var name: The name of the current smart folder node.
    :var internalName: The internal name of the current smart folder node.
    :var filters: A list of filiters for this smart folder hierarchy.
    :var isLeaf: The flag indicating if this is the last child of the hierarchy.
    """
    parentName: str = ''
    parentInternalName: str = ''
    name: str = ''
    internalName: str = ''
    filters: List[Filter] = ()
    isLeaf: bool = False
