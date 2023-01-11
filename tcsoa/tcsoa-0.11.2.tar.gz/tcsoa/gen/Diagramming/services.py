from tcsoa.gen.Diagramming._2014_06.services import DNDManagementService as imp0
from tcsoa.gen.Diagramming._2011_06.services import DiagramManagementService as imp1
from tcsoa.gen.Diagramming._2012_09.services import DiagramManagementService as imp2
from tcsoa.base import TcService


class DNDManagementService(TcService):
    createAndPaste = imp0.createAndPaste
    createConnectionPortsAndConnect = imp0.createConnectionPortsAndConnect


class DiagramManagementService(TcService):
    createDiagram = imp1.createDiagram
    createOrUpdateTemplate = imp1.createOrUpdateTemplate
    createOrUpdateTemplate2 = imp2.createOrUpdateTemplate
    getDiagramMembers = imp1.getDiagramMembers
    openDiagram = imp1.openDiagram
    saveDiagram = imp1.saveDiagram
