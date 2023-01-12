from tcsoa.gen.Internal_Classification._2020_04.services import ClassificationService as imp0
from tcsoa.gen.Internal_Classification._2017_05.services import ClassificationService as imp1
from tcsoa.gen.Internal_Classification._2009_10.services import ClassificationService as imp2
from tcsoa.gen.Internal_Classification._2018_11.services import ClassificationService as imp3
from tcsoa.base import TcService


class ClassificationService(TcService):
    findClassificationInfo = imp0.findClassificationInfo
    getClassDefinitionsNX = imp1.getClassDefinitionsNX
    getClassificationHierarchies = imp2.getClassificationHierarchies
    getClassificationProperties = imp2.getClassificationProperties
    saveClassificationObjects = imp3.saveClassificationObjects
