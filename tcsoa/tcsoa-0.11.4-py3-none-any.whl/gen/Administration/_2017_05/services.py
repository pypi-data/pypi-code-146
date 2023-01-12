from __future__ import annotations

from tcsoa.gen.Administration._2017_05.GroupManagement import AddChildGroupsToGroupStructure
from tcsoa.gen.Administration._2017_05.RoleManagement import RoleGroupStructure, AddRolesToGroupStructure
from tcsoa.gen.Administration._2017_05.UserManagement import AddUsersAsGroupMembersStructure, UserRoleGroupStructure, UserManagementResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class GroupManagementService(TcService):

    @classmethod
    def addChildGroups(cls, childGroupsToGroupStructs: List[AddChildGroupsToGroupStructure]) -> ServiceData:
        """
        Adds new groups and existing groups as child groups to specified Group objects. If groups are new, then they
        will be created first before they are added.
        """
        return cls.execute_soa_method(
            method_name='addChildGroups',
            library='Administration',
            service_date='2017_05',
            service_name='GroupManagement',
            params={'childGroupsToGroupStructs': childGroupsToGroupStructs},
            response_cls=ServiceData,
        )


class UserManagementService(TcService):

    @classmethod
    def removeGroupMembers(cls, userRoleGroupStructs: List[UserRoleGroupStructure]) -> UserManagementResponse:
        """
        This operation removes group members for specified User objects under given Group objects with specified Role
        objects. This operation requires system administration privilege or group administration privilege. Input
        should not have null User, Group and Role objects.
        """
        return cls.execute_soa_method(
            method_name='removeGroupMembers',
            library='Administration',
            service_date='2017_05',
            service_name='UserManagement',
            params={'userRoleGroupStructs': userRoleGroupStructs},
            response_cls=UserManagementResponse,
        )

    @classmethod
    def addUsersAsGroupMembers(cls, userRoleGroupStructs: List[AddUsersAsGroupMembersStructure]) -> ServiceData:
        """
        Adds new Users and existing Users as Group Members under the given Group objects with specific Role object. If
        a User is new, it will be created first before it is added as GroupMember. This operation requires system
        administration privilege or Group administration privilege. Specified Role objects must be an existing Role in
        the Group.
        """
        return cls.execute_soa_method(
            method_name='addUsersAsGroupMembers',
            library='Administration',
            service_date='2017_05',
            service_name='UserManagement',
            params={'userRoleGroupStructs': userRoleGroupStructs},
            response_cls=ServiceData,
        )


class RoleManagementService(TcService):

    @classmethod
    def removeRolesFromGroup(cls, roleGroupStructs: List[RoleGroupStructure]) -> ServiceData:
        """
        This operation removes specified Role objects from specified Group objects.
        """
        return cls.execute_soa_method(
            method_name='removeRolesFromGroup',
            library='Administration',
            service_date='2017_05',
            service_name='RoleManagement',
            params={'roleGroupStructs': roleGroupStructs},
            response_cls=ServiceData,
        )

    @classmethod
    def addRolesToGroup(cls, roleGroupStructs: List[AddRolesToGroupStructure]) -> ServiceData:
        """
        Adds new Roles and existing Roles to the specified Group objects. If the roles are new, it will create them
        first before they are added.
        """
        return cls.execute_soa_method(
            method_name='addRolesToGroup',
            library='Administration',
            service_date='2017_05',
            service_name='RoleManagement',
            params={'roleGroupStructs': roleGroupStructs},
            response_cls=ServiceData,
        )
