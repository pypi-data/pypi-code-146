from tcsoa.gen.ClassificationCommon._2020_01.services import ClassificationService as imp0
from tcsoa.gen.ClassificationCommon._2020_12.services import ClassificationService as imp1
from tcsoa.base import TcService


class ClassificationService(TcService):
    deleteClassificationObjects = imp0.deleteClassificationObjects
    getClassificationObjects = imp0.getClassificationObjects
    importClassificationDefinitions = imp1.importClassificationDefinitions
    saveClassificationObjects = imp0.saveClassificationObjects
    searchClassificationDefinitions = imp1.searchClassificationDefinitions
