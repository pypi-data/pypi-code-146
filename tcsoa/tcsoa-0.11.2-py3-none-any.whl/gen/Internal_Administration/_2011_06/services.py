from __future__ import annotations

from tcsoa.gen.Internal.Administration._2011_06.OrganizationManagement import GetGroupsForRoleInput, GetOrganizationGroupResponse
from typing import List
from tcsoa.base import TcService


class OrganizationManagementService(TcService):

    @classmethod
    def getOrganizationGroups(cls, inputs: List[GetGroupsForRoleInput]) -> GetOrganizationGroupResponse:
        """
        This operation retrieves list of organization groups which contain the given roles. An additional filtered
        organization tree structure which only includes those matched groups for each role could be returned as well
        depending on an option from input parameter. The group tree structure should be included if group hierarchy
        information is needed.
        """
        return cls.execute_soa_method(
            method_name='getOrganizationGroups',
            library='Internal-Administration',
            service_date='2011_06',
            service_name='OrganizationManagement',
            params={'inputs': inputs},
            response_cls=GetOrganizationGroupResponse,
        )
