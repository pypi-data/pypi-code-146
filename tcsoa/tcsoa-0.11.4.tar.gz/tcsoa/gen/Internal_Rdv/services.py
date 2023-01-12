from tcsoa.gen.Internal_Rdv._2009_01.services import VariantManagementService as imp0
from tcsoa.gen.Internal_Rdv._2010_04.services import VariantManagementService as imp1
from tcsoa.gen.Internal_Rdv._2009_04.services import VariantManagementService as imp2
from tcsoa.gen.Internal_Rdv._2009_05.services import VariantManagementService as imp3
from tcsoa.gen.Internal_Rdv._2008_03.services import VariantManagementService as imp4
from tcsoa.gen.Internal_Rdv._2007_06.services import VariantManagementService as imp5
from tcsoa.gen.Internal_Rdv._2007_09.services import VariantManagementService as imp6
from tcsoa.base import TcService


class VariantManagementService(TcService):
    addDesignToProduct = imp0.addDesignToProduct
    addPartToProduct = imp1.addPartToProduct
    applyNVEMetaExpression = imp0.applyNVEMetaExpression
    askNVEMetaExpression = imp0.askNVEMetaExpression
    createMultipleNamedVariantExpressions = imp2.createMultipleNamedVariantExpressions
    createSavedVariantRules = imp2.createSavedVariantRules
    deleteMultipleNamedVariantExpressions = imp2.deleteMultipleNamedVariantExpressions
    executeAdhocSearchWithOverlays = imp3.executeAdhocSearchWithOverlays
    executeSearchWithOverlays = imp3.executeSearchWithOverlays
    getApnComponents = imp0.getApnComponents
    getArchbreakdownBomlineChildComponents = imp0.getArchbreakdownBomlineChildComponents
    getArchbreakdownMeapnChildComponents = imp0.getArchbreakdownMeapnChildComponents
    getValidBackgroundOverlays = imp1.getValidBackgroundOverlays
    getValidoverlayBomlinesInfo = imp4.getValidoverlayBomlinesInfo
    getVariabilityInfo = imp5.getVariabilityInfo
    getVariantExprXOChartData = imp6.getVariantExprXOChartData
    realignNVEMetaExpressionTokens = imp3.realignNVEMetaExpressionTokens
    reapplyNVEMetaExpressions = imp0.reapplyNVEMetaExpressions
    replaceDesignInProduct = imp0.replaceDesignInProduct
    replacePartInProduct = imp1.replacePartInProduct
    validateNVEMetaExpressions = imp0.validateNVEMetaExpressions
