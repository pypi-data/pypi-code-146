from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Multisite._2020_12.ImportExportTCXML import ReportRecipe, StrVecMap, MultisiteDashboardResponse
from tcsoa.base import TcService


class ImportExportTCXMLService(TcService):

    @classmethod
    def getMultisiteDashBoardData(cls, sessionOptions: StrVecMap, reportRecipe: List[ReportRecipe]) -> MultisiteDashboardResponse:
        """
        The getMultisiteDashboard operation provides the historic dashboard data for each site in Multi-Site federation
        which helps to visualize the critical errors occurred during Multi-Site import, export and synchronization
        operations. It also helps to track and analyze the key data points to monitor the health of Multi-Site
        operation.
        
        Use cases:
        In the Multi-Site federation, a user can share the business objects among the participating sites, the client
        shares business object(s) using the remote import or remote export functionality. During the import/export
        operation errors can occur due to network, data condition etc. These errors should be tracked analyzed and
        displayed in dashboard so that the user can take appropriate actions.
        """
        return cls.execute_soa_method(
            method_name='getMultisiteDashBoardData',
            library='Internal-Multisite',
            service_date='2020_12',
            service_name='ImportExportTCXML',
            params={'sessionOptions': sessionOptions, 'reportRecipe': reportRecipe},
            response_cls=MultisiteDashboardResponse,
        )
