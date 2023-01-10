from tcsoa.gen.Visualization._2011_02.services import DataManagementService as imp0
from tcsoa.gen.Visualization._2013_05.services import DataManagementService as imp1
from tcsoa.gen.Visualization._2011_02.services import StructureManagementService as imp2
from tcsoa.gen.Visualization._2013_05.services import StructureManagementService as imp3
from tcsoa.gen.Visualization._2013_12.services import StructureManagementService as imp4
from tcsoa.gen.Visualization._2016_03.services import DataManagementService as imp5
from tcsoa.base import TcService


class DataManagementService(TcService):
    createLaunchFile = imp0.createLaunchFile
    createLaunchInfo = imp1.createLaunchInfo
    getMetaDataStampWithContext = imp5.getMetaDataStampWithContext


class StructureManagementService(TcService):
    createVisSC = imp2.createVisSC
    createVisSCsFromBOMs = imp2.createVisSCsFromBOMs
    createVisSCsFromBOMs2 = imp3.createVisSCsFromBOMs
    createVisSCsFromBOMsWithOptions = imp4.createVisSCsFromBOMsWithOptions
