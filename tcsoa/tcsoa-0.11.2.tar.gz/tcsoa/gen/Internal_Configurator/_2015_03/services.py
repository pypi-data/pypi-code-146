from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2015_03.ConfiguratorManagement import AvailableProductVariabilityInput, AvailableProductVariabilityOutput
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getAvailableProductVariability(cls, input: AvailableProductVariabilityInput) -> AvailableProductVariabilityOutput:
        """
        This operation computes the available features within a set of requested families. The parameters
        criteriaExpression and familiesToTest are used to pass in the input expression and families of interest
        requesting the available features. The operation in response returns the available product variability for the
        requested families satisfying the input expression in criteriaExpression and the constraint(s) present in the
        system. If the input parameter criteriaExpression is empty, then the response will return the product
        variability for the requested families satisfying all the system constraints. If the requested family list is
        empty, the operation will not return any variability information.
        
        Use cases:
        Consider the following Variability data in a Configurator context say MyProductItem:
        
        Family      Fetures
        A
                A1
                A2
                A3
        
        B
                B1
                B2
                B3
        
        C
                C1
                C2
                C3
        
        Rules:
            A3 Includes B2:  This is an inclusion rule stating that if the configuration has the feature A3 (of the
        family A) then include the feature B2 as well (of the family B).
        B2 Excludes C2:  This is an exclusion rule state that if the configuration has the feature B2 (of the family B)
        then exclude/remove the feature C2 (of the family C)
        
        Use case 1:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        CriteriaExpression = {}
        familiesToTest = {A, B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1(enable configurator constraint evaluation)
        
        Response would contain - A1, A2, A3, B1, B2, B3, C1, C2 &amp; C3
        
        Use case 2:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        CriteriaExpression = {A=A3}
        FamiliesToTest = {B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1
        
        Response would - B2, C1 &amp; C3
        
        Use case 3:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        criteriaExpression = {A=A1}
        FamiliesToTest = {B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1
        
        Response would - B1, B2, B3, C1, C2 &amp; C3
        
        
        Use case 4:
        Initialize a variant criteria dialog for a new VariantRule in the Configurator context MyProductItem:
        The application uses operation getAvailableProductVariability with AvailableProductVariabilityInput populated
        as below:
        criteriaExpression = {}
        familiesToTest = {}
        context containing reference to Item MyProductItem
        ApplyConstraints = 0
        
        A service exception will be thrown by the  getAvailableProductVariability operation as familiesToTest is empty.
        """
        return cls.execute_soa_method(
            method_name='getAvailableProductVariability',
            library='Internal-Configurator',
            service_date='2015_03',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=AvailableProductVariabilityOutput,
        )
