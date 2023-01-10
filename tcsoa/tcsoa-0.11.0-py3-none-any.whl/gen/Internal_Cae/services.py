from tcsoa.gen.Internal_Cae._2012_09.services import StructureManagementService as imp0
from tcsoa.gen.Internal_Cae._2011_06.services import StructureManagementService as imp1
from tcsoa.gen.Internal_Cae._2012_02.services import StructureManagementService as imp2
from tcsoa.gen.Internal_Cae._2013_05.services import StructureManagementService as imp3
from tcsoa.gen.Internal_Cae._2012_02.services import SimulationProcessManagementService as imp4
from tcsoa.gen.Internal_Cae._2013_12.services import SimulationProcessManagementService as imp5
from tcsoa.gen.Internal_Cae._2014_06.services import StructureManagementService as imp6
from tcsoa.gen.Internal_Cae._2009_10.services import SimulationProcessManagementService as imp7
from tcsoa.gen.Internal_Cae._2013_12.services import StructureManagementService as imp8
from tcsoa.base import TcService


class StructureManagementService(TcService):
    createNewModelByDM = imp0.createNewModelByDM
    executeDatamap = imp1.executeDatamap
    executeDatamap2 = imp0.executeDatamap
    executeMarkUpToDate = imp0.executeMarkUpToDate
    executeStructureMap = imp1.executeStructureMap
    generateNodeXML = imp2.generateNodeXML
    getCAEPropertyComparisonDetails = imp3.getCAEPropertyComparisonDetails
    loadSimulationDataMonitor = imp6.loadSimulationDataMonitor
    propagateCAEModelAttributes = imp8.propagateCAEModelAttributes
    refreshSimulationDataMonitor = imp6.refreshSimulationDataMonitor
    updateModelAttsByDM = imp0.updateModelAttsByDM


class SimulationProcessManagementService(TcService):
    importSimulationObjects = imp4.importSimulationObjects
    importSimulationObjects2 = imp5.importSimulationObjects2
    notifyUser = imp7.notifyUser
