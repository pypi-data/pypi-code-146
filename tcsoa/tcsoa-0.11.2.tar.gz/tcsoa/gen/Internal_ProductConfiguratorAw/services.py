from tcsoa.gen.Internal_ProductConfiguratorAw._2017_12.services import ConfiguratorManagementService as imp0
from tcsoa.gen.Internal_ProductConfiguratorAw._2020_05.services import ConfiguratorManagementService as imp1
from tcsoa.gen.Internal_ProductConfiguratorAw._2018_05.services import ConfiguratorManagementService as imp2
from tcsoa.gen.Internal_ProductConfiguratorAw._2020_12.services import ConfiguratorManagementService as imp3
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):
    createCustomVariantRule = imp0.createCustomVariantRule
    getConfiguratorDataHierarchy = imp1.getConfiguratorDataHierarchy
    getFilterPanelData = imp2.getFilterPanelData
    getVariantConfigurationData = imp0.getVariantConfigurationData
    getVariantExpressionData = imp2.getVariantExpressionData
    getVariantExpressionData2 = imp3.getVariantExpressionData2
    setVariantExpressionData = imp2.setVariantExpressionData
    setVariantExpressionData2 = imp3.setVariantExpressionData2
    validateProductConfigurations = imp2.validateProductConfigurations
    validateProductConfigurations2 = imp3.validateProductConfigurations2
    variantConfigurationView = imp2.variantConfigurationView
    variantConfigurationView2 = imp3.variantConfigurationView2
