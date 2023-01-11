from tcsoa.gen.EditContext._2015_07.services import DataManagementService as imp0
from tcsoa.gen.EditContext._2016_04.services import DataManagementService as imp1
from tcsoa.gen.EditContext._2016_10.services import DataManagementService as imp2
from tcsoa.gen.EditContext._2014_12.services import DataManagementService as imp3
from tcsoa.base import TcService


class DataManagementService(TcService):
    getReferencerEditContexts = imp0.getReferencerEditContexts
    setChangeContext = imp1.setChangeContext
    setChangeContext2 = imp2.setChangeContext2
    setEditContext = imp3.setEditContext
