from tcsoa.gen.Internal_XlsBom._2020_12.services import ImportService as imp0
from tcsoa.base import TcService


class ImportService(TcService):
    getStructureInfoFromExcel = imp0.getStructureInfoFromExcel
    importExcelAndUpdateMappingGrp = imp0.importExcelAndUpdateMappingGrp
    importExcelAndUpdateMappingGrpAsync = imp0.importExcelAndUpdateMappingGrpAsync
