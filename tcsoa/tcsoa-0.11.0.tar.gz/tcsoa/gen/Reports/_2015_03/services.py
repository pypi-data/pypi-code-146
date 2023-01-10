from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from tcsoa.gen.Reports._2015_03.CrfReports import GenerateReportsResponse2, PrintReportsCriteriaAsync, GeneratePrintReportsResponse, PrintReportsCriteria, GenerateReportsCriteria2Async
from tcsoa.gen.Reports._2010_04.CrfReports import GenerateReportsCriteria2
from tcsoa.gen.Reports._2007_01.CrfReports import GetReportDefinitionsResponse
from typing import List
from tcsoa.base import TcService


class CrfReportsService(TcService):

    @classmethod
    def generatePrintReports(cls, reportDefObj: ReportDefinition, inputs: List[PrintReportsCriteria]) -> GeneratePrintReportsResponse:
        """
        This operation generates the report based on the selected object and the report definition template.
        Optionally, it also sends the generated report to the physical printer for printing.
        """
        return cls.execute_soa_method(
            method_name='generatePrintReports',
            library='Reports',
            service_date='2015_03',
            service_name='CrfReports',
            params={'reportDefObj': reportDefObj, 'inputs': inputs},
            response_cls=GeneratePrintReportsResponse,
        )

    @classmethod
    def generatePrintReportsAsync(cls, reportDef: ReportDefinition, inputs: List[PrintReportsCriteriaAsync]) -> None:
        """
        This operation generates the print report asynchronously, based on the selected object and the report
        definition template. 
        Optionally, it also sends the generated report to the physical printer for printing.
        """
        return cls.execute_soa_method(
            method_name='generatePrintReportsAsync',
            library='Reports',
            service_date='2015_03',
            service_name='CrfReports',
            params={'reportDef': reportDef, 'inputs': inputs},
            response_cls=None,
        )

    @classmethod
    def generateReport(cls, inputs: List[GenerateReportsCriteria2]) -> GenerateReportsResponse2:
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
            method_name='generateReport',
            library='Reports',
            service_date='2015_03',
            service_name='CrfReports',
            params={'inputs': inputs},
            response_cls=GenerateReportsResponse2,
        )

    @classmethod
    def generateReportAsync(cls, inputs: List[GenerateReportsCriteria2Async]) -> None:
        """
        Generates report asynchronously(Summary Report/Custom Report/Item Report) using the specified criteria and the
        selected report style sheet. The report can be displayed with the selected report style. The report style is
        used to define how to display the report result in UI to end user. The report can optionally be saved as a
        Dataset in the Teamcenter database. The generated report is saved in the FMS transient volume.
        """
        return cls.execute_soa_method(
            method_name='generateReportAsync',
            library='Reports',
            service_date='2015_03',
            service_name='CrfReports',
            params={'inputs': inputs},
            response_cls=None,
        )

    @classmethod
    def getPrintTemplates(cls, contextObjects: List[BusinessObject]) -> GetReportDefinitionsResponse:
        """
        This operation returns the list of associated ReportDefinition Objects to the current selected object.
        """
        return cls.execute_soa_method(
            method_name='getPrintTemplates',
            library='Reports',
            service_date='2015_03',
            service_name='CrfReports',
            params={'contextObjects': contextObjects},
            response_cls=GetReportDefinitionsResponse,
        )
