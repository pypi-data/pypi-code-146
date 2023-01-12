from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetFilteredProjectObjectsOutput(TcBaseObj):
    """
    The list of business objects, which are filtered based on the  given filter criteria for a given  project.
    
    :var projectID: The project ID.
    :var objectsInProject: The list of UIDs of business objects which are filtered based on the   given filter criteria.
    """
    projectID: str = ''
    objectsInProject: List[str] = ()


@dataclass
class GetFilteredProjectObjectsResponse(TcBaseObj):
    """
    The list of business objects, which are filtered based on the  given filter criteria for a given  project.
    
    :var filteredObjectsInProjects: List of filtered busisness objects for each of the requested projects.
    :var serviceData: Partial errors, if any.
    """
    filteredObjectsInProjects: List[GetFilteredProjectObjectsOutput] = ()
    serviceData: ServiceData = None
