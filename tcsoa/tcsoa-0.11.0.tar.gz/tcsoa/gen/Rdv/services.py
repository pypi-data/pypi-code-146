from tcsoa.gen.Rdv._2008_05.services import ContextManagementService as imp0
from tcsoa.gen.Rdv._2012_09.services import ContextManagementService as imp1
from tcsoa.gen.Rdv._2010_09.services import ContextManagementService as imp2
from tcsoa.gen.Rdv._2009_04.services import ContextManagementService as imp3
from tcsoa.gen.Rdv._2013_05.services import ContextManagementService as imp4
from tcsoa.base import TcService


class ContextManagementService(TcService):
    addPartToProduct = imp0.addPartToProduct
    createFormAttrSearchCriteria = imp1.createFormAttrSearchCriteria
    createSCO = imp2.createSCO
    createSearchCriteriaScope = imp1.createSearchCriteriaScope
    createSearchSCO = imp1.createSearchSCO
    getAllGOPartSolutions = imp3.getAllGOPartSolutions
    getICSClassNames = imp1.getICSClassNames
    getPastePrimeAttributes = imp3.getPastePrimeAttributes
    getProductItemInfo = imp0.getProductItemInfo
    getRelatedObjectsInContext = imp4.getRelatedObjectsInContext
    removePartsRelatedToABE = imp0.removePartsRelatedToABE
    replacePartInProduct = imp0.replacePartInProduct
    updateSCO = imp2.updateSCO
    updateSearchSCO = imp1.updateSearchSCO
