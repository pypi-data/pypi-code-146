from tcsoa.gen.Classification._2009_10.services import ClassificationService as imp0
from tcsoa.gen.Classification._2016_03.services import ClassificationService as imp1
from tcsoa.gen.Classification._2007_01.services import ClassificationService as imp2
from tcsoa.gen.Classification._2011_06.services import ClassificationService as imp3
from tcsoa.gen.Classification._2016_09.services import ClassificationService as imp4
from tcsoa.gen.Classification._2015_10.services import ClassificationService as imp5
from tcsoa.gen.Classification._2011_12.services import ClassificationService as imp6
from tcsoa.gen.Classification._2015_03.services import ClassificationService as imp7
from tcsoa.base import TcService


class ClassificationService(TcService):
    autoComputeAttributes = imp0.autoComputeAttributes
    convertValues = imp1.convertValues
    createClassificationObjects = imp2.createClassificationObjects
    createOrUpdateKeyLOVs = imp0.createOrUpdateKeyLOVs
    deleteChildrenInHierarchy = imp3.deleteChildrenInHierarchy
    deleteClassificationObjects = imp2.deleteClassificationObjects
    findClassificationObjects = imp2.findClassificationObjects
    findClassifiedObjects = imp2.findClassifiedObjects
    findValues = imp4.findValues
    getAttributesForClasses = imp2.getAttributesForClasses
    getAttributesForClasses2 = imp0.getAttributesForClasses2
    getChildren = imp2.getChildren
    getChildrenExtended = imp1.getChildrenExtended
    getClassDefinitions = imp5.getClassDefinitions
    getClassDescriptions = imp2.getClassDescriptions
    getClassificationObjectInfo = imp6.getClassificationObjectInfo
    getClassificationObjects = imp2.getClassificationObjects
    getFileIds = imp2.getFileIds
    getKeyLOVs = imp2.getKeyLOVs
    getKeyLOVs2 = imp0.getKeyLOVs2
    getKeyLOVsForDependentAttributes = imp7.getKeyLOVsForDependentAttributes
    getLibraryHierarchy = imp3.getLibraryHierarchy
    getParents = imp2.getParents
    getPartFamilyTemplates = imp2.getPartFamilyTemplates
    search = imp2.search
    searchByInstanceId = imp2.searchByInstanceId
    searchClassesExtended = imp1.searchClassesExtended
    searchForClasses = imp2.searchForClasses
    updateClassificationObjects = imp2.updateClassificationObjects
