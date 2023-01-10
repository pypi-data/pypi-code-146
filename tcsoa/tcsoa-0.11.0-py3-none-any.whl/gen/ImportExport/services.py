from tcsoa.gen.ImportExport._2011_06.services import FileImportExportService as imp0
from tcsoa.gen.ImportExport._2007_06.services import FileImportExportService as imp1
from tcsoa.gen.ImportExport._2008_06.services import FileImportExportService as imp2
from tcsoa.gen.ImportExport._2017_11.services import FileImportExportService as imp3
from tcsoa.gen.ImportExport._2012_09.services import FileImportExportService as imp4
from tcsoa.base import TcService


class FileImportExportService(TcService):
    createReqMarkup = imp0.createReqMarkup
    exportToApplication = imp1.exportToApplication
    exportToApplication2 = imp2.exportToApplication
    exportToApplication3 = imp0.exportToApplication
    exportToApplication4 = imp3.exportToApplication
    getExportTemplates = imp2.getExportTemplates
    getExportTemplates2 = imp0.getExportTemplates
    importFromApplication = imp1.importFromApplication
    importFromApplication2 = imp2.importFromApplication
    importFromApplication3 = imp0.importFromApplication
    importFromApplication4 = imp4.importFromApplication
    updateReqMarkup = imp0.updateReqMarkup
