from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, TC_Project
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ModifyProjectsInfo(TcBaseObj):
    """
    This structure holds the TC_Project object and the information required to modify the project.
    
    :var sourceProject: The TC_Project object  to be modified.
    :var projectInfo: A ProjectInformation structure.
    :var clientId: Unique identifier for the client to track any errors.
    """
    sourceProject: TC_Project = None
    projectInfo: ProjectInformation = None
    clientId: str = ''


@dataclass
class ProjectClientId(TcBaseObj):
    """
    This structure holds TC_Project object and corresponding client id.
    
    :var tcProject: The TC_Project object whose team members need to be retrieved.
    :var clientId: Unique identifier used by the client to track any errors.
    """
    tcProject: TC_Project = None
    clientId: str = ''


@dataclass
class ProjectInformation(TcBaseObj):
    """
    Structure that holds the information required to create the destination project.
    
    :var projectId: The project ID of  the project  to be created.
    :var projectName: The name of the project to be created.
    :var projectDescription: The description of the project to be created.
    :var useProgramContext: The value of useProgramContext attribute on TC_Project.
    :var active: The value of active attribute on TC_Project.
    :var visible: The value of visible attribute on TC_Project.
    :var teamMembers: A list of TeamMemberInfo structures.
    :var clientId: Unique identifier used by the client to track any errors.
    """
    projectId: str = ''
    projectName: str = ''
    projectDescription: str = ''
    useProgramContext: bool = False
    active: bool = False
    visible: bool = False
    teamMembers: List[TeamMemberInfo] = ()
    clientId: str = ''


@dataclass
class ProjectOpsOutput(TcBaseObj):
    """
    Structure that holds the TC_Project object.
    
    :var project: The created TC_Project object.
    :var clientId: Unique identifier used by the client to track any errors.
    """
    project: TC_Project = None
    clientId: str = ''


@dataclass
class ProjectOpsResponse(TcBaseObj):
    """
    Response from the project create, modify operations.
    
    :var projectOpsOutputs: Vector of ProjectOpsOuput objects.
    :var serviceData: Service data with the partial error information
    """
    projectOpsOutputs: List[ProjectOpsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ProjectTeamData(TcBaseObj):
    """
    This structure holds team member information for a single project.
    
    :var project: The TC_Project object for which team members are obtained.
    :var regularMembers: A list of non privileged members of the given project.
    :var projectTeamAdmins: A  list of project team adminstrators of the given project.
    :var privMembers: A list of privileged members of the given project.
    """
    project: TC_Project = None
    regularMembers: List[BusinessObject] = ()
    projectTeamAdmins: List[BusinessObject] = ()
    privMembers: List[BusinessObject] = ()


@dataclass
class ProjectTeamsResponse(TcBaseObj):
    """
    This structure holds team member information for all the given projects.
    
    :var projectTeams: List of ProjectTeamData objects one for each of the given projects.
    :var serviceData: A standard ServiceData object.
    """
    projectTeams: List[ProjectTeamData] = ()
    serviceData: ServiceData = None


@dataclass
class TeamMemberInfo(TcBaseObj):
    """
    A structure containing team member information.
    
    :var teamMember: The team member of a project.
    :var teamMemberType: A value indicating the teamMember type. Valid values are 0, 1 and 2.
    0 = Team member (teamMember is a GroupMember or Group object)
    1 = Privileged user (teamMember is a User object)
    2 = Team administrator (teamMember is a User object)
    """
    teamMember: BusinessObject = None
    teamMemberType: int = 0


@dataclass
class CopyProjectsInfo(TcBaseObj):
    """
    Structure that holds project information required to create a new TC_Project object using this operation.
    
    :var sourceProject: The TC_Project of  a project  to be copied.
    :var projectInfo: A ProjectInformation structure containing the destination project details..
    :var clientId: Unique identifier used by the client to track any errors.
    """
    sourceProject: TC_Project = None
    projectInfo: ProjectInformation = None
    clientId: str = ''
