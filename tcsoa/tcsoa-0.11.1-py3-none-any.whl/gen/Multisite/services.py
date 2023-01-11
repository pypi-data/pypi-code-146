from tcsoa.gen.Multisite._2019_06.services import SearchService as imp0
from tcsoa.gen.Multisite._2011_06.services import ImportExportService as imp1
from tcsoa.gen.Multisite._2019_06.services import ImportExportTCXMLService as imp2
from tcsoa.gen.Multisite._2014_10.services import ImportExportTCXMLService as imp3
from tcsoa.gen.Multisite._2007_06.services import ImportExportService as imp4
from tcsoa.base import TcService


class SearchService(TcService):
    publish = imp0.publish
    unpublish = imp0.unpublish


class ImportExportService(TcService):
    registerItemId = imp1.registerItemId
    remoteImport = imp4.remoteImport
    unregisterItemId = imp1.unregisterItemId


class ImportExportTCXMLService(TcService):
    remoteCheckin = imp2.remoteCheckin
    remoteCheckout = imp2.remoteCheckout
    remoteExport = imp3.remoteExport
    remoteImport = imp3.remoteImport
    remoteImportByUID = imp3.remoteImportByUID
