from __future__ import annotations

from tcsoa.gen.BusinessObjects import VariantRule, Cfg0ConfiguratorPerspective
from tcsoa.gen.Internal.ProductConfiguratorAw._2017_12.ConfiguratorManagement import CreateCustomVariantRuleResponse, VariantConfigurationDataResponse, UserSelectionMap, VariantConfigurationDataInput
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def createCustomVariantRule(cls, configPerspective: Cfg0ConfiguratorPerspective, userSelections: UserSelectionMap, guidedConfigurationMode: bool, variantRule: VariantRule) -> CreateCustomVariantRuleResponse:
        """
        This operation creates adhoc Variant Rule using user selections. An adhoc Variant Rule is purgable by
        purge_adhoc_configuration_contexts utility if referenced by adhoc configuration context (ConfigurationContext)
        
        Exceptions:
        >The following service exception may be returned:
        - 333005 Failed to create Variant Rule. 
        - 333006 configPerspective is null.
        
        """
        return cls.execute_soa_method(
            method_name='createCustomVariantRule',
            library='Internal-ProductConfiguratorAw',
            service_date='2017_12',
            service_name='ConfiguratorManagement',
            params={'configPerspective': configPerspective, 'userSelections': userSelections, 'guidedConfigurationMode': guidedConfigurationMode, 'variantRule': variantRule},
            response_cls=CreateCustomVariantRuleResponse,
        )

    @classmethod
    def getVariantConfigurationData(cls, input: VariantConfigurationDataInput) -> VariantConfigurationDataResponse:
        """
        This operation retrieves variant configuration data required to create a custom variant rule.
        For a given Configurator Context with a list of current variant option selections or a seed variant rule, the
        following is retrieved:
        - The valid selections for the given group by optionally applying constraints
        - All variant option groups available in this Configurator Context
        
        
        
        Exceptions:
        >The following service exception may be returned.
        
        '77073' The operation has failed, because an invalid Configurator Perspective was passed.
        '77074' The operation must contain a product item in the Configurator Perspective.
        '333001' The variant configuration cannot be performed because both the configuration context and the
        configuration perspective must be provided.
        '333002' Configurator context is not found for input selected object.
        """
        return cls.execute_soa_method(
            method_name='getVariantConfigurationData',
            library='Internal-ProductConfiguratorAw',
            service_date='2017_12',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=VariantConfigurationDataResponse,
        )
