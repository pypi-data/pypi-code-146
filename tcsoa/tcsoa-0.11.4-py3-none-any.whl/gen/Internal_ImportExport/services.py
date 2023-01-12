from tcsoa.gen.Internal_ImportExport._2010_04.services import L10NImportExportService as imp0
from tcsoa.gen.Internal_ImportExport._2018_06.services import L10NImportExportService as imp1
from tcsoa.gen.Internal_ImportExport._2017_11.services import FileImportExportService as imp2
from tcsoa.gen.Internal_ImportExport._2017_05.services import FileImportExportService as imp3
from tcsoa.base import TcService


class L10NImportExportService(TcService):
    exportObjectsForTranslation = imp0.exportObjectsForTranslation
    exportObjectsForTranslation2 = imp1.exportObjectsForTranslation2
    filterObjectsForTranslation = imp0.filterObjectsForTranslation
    importTranslations = imp0.importTranslations


class FileImportExportService(TcService):
    importDocumentAsync = imp2.importDocumentAsync
    importDocumentOffline = imp2.importDocumentOffline
    importSpecAsync = imp3.importSpecAsync
