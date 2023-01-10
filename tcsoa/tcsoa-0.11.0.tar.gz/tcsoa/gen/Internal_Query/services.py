from tcsoa.gen.Internal_Query._2012_02.services import SavedQueryService as imp0
from tcsoa.gen.Internal_Query._2013_05.services import SavedQueryService as imp1
from tcsoa.gen.Internal_Query._2014_10.services import SavedQueryService as imp2
from tcsoa.gen.Internal_Query._2008_06.services import FinderService as imp3
from tcsoa.base import TcService


class SavedQueryService(TcService):
    describeSavedQueryDefinitions = imp0.describeSavedQueryDefinitions
    describeSavedQueryDefinitions2 = imp1.describeSavedQueryDefinitions2
    describeSavedQueryDefinitions3 = imp2.describeSavedQueryDefinitions3


class FinderService(TcService):
    findObjectsByClassAndAttributes = imp3.findObjectsByClassAndAttributes
