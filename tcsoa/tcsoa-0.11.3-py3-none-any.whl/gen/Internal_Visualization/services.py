from tcsoa.gen.Internal_Visualization._2008_06.services import StructureManagementService as imp0
from tcsoa.gen.Internal_Visualization._2008_06.services import DataManagementService as imp1
from tcsoa.gen.Internal_Visualization._2010_09.services import DataManagementService as imp2
from tcsoa.gen.Internal_Visualization._2012_10.services import DataManagementService as imp3
from tcsoa.gen.Internal_Visualization._2010_09.services import StructureManagementService as imp4
from tcsoa.gen.Internal_Visualization._2011_12.services import StructureManagementService as imp5
from tcsoa.gen.Internal_Visualization._2010_04.services import DataManagementService as imp6
from tcsoa.gen.Internal_Visualization._2017_05.services import DataManagementService as imp7
from tcsoa.gen.Internal_Visualization._2018_11.services import StructureManagementService as imp8
from tcsoa.base import TcService


class StructureManagementService(TcService):
    areRecipesMergable = imp0.areRecipesMergable
    createBOMsFromRecipes = imp0.createBOMsFromRecipes
    createVisSC = imp4.createVisSC
    createVisSCsFromBOMs = imp0.createVisSCsFromBOMs
    expandPSFromOccurrenceList = imp0.expandPSFromOccurrenceList
    expandPSFromOccurrenceList2 = imp5.expandPSFromOccurrenceList
    getStructureIdFromRecipe = imp8.getStructureIdFromRecipe


class DataManagementService(TcService):
    authenticateUser = imp1.authenticateUser
    createLaunchFile = imp1.createLaunchFile
    createMarkup = imp1.createMarkup
    createSessionModel = imp1.createSessionModel
    createSnapshot3D = imp2.createSnapshot3D
    createSnapshot3D2 = imp3.createSnapshot3D
    createTwoDSnapshot = imp1.createTwoDSnapshot
    findProductViewsForNodes = imp2.findProductViewsForNodes
    gatherMarkups = imp6.gatherMarkups
    gatherSnapshot3DList = imp2.gatherSnapshot3DList
    getLatestFileReadTickets = imp1.getLatestFileReadTickets
    getMetaDataStamp = imp1.getMetaDataStamp
    getNodesPresentInProductView = imp2.getNodesPresentInProductView
    getSnapshot3DInfo = imp2.getSnapshot3DInfo
    getSnapshot3DInfo2 = imp7.getSnapshot3DInfo2
    saveSession = imp1.saveSession
    updateMarkup = imp1.updateMarkup
    updateSessionModel = imp1.updateSessionModel
    updateSnapshot3D = imp2.updateSnapshot3D
    updateSnapshot3DStructureFiles = imp2.updateSnapshot3DStructureFiles
    updateTwoDSnaphot = imp1.updateTwoDSnaphot
