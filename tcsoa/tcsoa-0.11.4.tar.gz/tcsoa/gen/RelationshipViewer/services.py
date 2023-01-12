from tcsoa.gen.RelationshipViewer._2012_10.services import NetworkEngineService as imp0
from tcsoa.gen.RelationshipViewer._2014_11.services import NetworkEngineService as imp1
from tcsoa.gen.RelationshipViewer._2019_12.services import NetworkEngineService as imp2
from tcsoa.base import TcService


class NetworkEngineService(TcService):
    createRelations = imp0.createRelations
    getGraphStyleDef = imp0.getGraphStyleDef
    getViews = imp0.getViews
    getViews2 = imp0.getViews2
    getViews3 = imp1.getViews3
    getViews4 = imp2.getViews4
    queryNetwork = imp0.queryNetwork
    queryNetwork2 = imp0.queryNetwork2
