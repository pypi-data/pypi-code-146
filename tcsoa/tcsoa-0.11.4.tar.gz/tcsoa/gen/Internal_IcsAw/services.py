from tcsoa.gen.Internal_IcsAw._2017_06.services import AuthorService as imp0
from tcsoa.gen.Internal_IcsAw._2018_05.services import ClassificationService as imp1
from tcsoa.gen.Internal_IcsAw._2018_12.services import ClassificationService as imp2
from tcsoa.gen.Internal_IcsAw._2019_12.services import ClassificationService as imp3
from tcsoa.gen.Internal_IcsAw._2017_12.services import AuthorService as imp4
from tcsoa.gen.Internal_IcsAw._2019_06.services import ClassificationService as imp5
from tcsoa.base import TcService


class AuthorService(TcService):
    createOrUpdateClassificationObjects = imp0.createOrUpdateClassificationObjects
    findClassifications = imp4.findClassifications


class ClassificationService(TcService):
    deleteClassificationObjects = imp1.deleteClassificationObjects
    findClassificationInfo = imp1.findClassificationInfo
    findClassificationInfo2 = imp2.findClassificationInfo2
    findClassificationInfo3 = imp3.findClassificationInfo3
    getClassificationCmdVisibilityInfo = imp5.getClassificationCmdVisibilityInfo
    saveClassificationObjects = imp1.saveClassificationObjects
    saveClassificationObjects2 = imp2.saveClassificationObjects2
