from tcsoa.gen.Internal_ActiveWorkspaceVis._2015_03.services import MassiveModelVisualizationService as imp0
from tcsoa.gen.Internal_ActiveWorkspaceVis._2018_05.services import MassiveModelVisualizationService as imp1
from tcsoa.gen.Internal_ActiveWorkspaceVis._2014_11.services import OccurrenceManagementService as imp2
from tcsoa.base import TcService


class MassiveModelVisualizationService(TcService):
    getIndexedProducts = imp0.getIndexedProducts
    getStructureFiles = imp0.getStructureFiles
    getStructureIdFromRecipe = imp0.getStructureIdFromRecipe
    getStructureIdFromRecipe2 = imp1.getStructureIdFromRecipe2
    groupOccurrencesByProperties = imp0.groupOccurrencesByProperties
    updateDeltaCollection = imp0.updateDeltaCollection


class OccurrenceManagementService(TcService):
    getVisBookmarkInfo = imp2.getVisBookmarkInfo
    saveVisBookmarkInfo = imp2.saveVisBookmarkInfo
