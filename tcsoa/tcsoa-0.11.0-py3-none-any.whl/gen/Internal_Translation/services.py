from tcsoa.gen.Internal_Translation._2007_06.services import TranslationManagementService as imp0
from tcsoa.base import TcService


class TranslationManagementService(TcService):
    createDatasetOfVersion = imp0.createDatasetOfVersion
    insertDatasetVersion = imp0.insertDatasetVersion
    queryTranslationRequests = imp0.queryTranslationRequests
    updateTranslationRequest = imp0.updateTranslationRequest
