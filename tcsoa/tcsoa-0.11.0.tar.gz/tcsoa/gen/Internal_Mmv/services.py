from tcsoa.gen.Internal_Mmv._2012_09.services import SpatialStructureManagementService as imp0
from tcsoa.base import TcService


class SpatialStructureManagementService(TcService):
    acquireSpatialHierarchy = imp0.acquireSpatialHierarchy
    createMmvCursor = imp0.createMmvCursor
    getNodeBBox = imp0.getNodeBBox
    getSpatialCellsReadTickets = imp0.getSpatialCellsReadTickets
    isSpatialHierarchyLatest = imp0.isSpatialHierarchyLatest
    releaseMmvCursor = imp0.releaseMmvCursor
    releaseSpatialHierarchy = imp0.releaseSpatialHierarchy
