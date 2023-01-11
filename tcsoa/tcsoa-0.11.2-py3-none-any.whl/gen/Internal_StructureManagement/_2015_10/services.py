from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Internal.StructureManagement._2015_10.VariantManagement import VariantConfigurationCriteria


class VariantManagementService(TcService):

    @classmethod
    def applyVariantConfiguration(cls, window: BOMWindow, variantConfigurationCriteria: VariantConfigurationCriteria) -> ServiceData:
        """
        The applyVariantConfiguration operation configures  the Product Structure in the window by input formula or
        variant rule. The value of PSM_enable_product_configurator  preference must be true for successful completion
        of this operation.
        
        Use cases:
        Use Case 1:  Configure the window by applying formula or variant rule-  
        
        You can get formula from getVariantExpressions operation or can pass it in the following format -
        "[FamilyNamespace]FamilyName=FamilyValue. For example [Teamcenter]Color = red | [Teamcenter]Color = blue". This
        will configure the window accordingly or you can configure the window using variant rule created in Product
        Configurator application. 
        
         
        
        Use Case 2:  Configure the window by applying formula or variant rule with defaults and rule checks  - 
        
        To fully configure the BOMWindow for variants, you need to evaluate defaults and rule checks which can be done
        via below operations. You can extract variant criteria as formula string from either getProductDefaults or from
        validateProductConfiguration depending on the requirement. Typically getProductDefaults and
        validateProductConfiguariton in sequence and can pass final variant criteria as input for
        applyVariantConfiguartion.
        
        
        Order of service operation calls -
        - getVariantExpression
        - getProductDefaults
        - validateProductConfiguration
        - applyVariantConfiguration
        
        """
        return cls.execute_soa_method(
            method_name='applyVariantConfiguration',
            library='Internal-StructureManagement',
            service_date='2015_10',
            service_name='VariantManagement',
            params={'window': window, 'variantConfigurationCriteria': variantConfigurationCriteria},
            response_cls=ServiceData,
        )
