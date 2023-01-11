from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0ConfiguratorPerspective
from tcsoa.gen.Internal.ProductConfiguratorAw._2018_05.ConfiguratorManagement import SelectedExpression, VariantConfigurationViewResponse, FilterPanelDataResponse, VariantExpressionDataResponse, VariantExpressionDataInput, VariantConfigurationViewIn, ValidateProductConfigResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def variantConfigurationView(cls, input: VariantConfigurationViewIn) -> VariantConfigurationViewResponse:
        """
        This operation retrieves variant configuration data required to create a custom variant rule.
        For a given Cfg0ConfiguratorPerspective and selected context or a seed variant rule, the following is retrieved:
        &bull;The valid selections for given groups by optionally applying constraints
        &bull;All scope objects (Cfg0AbsFamilyGroup, Ptn0Partition) available in the current Configurator Context
        &bull;Violations and other indicators like incomplete, invalid, package.
        &bull;The payload that should be retained by the client for subsequent calls.
        """
        return cls.execute_soa_method(
            method_name='variantConfigurationView',
            library='Internal-ProductConfiguratorAw',
            service_date='2018_05',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=VariantConfigurationViewResponse,
        )

    @classmethod
    def getFilterPanelData(cls, selectedObject: BusinessObject) -> FilterPanelDataResponse:
        """
        This operation returns the filter panel data which is necessary to render filter panel on the client.
        
        Exceptions:
        >The following service exception may be returned.
        
        333003 No callback is registered to retrieve the configurator context for Business Objects of the given type.
        333008 Only objects of type Awb0Element and its subtypes are supported.
        """
        return cls.execute_soa_method(
            method_name='getFilterPanelData',
            library='Internal-ProductConfiguratorAw',
            service_date='2018_05',
            service_name='ConfiguratorManagement',
            params={'selectedObject': selectedObject},
            response_cls=FilterPanelDataResponse,
        )

    @classmethod
    def getVariantExpressionData(cls, variantExpressionDataInput: VariantExpressionDataInput) -> VariantExpressionDataResponse:
        """
        This operation returns the variant configuration expression data of the input objects.
        """
        return cls.execute_soa_method(
            method_name='getVariantExpressionData',
            library='Internal-ProductConfiguratorAw',
            service_date='2018_05',
            service_name='ConfiguratorManagement',
            params={'variantExpressionDataInput': variantExpressionDataInput},
            response_cls=VariantExpressionDataResponse,
        )

    @classmethod
    def setVariantExpressionData(cls, selectedExpressions: List[SelectedExpression], configPerspective: Cfg0ConfiguratorPerspective) -> ServiceData:
        """
        This operation sets the configuration expressions for the input business objects. The variant expressions can
        be set for variant conditions, rules and variant criteria.
        """
        return cls.execute_soa_method(
            method_name='setVariantExpressionData',
            library='Internal-ProductConfiguratorAw',
            service_date='2018_05',
            service_name='ConfiguratorManagement',
            params={'selectedExpressions': selectedExpressions, 'configPerspective': configPerspective},
            response_cls=ServiceData,
        )

    @classmethod
    def validateProductConfigurations(cls, configPerspective: Cfg0ConfiguratorPerspective, applyConstraints: int, selectedExpressions: List[SelectedExpression]) -> ValidateProductConfigResponse:
        """
        This operation validates the input selections by applying the constraint rules such as inclusion rule, 
        exclusion rule or feasibility rule for the input configurator perspective.
        The operation also returns validation status, violations and selections by considering input selections and the
        rules in the context. The response parameter 'criteriaStatus' conveys the information about the status of the
        configuration which is either valid or invalid. The parameter 'valueToViolationsMap' represents map of values
        having voilations. Each value in this map have list of vloilations. The paramter 'UserSelectionMap2' conveys
        the information about family to option values. This map contains entries accordance with the given input
        selections and the rules in the context.
        
        Exceptions:
        >The following service exception may be returned.
        
        77073     The operation has failed, because an invalid Configurator Perspective was passed.
        77074     The operation must contain a product item in the Configurator Perspective.
        256054   The value for the applyConstraints bit pattern is invalid.
        """
        return cls.execute_soa_method(
            method_name='validateProductConfigurations',
            library='Internal-ProductConfiguratorAw',
            service_date='2018_05',
            service_name='ConfiguratorManagement',
            params={'configPerspective': configPerspective, 'applyConstraints': applyConstraints, 'selectedExpressions': selectedExpressions},
            response_cls=ValidateProductConfigResponse,
        )
