from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import User, TC_Project
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProjectInfo(TcBaseObj):
    """
    This structure holds the TC_Project and a flag indicating the user's membership type.
    
    :var project: The TC_Project object.
    :var isUserPrivileged: Flag indicating if the given  user is a privleged  member.
    """
    project: TC_Project = None
    isUserPrivileged: bool = False


@dataclass
class UserProjectsInfo(TcBaseObj):
    """
    This structure holds the projects for one of the given users.
    
    :var user: The User object of Teamcenter.
    :var activeProjectsOnly: Flag to indicate the status of projects  returned True indicates only active projects are
    returned. False indicates both active and inactive projects are returned.
    :var privilegedProjectsOnly: Flag to indicate if returned projects  are privleged or not.True indicates projects
    are privileged, false indicates all projects where the user is a member of regardless of privilege in the projects.
    :var programsOnly: Flag Indicating if user wants to get program only pojects of the user, false indicates returning
    all projects where regardless of status program only  value of TC_Project.
    :var clientId: An id associated with a client.
    :var projectsInfo: A list of ProjectInfo structure.
    """
    user: User = None
    activeProjectsOnly: bool = False
    privilegedProjectsOnly: bool = False
    programsOnly: bool = False
    clientId: str = ''
    projectsInfo: List[ProjectInfo] = ()


@dataclass
class UserProjectsInfoInput(TcBaseObj):
    """
    This structure holds the User object and criteria to find the user projects.
    
    :var user: The User object of Teamcenter.
    :var activeProjectsOnly: Flag Indicating if user wants to get active projects or 
    not.True indicates return only active projects of the user, false indicates return both active and inactive
    projects of the user.
    :var privilegedProjectsOnly: Flag Indicating if user wants to get privleged projects  
    or not.True indicates return privileged projects of the user, false indicates return all projects where the user is
    a member of regardless of status.
    :var programsOnly: Flag Indicating if user wants to get program only projects of the user, false indicates return
    all projects regardless of status program only.
    :var clientId: An id associated with a client.
    """
    user: User = None
    activeProjectsOnly: bool = False
    privilegedProjectsOnly: bool = False
    programsOnly: bool = False
    clientId: str = ''


@dataclass
class UserProjectsInfoResponse(TcBaseObj):
    """
    This structure holds the projects for all the given users.
    
    :var userProjectInfos: List of UserProjectsInfo structures one for each given user..
    :var serviceData: A  standard ServiceData.
    """
    userProjectInfos: List[UserProjectsInfo] = ()
    serviceData: ServiceData = None
