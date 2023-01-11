from tcsoa.gen.Internal_Ai._2008_06.services import AiService as imp0
from tcsoa.gen.Internal_Ai._2016_03.services import AiService as imp1
from tcsoa.gen.Internal_Ai._2016_04.services import AiService as imp2
from tcsoa.base import TcService


class AiService(TcService):
    beginGenerateMonolithicJt = imp0.beginGenerateMonolithicJt
    endGenerateMonolithicJt = imp0.endGenerateMonolithicJt
    getApplicationInterfaceTypes = imp1.getApplicationInterfaceTypes
    invoke = imp0.invoke
    invoke2 = imp2.invoke2
