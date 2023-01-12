from tcsoa.gen.Internal_DocMgmtAw._2019_06.services import DocMgmtService as imp0
from tcsoa.gen.Internal_DocMgmtAw._2019_12.services import DocMgmtService as imp1
from tcsoa.base import TcService


class DocMgmtService(TcService):
    processMarkups = imp0.processMarkups
    processTextDataset = imp1.processTextDataset
