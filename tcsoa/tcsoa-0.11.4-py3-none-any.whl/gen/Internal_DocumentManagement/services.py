from tcsoa.gen.Internal_DocumentManagement._2013_05.services import DigitalSignatureService as imp0
from tcsoa.gen.Internal_DocumentManagement._2008_06.services import DispatcherManagementService as imp1
from tcsoa.gen.Internal_DocumentManagement._2008_06.services import DocumentControlService as imp2
from tcsoa.gen.Internal_DocumentManagement._2013_12.services import MarkupService as imp3
from tcsoa.gen.Internal_DocumentManagement._2020_12.services import AttributeExchangeService as imp4
from tcsoa.base import TcService


class DigitalSignatureService(TcService):
    cancelSign = imp0.cancelSign
    digitalSigningSaveTool = imp0.digitalSigningSaveTool
    isCheckOutForSign = imp0.isCheckOutForSign


class DispatcherManagementService(TcService):
    getConfigurations = imp1.getConfigurations


class DocumentControlService(TcService):
    getIRDCs = imp2.getIRDCs


class MarkupService(TcService):
    loadMarkups = imp3.loadMarkups
    saveMarkups = imp3.saveMarkups


class AttributeExchangeService(TcService):
    processAttrExchangeConfigurations = imp4.processAttrExchangeConfigurations
