from tcsoa.gen.Internal_Multisite._2017_11.services import ArchiveRestoreService as imp0
from tcsoa.gen.Internal_Multisite._2018_06.services import SearchService as imp1
from tcsoa.gen.Internal_Multisite._2020_12.services import ImportExportTCXMLService as imp2
from tcsoa.gen.Internal_Multisite._2011_06.services import ImportExportAsyncService as imp3
from tcsoa.base import TcService


class ArchiveRestoreService(TcService):
    archiveObjects = imp0.archiveObjects
    getReportFileTicket = imp0.getReportFileTicket
    restoreObjects = imp0.restoreObjects


class SearchService(TcService):
    fetchOdsRecords = imp1.fetchOdsRecords


class ImportExportTCXMLService(TcService):
    getMultisiteDashBoardData = imp2.getMultisiteDashBoardData


class ImportExportAsyncService(TcService):
    remoteExport = imp3.remoteExport
