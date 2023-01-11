from tcsoa.gen.Internal_OccMgmt._2020_12.services import EffectivityManagementService as imp0
from tcsoa.gen.Internal_OccMgmt._2020_05.services import ImportExportService as imp1
from tcsoa.base import TcService


class EffectivityManagementService(TcService):
    getEffectivity = imp0.getEffectivity
    setEffectivity = imp0.setEffectivity


class ImportExportService(TcService):
    getMappingGroupInfo = imp1.getMappingGroupInfo
    importExcelAndUpdateMappingGrp = imp1.importExcelAndUpdateMappingGrp
    importExcelAndUpdateMappingGrpAsync = imp1.importExcelAndUpdateMappingGrpAsync
