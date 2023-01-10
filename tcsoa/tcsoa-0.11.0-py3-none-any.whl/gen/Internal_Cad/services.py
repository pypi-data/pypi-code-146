from tcsoa.gen.Internal_Cad._2007_12.services import DataManagementService as imp0
from tcsoa.gen.Internal_Cad._2008_03.services import DataManagementService as imp1
from tcsoa.gen.Internal_Cad._2017_05.services import StructureManagementService as imp2
from tcsoa.gen.Internal_Cad._2013_05.services import DataManagementService as imp3
from tcsoa.gen.Internal_Cad._2008_06.services import DataManagementService as imp4
from tcsoa.gen.Internal_Cad._2008_05.services import DataManagementService as imp5
from tcsoa.gen.Internal_Cad._2010_04.services import DataManagementService as imp6
from tcsoa.base import TcService


class DataManagementService(TcService):
    createAppUidObjects = imp0.createAppUidObjects
    exportConfiguredNXAssembly = imp1.exportConfiguredNXAssembly
    queryPartRelatedFeatures = imp3.queryPartRelatedFeatures
    queryRelatedFeatures = imp4.queryRelatedFeatures
    resolveAttrMappingsForNX = imp5.resolveAttrMappingsForNX
    revise = imp6.revise
    saveAsNewItem = imp6.saveAsNewItem


class StructureManagementService(TcService):
    getProductStructureArrangements = imp2.getProductStructureArrangements
