from tcsoa.gen.ConfigFilterCriteria._2011_06.services import EffectivityManagementService as imp0
from tcsoa.gen.ConfigFilterCriteria._2013_05.services import EffectivityManagementService as imp1
from tcsoa.gen.ConfigFilterCriteria._2017_05.services import EffectivityManagementService as imp2
from tcsoa.gen.ConfigFilterCriteria._2013_05.services import VariantManagementService as imp3
from tcsoa.base import TcService


class EffectivityManagementService(TcService):
    convertEffectivityExpressions = imp0.convertEffectivityExpressions
    convertEffectivityTables = imp0.convertEffectivityTables
    getAvailableProductEffectivity = imp0.getAvailableProductEffectivity
    getConfigurableProducts = imp0.getConfigurableProducts
    getEffectivityConditions = imp0.getEffectivityConditions
    getEffectivityDisplayString = imp1.getEffectivityDisplayString
    getEffectivityExpressions = imp0.getEffectivityExpressions
    getEffectivityOverlapStates = imp1.getEffectivityOverlapStates
    getEffectivitySubsetTables = imp2.getEffectivitySubsetTables
    getEffectivityTables = imp0.getEffectivityTables
    getRevRuleEffectivityCriteria = imp0.getRevRuleEffectivityCriteria
    setEffectivityConditionSubsets = imp2.setEffectivityConditionSubsets
    setEffectivityConditions = imp0.setEffectivityConditions
    setRevRuleEffectivityCriteria = imp0.setRevRuleEffectivityCriteria


class VariantManagementService(TcService):
    getProductConfigurations = imp3.getProductConfigurations
