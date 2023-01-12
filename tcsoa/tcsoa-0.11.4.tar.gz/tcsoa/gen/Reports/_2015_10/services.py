from __future__ import annotations

from tcsoa.gen.Reports._2015_10.CrfReports import GetOfficeStyleSheetResponse
from tcsoa.gen.BusinessObjects import ReportDefinition
from tcsoa.base import TcService


class CrfReportsService(TcService):

    @classmethod
    def getOfficeStylesheets(cls, reportDefinition: ReportDefinition) -> GetOfficeStyleSheetResponse:
        """
        The operation returns the list of associated Office stylesheets
        """
        return cls.execute_soa_method(
            method_name='getOfficeStylesheets',
            library='Reports',
            service_date='2015_10',
            service_name='CrfReports',
            params={'reportDefinition': reportDefinition},
            response_cls=GetOfficeStyleSheetResponse,
        )
