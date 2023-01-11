from __future__ import annotations

from tcsoa.gen.Internal.Core._2007_01.DataManagement import GetOrganizationInformationInputData, GetAttributeValuesInputData, GetOrganizationInformationResponse, GetAttributeValuesResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getAttributeValues(cls, classAttributeValues: List[GetAttributeValuesInputData]) -> GetAttributeValuesResponse:
        """
        This operation retrieves the values of an attribute from the database for all the instances of a class.
        """
        return cls.execute_soa_method(
            method_name='getAttributeValues',
            library='Internal-Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'classAttributeValues': classAttributeValues},
            response_cls=GetAttributeValuesResponse,
        )

    @classmethod
    def getOrganizationInformation(cls, options: List[GetOrganizationInformationInputData]) -> GetOrganizationInformationResponse:
        """
        This operation  retrieves the whole organization group hierarchy with groups at all the levels.  The hierarchy
        could include Role objects added to each groups as well as GroupMember objects as well by specifying options in
        input GetOrganizationInformationInputData object to include role objects and group member objects. The group
        name in GetOrganizationInformationInputData object should always be empty and the option to return only first
        level subgroups in GetOrganizationInformationInputData object is not implemented and should be ignored.
        """
        return cls.execute_soa_method(
            method_name='getOrganizationInformation',
            library='Internal-Core',
            service_date='2007_01',
            service_name='DataManagement',
            params={'options': options},
            response_cls=GetOrganizationInformationResponse,
        )
