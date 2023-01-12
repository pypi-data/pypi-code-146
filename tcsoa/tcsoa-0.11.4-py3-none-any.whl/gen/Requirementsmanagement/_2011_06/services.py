from __future__ import annotations

from typing import List
from tcsoa.gen.Requirementsmanagement._2011_06.RequirementsManagement import PublishColumnConfigInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def publishColumnConfiguration(cls, input: List[PublishColumnConfigInfo]) -> ServiceData:
        """
        This operation publishes the Column Configuration that is Mark as Publishable by the user. This operation will
        get the column configuration values from the specified Fnd0ColumnConfiguration object and create the site
        preferences. After creating the site preference it will set the "IsPublished" property to true present on the
        specified Fnd0ColumnConfiguration object.  So by creating the site preference these column configuration will
        be visible to all present users in the system. This operation converts the user preferences to the site level
        preferences in Teamcenter Context so that all users can use it. When user save the column configuration,
        applied on the BOM structure then it will store all applied column configuration values as user protection
        scope preferences. After that user can mark the same column configuration as Mark as Publishable that means
        user want that column configuration to be available to other users in the system. So Administrator privileged
        user can publish the column configuration so it will be available to all other users in the system. The user
        which originally saved the column configuration will see two preferences with same name, one with protection
        scope user and other one with site protection scope.
        
        Use cases:
        You can publish the column configuration that is Mark as Publishable by the user so that it will be visible to
        all other users and others users can apply the publish column configuration on BOM structure.
        """
        return cls.execute_soa_method(
            method_name='publishColumnConfiguration',
            library='Requirementsmanagement',
            service_date='2011_06',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
