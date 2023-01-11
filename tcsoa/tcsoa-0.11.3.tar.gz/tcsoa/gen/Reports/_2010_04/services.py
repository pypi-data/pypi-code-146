from __future__ import annotations

from tcsoa.gen.Reports._2010_04.CrfReports import GenerateReportsCriteria2
from tcsoa.gen.Reports._2008_12.CrfReports import GenerateReportsResponse
from typing import List
from tcsoa.base import TcService


class CrfReportsService(TcService):

    @classmethod
    def generateReports(cls, inputs: List[GenerateReportsCriteria2]) -> GenerateReportsResponse:
        """
        Generates reports (Summary Report/Custom Report/Item Report) using the specified criteria and the selected
        report style. The report will be displayed by the selected report style at the end. If no report style is
        selected, then the report will be displayed in xml file to the end user. If user would like to save the report
        as a Dataset, it will use the provided Dataset name to save the report to Teamcenter. After the report is
        generated, the report file will be uploaded to the transient volumes, user can get it from the transient
        volumes. Multiple reports generation is not supported currently.
        
        Use cases:
        User can generate one report (Summary Report/Custom Report/Item Report) by selecting one report definition and
        then inputs criteria for the report query, selects one report style, and inputs the Dataset name for the report
        if user would like to save the report as a Dataset in Teamcenter.
        """
        return cls.execute_soa_method(
            method_name='generateReports',
            library='Reports',
            service_date='2010_04',
            service_name='CrfReports',
            params={'inputs': inputs},
            response_cls=GenerateReportsResponse,
        )
