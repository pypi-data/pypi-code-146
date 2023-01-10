from tcsoa.gen.Bom._2008_06.services import StructureManagementService as imp0
from tcsoa.gen.Bom._2010_09.services import StructureManagementService as imp1
from tcsoa.base import TcService


class StructureManagementService(TcService):
    addOrUpdateChildrenToParentLine = imp0.addOrUpdateChildrenToParentLine
    createBaseline = imp0.createBaseline
    getTraversedObjectsByRule = imp1.getTraversedObjectsByRule
    removeChildrenFromParentLine = imp0.removeChildrenFromParentLine
    verifyObjectCoverageByRule = imp1.verifyObjectCoverageByRule
