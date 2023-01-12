from __future__ import annotations

from tcsoa.gen.Internal.Administration._2018_11.SiteManagement import CreateOrUpdateSitesResponse, SiteInfo
from typing import List
from tcsoa.base import TcService


class SiteManagementService(TcService):

    @classmethod
    def createOrUpdateSites(cls, siteInfos: List[SiteInfo]) -> CreateOrUpdateSitesResponse:
        """
        This operation creates or updates POM_imc business objects with given properties. A new POM_imc business object
        will be created if it does not already exist, otherwise existing POM_imc business objects will be updated. In
        order to update, a valid Site ID must exist.
        
        The only required fields are Site Name and Site ID, additional properties can be added through the use of the
        additional properties map.
        
        All fields can be updated besides Site ID.
        
        Use cases:
        Use Case 1: Create a site based on the site ID, site name, and any additional properties.
        Use Case 2: Given a site ID that exists, update the site information with the site name and any additional
        properties
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateSites',
            library='Internal-Administration',
            service_date='2018_11',
            service_name='SiteManagement',
            params={'siteInfos': siteInfos},
            response_cls=CreateOrUpdateSitesResponse,
        )
