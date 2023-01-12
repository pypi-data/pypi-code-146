from __future__ import annotations

from tcsoa.gen.BusinessObjects import Group, GroupMember, User, Role, TC_Project
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Core._2018_11.ProjectLevelSecurity import UserGroupRoleInfo
from dataclasses import dataclass


@dataclass
class GroupMemberPrivilege(TcBaseObj):
    """
    The structure holds the GroupMember object and its privilege in the ProjectTeam of the input TC_Project.
    
    :var groupmember: The GroupMember object
    :var privilege: The privilege status of the GroupMember in the ProjectTeam of the input TC_Project.
    0 = regular member
    1 = privileged member
    2 = project team administrator
    3 = project administrator
    :var isRemovable: Indicates if the GroupMember is removable from the ProjectTeam. If true, it indicates the
    GroupMember is directly in the ProjectTeam, and it is removable from the ProjectTeam. If false, it indicates the
    GroupMember is under a Group in the ProjectTeam, and it is not removable from the ProjectTeam.
    """
    groupmember: GroupMember = None
    privilege: int = 0
    isRemovable: bool = False


@dataclass
class GroupNode(TcBaseObj):
    """
    The view model for Group, which contains the Group object itself and a flag to indicate if the Group is removable
    from the ProjectTeam.
    
    :var tcGroup: The Group node view model
    :var isRemovable: If true, the Group is directly in the ProjectTeam and is removable. If false, the Group is a
    child of another Group and is not removable.
    """
    tcGroup: Group = None
    isRemovable: bool = False


@dataclass
class GroupNodeWithChildren(TcBaseObj):
    """
    The structure of a Group node with its child nodes.
    
    :var groupNode: The GroupNode.
    :var childGroups: The child Groups.
    :var childRoles: The Roles under the Group.
    """
    groupNode: GroupNode = None
    childGroups: List[GroupNode] = ()
    childRoles: List[GroupRoleNodeWithChildren] = ()


@dataclass
class GroupRoleNode(TcBaseObj):
    """
    The view model of a Role object, which contains the Role object it self, the Group object it is associated with,
    and a flag indicating if it is removable from the Project Team.
    
    :var tcGroup: The Group.
    :var tcRole: The Role.
    :var isRemovable: For the first level GroupRoleNode structures, they are removable because these are the parent
    node for the GroupMembers that are directly in the project members. Hence the values are true. For the
    GroupRoleNode structures under the Group objects in the ProjectTeam, the values are false.
    """
    tcGroup: Group = None
    tcRole: Role = None
    isRemovable: bool = False


@dataclass
class GroupRoleNodeWithChildren(TcBaseObj):
    """
    The structure which holds the first level node (Group.Role) and the GroupMember objects along with their privilege
    in the Project Team.
    
    :var groupRole: The first level Group.Role node.
    :var groupmemberList: The GroupMember objects that are in the Project Team with the same Group and Role, along with
    their privilege.
    """
    groupRole: GroupRoleNode = None
    groupmemberList: List[GroupMemberPrivilege] = ()


@dataclass
class ProjectAndPrivilege(TcBaseObj):
    """
    The structure to hold the TC_Project object and the privilege of the user.
    
    :var project: The TC_Project object retrieved from DB.
    :var privilege: The User's privilege in the associated TC_Project.
    - -1 = User is not a member of the project (possible when having bypass for DBA users).
    -  0 = User is a regular member of the project.
    -  1 = User is a project author of the project.
    -  2 = User is a project team administrator of the project.
    -  3 = User is the owning user of the project.
    
    """
    project: TC_Project = None
    privilege: int = 0


@dataclass
class ProjectPrivilegeResponse(TcBaseObj):
    """
    This structure contains a list of ProjectAndPrivilege structure that has privilege of the login user in each
    TC_Project object, and the Service Data.
    
    :var projectPrivilege: A list of TC_Project objects and the privileges of the login user in them.
    :var serviceData: The Service Data
    """
    projectPrivilege: List[ProjectAndPrivilege] = ()
    serviceData: ServiceData = None


@dataclass
class ProjectTeamPagedInput(TcBaseObj):
    """
    The paginated input to get the ProjectTeam for the given TC_Project object.
    
    :var project: The TC_Project object to get the ProjectTeam.
    :var startIndex: The start index
    :var pageSize: The page size
    :var quickLoad: If true, to retrieve the ProjectTeam data from the server memory. If false, the data is retrieved
    from the database.
    """
    project: TC_Project = None
    startIndex: int = 0
    pageSize: int = 0
    quickLoad: bool = False


@dataclass
class ProjectTeamPagedResponse(TcBaseObj):
    """
    The structure holds the paginated first level nodes of ProjectTeam, starting with Group objects.
    
    :var totalMemberCount: The total number of the project members in the ProjectTeam of the given TC_Project object.
    :var endIndex: The index of the last element returned for pagination.
    :var groups: A list of Group objects that are in the project members of the input TC_Project.
    :var structuredGroupMembers: A list of structured GroupRoleNode which represents the first level node of the
    GroupMember objects in the ProjectTeam.
    :var serviceData: The Service Data
    """
    totalMemberCount: int = 0
    endIndex: int = 0
    groups: List[GroupNode] = ()
    structuredGroupMembers: List[GroupRoleNode] = ()
    serviceData: ServiceData = None


@dataclass
class SetPrivilegeForUserInput(TcBaseObj):
    """
    The input structure for setUserPrivilege operation
    
    :var project: The TC_Project object which the User privilege needs to be set.
    :var users: The User objects to set privilege.
    :var groupNode: The Group node to set privilege on all the User objects under it. The privilege will be set for all
    the User objects under this Group, including subgroups.
    :var groupRoleNode: The GroupRole node to set privilege on all the User objects under it. The privilege will be set
    on all the User objects under this GroupRole node
    :var privilegeStatus: - 0 = regular member (non-privileged member)
    - 1 = project author (privileged member)
    - 2 = project team administrator
    
    """
    project: TC_Project = None
    users: List[User] = ()
    groupNode: List[GroupNode] = ()
    groupRoleNode: List[GroupRoleNode] = ()
    privilegeStatus: int = 0


@dataclass
class UserProjectsAndPrivilege(TcBaseObj):
    """
    The structure holds the User and the TC_Project objects that are associated with this User, along with the User's
    privilege status in each TC_Project.
    
    :var userGroupRole: The given User or the given User with specific Group and Role that the TC_Project objects are
    associated with.
    :var totalProjectCount: The total number of TC_Project associtated with the User.
    :var endIndex: The end index of the paged response.
    :var projects: All the TC_Project objects that are associated with the given User, along with the privilege status
    of the User.
    """
    userGroupRole: UserGroupRoleInfo = None
    totalProjectCount: int = 0
    endIndex: int = 0
    projects: List[ProjectAndPrivilege] = ()


@dataclass
class UserProjectsAndPrivilegeResponse(TcBaseObj):
    """
    The structure holds the User objects, the associated TC_Project objects, and their privilege status in each
    TC_Project objects.
    
    :var userProjects: The Users and their associated TC_Projects, along with the privilege status of each User.
    :var serviceData: The Service Data.
    """
    userProjects: List[UserProjectsAndPrivilege] = ()
    serviceData: ServiceData = None


@dataclass
class ChildStructureResponse(TcBaseObj):
    """
    The structure to hold the children of a specific node in ProjectTeam.
    
    :var childGroups: The child Groups.
    :var childRoles: The child Roles.
    :var childGroupMembers: The child GroupMembers.
    :var childGroupMap: Map the Group objects to their child Groups.
    :var sd: The Service Data.
    """
    childGroups: List[GroupNodeWithChildren] = ()
    childRoles: List[GroupRoleNodeWithChildren] = ()
    childGroupMembers: List[GroupMemberPrivilege] = ()
    childGroupMap: GroupChildGroup = None
    sd: ServiceData = None


@dataclass
class AddOrRemoveProjectMemberInput(TcBaseObj):
    """
    The structure holds the TC_Project object and the nodes to add or remove.
    
    :var project: The TC_Project object which the members are added or removed.
    :var gms: The GroupMember objects to be added or removed.
    :var groups: The Group objects to be added or removed.
    :var groupRoles: The GroupRole nodes to have the GroupMember objects under it added to or removed from the Project
    Team.
    :var addOrRemove: Indicates if the members need to be added or removed from the TC_Project. If true, the members in
    the input are added to the project. If false, the members in the input are removed from the project.
    """
    project: TC_Project = None
    gms: List[GroupMember] = ()
    groups: List[Group] = ()
    groupRoles: List[GroupRoleNode] = ()
    addOrRemove: bool = False


"""
The map for the Group object to its child GroupNodes.
"""
GroupChildGroup = Dict[Group, List[GroupNodeWithChildren]]
