from tcsoa.gen.Cae._2012_02.services import StructureManagementService as imp0
from tcsoa.gen.Cae._2014_06.services import StructureManagementService as imp1
from tcsoa.gen.Cae._2011_06.services import SimulationProcessManagementService as imp2
from tcsoa.gen.Cae._2013_12.services import SimulationProcessManagementService as imp3
from tcsoa.base import TcService


class StructureManagementService(TcService):
    executeDatamap = imp0.executeDatamap
    executeDeriveCAEStructure = imp1.executeDeriveCAEStructure
    executeStructureMap = imp0.executeStructureMap


class SimulationProcessManagementService(TcService):
    launchSimulationTool = imp2.launchSimulationTool
    launchSimulationTool2 = imp3.launchSimulationTool2
