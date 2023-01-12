from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2013_12.DataManagement import GetTCSessionInfoResponse3, GetTCSessionInfoResponse
from tcsoa.gen.Internal.AWS2._2013_12.OrganizationManagement import GroupMembershipInput2
from tcsoa.gen.Internal.AWS2._2012_10.OrganizationManagement import GroupMembershipResponse
from typing import List
from tcsoa.gen.Internal.AWS2._2013_12.Workflow import TaskSearchResponse, TaskSearchInput
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getTCSessionInfo2(cls) -> GetTCSessionInfoResponse:
        """
        This operation gets information about the current user's Teamcenter session.s
        """
        return cls.execute_soa_method(
            method_name='getTCSessionInfo2',
            library='Internal-AWS2',
            service_date='2013_12',
            service_name='DataManagement',
            params={},
            response_cls=GetTCSessionInfoResponse,
        )

    @classmethod
    def getTCSessionInfo3(cls, extraInfoIn: List[str]) -> GetTCSessionInfoResponse3:
        """
        This operation provides information about the current user's Teamcenter session. The additional  information
        provided in getTCSessionInfo3 as compared to getTCSessionInfo2 is a map of extra information. Any new
        information that needs to be passed to the client will be put in this map.
        
        Use cases:
        After the user logs in to Active Workspace this operation is invoked by the Active Workspace client to get
        information related to the user session like Groups, Projects, and the Teamcenter Server version.
        """
        return cls.execute_soa_method(
            method_name='getTCSessionInfo3',
            library='Internal-AWS2',
            service_date='2013_12',
            service_name='DataManagement',
            params={'extraInfoIn': extraInfoIn},
            response_cls=GetTCSessionInfoResponse3,
        )


class WorkflowService(TcService):

    @classmethod
    def performTaskSearch(cls, searchInput: TaskSearchInput) -> TaskSearchResponse:
        """
        This operation searches for EPMTasks in a user's inbox based on input search criteria.
        
        Use cases:
        Use this operation to search for tasks in logged in user's inbox. User can provide multiple search criteria to
        search for tasks. For example :
        
        Search  tasks by specific task type
        User wants to search for all the Do tasks in his inbox.
        
        Search tasks by assignee
        User wants to search for all the task in his inbox which are assigned to a specific group.
        
        Search tasks by due date
        User wants to search for all the tasks  in his inbox  based on a due date. The  due date can  be specified as a
        specific date or month or year.
        """
        return cls.execute_soa_method(
            method_name='performTaskSearch',
            library='Internal-AWS2',
            service_date='2013_12',
            service_name='Workflow',
            params={'searchInput': searchInput},
            response_cls=TaskSearchResponse,
        )


class OrganizationManagementService(TcService):

    @classmethod
    def getGroupMembership2(cls, input: GroupMembershipInput2) -> GroupMembershipResponse:
        """
        This operation searches for active GroupMember based on name, role and group inputs . Literal and partial
        strings (strings with wildcard character '*') are supported. Literal string are AND together and partial
        strings are grouped OR and AND with with the literal strings.
        Using the following search critera:
        
        userId = "tc*"
        userName =  "tcadmin"
        groupName = "dba"
        roleName = "DB*"
        
        The operation will assemble the final search criteria as follows: 
        
        username = "tcadmin" AND groupName = "dba" AND ( userId = "tc*" OR roleName = "DB*" ). 
        
        Following examples demonstrate how this operation can be used to get GroupMember objects based on different
        inputs:
        
        - Search for GroupMember objects which  have User objects where userd_id, user_name contain  "XYZ". Input for
        this search will be :
        
        
        userId   - "*XYZ*"
        userName - "*XYZ*"
        
        - Search for GroupMember objects which have User or Role or Group objects where userd_id, user_name,
        role_name,or name contain  "xyz". Input for this search will be :
        
        
        userId      -   "*xyz*"
        userName    -  "*xyz*"
        roleName    -  "*xyz*"
        groupName   -  "*xyz*"
        
        - Search for GroupMember objects which have User or Role objects where userd_id,user_name, role_name contain 
        "xyz" and has Group object with name "dba". Inputs for this search will be :
        
        
        userId     -   "*xyz*"
        userName   -  "*xyz*"
        roleName   -  "*xyz*"
        groupName  -  "dba"
        
        - Search for GroupMember objects which have User or Group objects where userd_id, user_name, name contain 
        "xyz" and has Role object with role_name  "DBA". Inputs for this search will be :
        
        
        userId           -   "*xyz*"
        userName   -  "*xyz*"
        roleName   -  "DBA"
        groupName  -  "*xyz*"   
        
        - Search for GroupMember objects which have User objects where user_id, user_name contain"xyz" and Role object
        with role_name  "DBA" and Group object with name "dba". Inputs for this search will be :
        
        
        userId     -   "*xyz*"
        userName   -  "*xyz*"
        roleName   -  "DBA"
        groupName  -  "dba"
        
        - Search for GroupMember objects which have User objects where user_id "xyz" and user_name "xyz" and Role
        object with role_name  "DBA" and Group object with name "dba". Inputs for this search will be :
        
        
        userId     -   "xyz"
        userName   -  "xyz"
        roleName   -  "DBA"
        groupName  -  "dba"
        
        Use cases:
        Search GroupMember(s) againt signoff profile of a select-signoff task:
        
        User has an active select-signoff-task with signoff profile. Profile specifies the group, role and number of
        the users who are allowed to perform the review. This task has following profiles:
        - * / DBA / 1 ( Any User  who has a role "DBA")
        - dba / * / 1 ( Any User who is in  group "dba" )
        - dba / DBA / 1 ( Any User who has a role "DBA" and in group "dba" )
        - Engineering++ / * / 1 ( Any  User from "Engineering" sub-group )
        - GroupA++ / RoleA / 1 ( Any User who has a role "RoleA" and from "GroupA" sub-group )
        
        
        
        Here user wants to search for all the active GroupMembers in Teamcenter organization with above profiles to
        signoff the task.
        """
        return cls.execute_soa_method(
            method_name='getGroupMembership2',
            library='Internal-AWS2',
            service_date='2013_12',
            service_name='OrganizationManagement',
            params={'input': input},
            response_cls=GroupMembershipResponse,
        )
