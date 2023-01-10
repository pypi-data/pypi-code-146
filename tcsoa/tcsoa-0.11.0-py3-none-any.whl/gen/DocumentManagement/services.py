from tcsoa.gen.DocumentManagement._2018_11.services import PrintOrRenderService as imp0
from tcsoa.gen.DocumentManagement._2010_04.services import DigitalSignatureService as imp1
from tcsoa.gen.DocumentManagement._2008_06.services import DocumentControlService as imp2
from tcsoa.gen.DocumentManagement._2010_04.services import LaunchDefinitionService as imp3
from tcsoa.gen.DocumentManagement._2013_12.services import PrintOrRenderService as imp4
from tcsoa.gen.DocumentManagement._2007_01.services import DocumentTemplateService as imp5
from tcsoa.gen.DocumentManagement._2011_06.services import AttributeExchangeService as imp6
from tcsoa.gen.DocumentManagement._2018_06.services import AttributeExchangeService as imp7
from tcsoa.base import TcService


class PrintOrRenderService(TcService):
    containsRenderableFiles = imp0.containsRenderableFiles
    getPrinterDefinitions = imp4.getPrinterDefinitions
    printSubmitRequest = imp4.printSubmitRequest
    renderFilesSubmitRequest = imp0.renderFilesSubmitRequest
    renderSubmitRequest = imp4.renderSubmitRequest


class DigitalSignatureService(TcService):
    digitalSigningSave = imp1.digitalSigningSave


class DocumentControlService(TcService):
    getAdditionalFilesForCheckin = imp2.getAdditionalFilesForCheckin
    getCheckinModeAndFiles = imp2.getCheckinModeAndFiles
    postCreate = imp2.postCreate


class LaunchDefinitionService(TcService):
    getLaunchDefinition = imp3.getLaunchDefinition


class DocumentTemplateService(TcService):
    getTemplates = imp5.getTemplates


class AttributeExchangeService(TcService):
    resolveAttrMappingsAndGetProperties = imp6.resolveAttrMappingsAndGetProperties
    resolveAttrMappingsAndSetProperties = imp6.resolveAttrMappingsAndSetProperties
    updateDocumentProperties = imp7.updateDocumentProperties
