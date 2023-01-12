from __future__ import annotations

from tcsoa.gen.Internal.Administration._2012_10.OrganizationManagement import GetOrganizationUserMembersResponse, OrganizationMembersInput
from tcsoa.base import TcService


class OrganizationManagementService(TcService):

    @classmethod
    def getOrganizationGroupMembers(cls, input: OrganizationMembersInput) -> GetOrganizationUserMembersResponse:
        """
        This operation searches for GroupMember objects in Teamcenter organization. The found GroupMember objects would
        have either user ID or user name matches with the user ID and user name in search criteria, and group name and
        role name match the group name and role name respectively in search criteria. It also has option to return
        inactive GroupMember objects.
        
        Use cases:
        Find group members for given group, role, user id and user name.
        """
        return cls.execute_soa_method(
            method_name='getOrganizationGroupMembers',
            library='Internal-Administration',
            service_date='2012_10',
            service_name='OrganizationManagement',
            params={'input': input},
            response_cls=GetOrganizationUserMembersResponse,
        )
