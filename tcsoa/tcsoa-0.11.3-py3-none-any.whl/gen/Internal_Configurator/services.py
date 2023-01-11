from tcsoa.gen.Internal_Configurator._2015_10.services import ConfiguratorManagementService as imp0
from tcsoa.gen.Internal_Configurator._2014_06.services import ConfiguratorManagementService as imp1
from tcsoa.gen.Internal_Configurator._2015_03.services import ConfiguratorManagementService as imp2
from tcsoa.gen.Internal_Configurator._2018_11.services import ConfiguratorManagementService as imp3
from tcsoa.gen.Internal_Configurator._2018_06.services import ConfiguratorManagementService as imp4
from tcsoa.gen.Internal_Configurator._2017_11.services import ConfiguratorManagementService as imp5
from tcsoa.gen.Internal_Configurator._2014_12.services import ConfiguratorManagementService as imp6
from tcsoa.gen.Internal_Configurator._2016_09.services import ConfiguratorManagementService as imp7
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):
    convertVariantExpressions = imp0.convertVariantExpressions
    createUpdateVariantRules = imp1.createUpdateVariantRules
    executeSearch = imp1.executeSearch
    fetchNextSearchResults = imp1.fetchNextSearchResults
    getAvailableProductVariability = imp2.getAvailableProductVariability
    getAvailableProductVariability2 = imp0.getAvailableProductVariability
    getConfigurationRosterCoverage = imp3.getConfigurationRosterCoverage
    getConfigurationSessionInfo = imp4.getConfigurationSessionInfo
    getContextBasedVariantExpressions = imp5.getContextBasedVariantExpressions
    getDefaultRules = imp1.getDefaultRules
    getExcludeRules = imp1.getExcludeRules
    getFamilyGroups = imp1.getFamilyGroups
    getIncludeRules = imp1.getIncludeRules
    getModelAndOptionConditions = imp6.getModelAndOptionConditions
    getModelsForProduct = imp1.getModelsForProduct
    getOptionFamilies = imp1.getOptionFamilies
    getOptionValueAvailability = imp7.getOptionValueAvailability
    getOptionValues = imp1.getOptionValues
    getOverlapStates = imp6.getOverlapStates
    getProductDefaults = imp1.getProductDefaults
    getProductDefaults2 = imp0.getProductDefaults
    getRevRulesForConfiguratorContext = imp0.getRevRulesForConfiguratorContext
    getVariability = imp4.getVariability
    getVariantCache = imp1.getVariantCache
    getVariantExpressionDisplayStrings = imp1.getVariantExpressionDisplayStrings
    getVariantExpressions = imp0.getVariantExpressions
    setConfigurationSessionInfo = imp5.setConfigurationSessionInfo
    setVariantExpressions = imp0.setVariantExpressions
    stopSearch = imp1.stopSearch
    updateAdmissibility = imp6.updateAdmissibility
    validateProductConditions = imp4.validateProductConditions
    validateProductConfiguration = imp1.validateProductConfiguration
    validateProductConfiguration2 = imp0.validateProductConfiguration
