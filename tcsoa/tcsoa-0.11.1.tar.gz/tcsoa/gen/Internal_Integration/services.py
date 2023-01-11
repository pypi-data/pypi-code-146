from tcsoa.gen.Internal_Integration._2007_06.services import IntegrationManagementService as imp0
from tcsoa.gen.Internal_Integration._2008_06.services import IntegrationManagementService as imp1
from tcsoa.base import TcService


class IntegrationManagementService(TcService):
    connect = imp0.connect
    renameIMF = imp1.renameIMF
