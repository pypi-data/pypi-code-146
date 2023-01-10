from __future__ import annotations

from tcsoa.gen.Reports._2007_01.CrfReports import GetReportDefinitionsResponse
from typing import List
from tcsoa.gen.Reports._2008_06.CrfReports import ReportsCriteria2
from tcsoa.base import TcService


class CrfReportsService(TcService):

    @classmethod
    def getReportDefinitions(cls, inputCriteria: List[ReportsCriteria2]) -> GetReportDefinitionsResponse:
        """
        Retrieves a set of report definitions that meet the specified criteria.
        
        Use cases:
        Document set of user level use cases, should describe how user interacts with this operation to accomplish the
        goal.
        """
        return cls.execute_soa_method(
            method_name='getReportDefinitions',
            library='Reports',
            service_date='2008_06',
            service_name='CrfReports',
            params={'inputCriteria': inputCriteria},
            response_cls=GetReportDefinitionsResponse,
        )
