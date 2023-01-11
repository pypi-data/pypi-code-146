from tcsoa.gen.Internal_BusinessModeler._2010_04.services import DataModelManagementService as imp0
from tcsoa.gen.Internal_BusinessModeler._2010_09.services import DataModelManagementService as imp1
from tcsoa.gen.Internal_BusinessModeler._2013_05.services import DynamicLOVQueryService as imp2
from tcsoa.gen.Internal_BusinessModeler._2007_01.services import DataModelManagementService as imp3
from tcsoa.gen.Internal_BusinessModeler._2011_06.services import DataModelManagementService as imp4
from tcsoa.base import TcService


class DataModelManagementService(TcService):
    deployDataModel = imp0.deployDataModel
    deployDataModel2 = imp1.deployDataModel2
    exportDataModel = imp3.exportDataModel
    getChangedTemplateFiles = imp0.getChangedTemplateFiles
    getSiteTemplateDeployInfo = imp1.getSiteTemplateDeployInfo
    getTemplateFiles = imp0.getTemplateFiles
    importDataModel = imp3.importDataModel
    updateClientMetaCache = imp4.updateClientMetaCache
    updateServerMetaCache = imp4.updateServerMetaCache


class DynamicLOVQueryService(TcService):
    executeDynamicLOVQuery = imp2.executeDynamicLOVQuery
