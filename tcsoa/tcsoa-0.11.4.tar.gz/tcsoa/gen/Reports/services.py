from tcsoa.gen.Reports._2007_06.services import CubeReportsService as imp0
from tcsoa.gen.Reports._2007_01.services import CrfReportsService as imp1
from tcsoa.gen.Reports._2015_03.services import CrfReportsService as imp2
from tcsoa.gen.Reports._2008_12.services import CrfReportsService as imp3
from tcsoa.gen.Reports._2010_04.services import CrfReportsService as imp4
from tcsoa.gen.Reports._2015_10.services import CrfReportsService as imp5
from tcsoa.gen.Reports._2008_06.services import CrfReportsService as imp6
from tcsoa.base import TcService


class CubeReportsService(TcService):
    constructReportURL = imp0.constructReportURL


class CrfReportsService(TcService):
    createReportDefinition = imp1.createReportDefinition
    generatePrintReports = imp2.generatePrintReports
    generatePrintReportsAsync = imp2.generatePrintReportsAsync
    generateReport = imp1.generateReport
    generateReport2 = imp2.generateReport
    generateReportAsync = imp2.generateReportAsync
    generateReportDefintionIds = imp1.generateReportDefintionIds
    generateReports = imp3.generateReports
    generateReports2 = imp4.generateReports
    getOfficeStylesheets = imp5.getOfficeStylesheets
    getPrintTemplates = imp2.getPrintTemplates
    getReportDefinitions = imp1.getReportDefinitions
    getReportDefinitions2 = imp6.getReportDefinitions
