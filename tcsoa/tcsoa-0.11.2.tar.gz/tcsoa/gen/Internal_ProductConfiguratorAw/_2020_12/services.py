from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Internal.ProductConfiguratorAw._2020_12.ConfiguratorManagement import SetVariantExpressionDataInput, ValidateProductConfigsInput, VariantConfigurationViewResponse2, VariantConfigurationViewIn2, VariantExpressionDataInput2, VariantExpressionDataResponse2, ValidateProductConfigsResponse2
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def variantConfigurationView2(cls, input: VariantConfigurationViewIn2) -> VariantConfigurationViewResponse2:
        """
        This operation retrieves variant configuration data available in the current Configurator Context
        required to create a custom variant rule.
        For a given Cfg0ConfiguratorPerspective and selected context or a seed variant rule, the following is retrieved:
        &bull;The valid selections for given groups by optionally applying constraints
        &bull;Violations and other indicators like incomplete, invalid, package.
        &bull;The payload that should be retained by the client for subsequent calls.
        """
        return cls.execute_soa_method(
            method_name='variantConfigurationView2',
            library='Internal-ProductConfiguratorAw',
            service_date='2020_12',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=VariantConfigurationViewResponse2,
        )

    @classmethod
    def getVariantExpressionData2(cls, variantExpressionDataInput: VariantExpressionDataInput2) -> VariantExpressionDataResponse2:
        """
        This operation returns the variant configuration expression data of the input objects.
        """
        return cls.execute_soa_method(
            method_name='getVariantExpressionData2',
            library='Internal-ProductConfiguratorAw',
            service_date='2020_12',
            service_name='ConfiguratorManagement',
            params={'variantExpressionDataInput': variantExpressionDataInput},
            response_cls=VariantExpressionDataResponse2,
        )

    @classmethod
    def setVariantExpressionData2(cls, input: SetVariantExpressionDataInput) -> ServiceData:
        """
        This operation sets the configuration expressions for the input business objects. The variant expressions can
        be set for variant conditions, rules and variant criteria.
        """
        return cls.execute_soa_method(
            method_name='setVariantExpressionData2',
            library='Internal-ProductConfiguratorAw',
            service_date='2020_12',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def validateProductConfigurations2(cls, validateProductConfigsInput: ValidateProductConfigsInput) -> ValidateProductConfigsResponse2:
        """
        This operation validates the input selections by applying the constraint rules such as inclusion rule, 
        exclusion rule or feasibility rule for the input configurator perspective.
        
        The operation also returns validation status, violations and selections by considering input selections and the
        rules in the context. The response parameter criteriaStatus conveys the information about the status of the
        configuration which is either valid or invalid. The parameter valueToViolationsMap represents map of values
        having voilations. Each value in this map have list of vloilations.
        
        Exceptions:
        >The following error code may be returned:
        77073    The operation has failed, because an invalid Configurator Perspective was passed.
        77074    The operation must contain a product item in the Configurator Perspective.
        256054 The value for the applyConstraints bit pattern is invalid.
        77146    The operation has failed, because invalid key/value is passed in requestInfo.
        """
        return cls.execute_soa_method(
            method_name='validateProductConfigurations2',
            library='Internal-ProductConfiguratorAw',
            service_date='2020_12',
            service_name='ConfiguratorManagement',
            params={'validateProductConfigsInput': validateProductConfigsInput},
            response_cls=ValidateProductConfigsResponse2,
        )
