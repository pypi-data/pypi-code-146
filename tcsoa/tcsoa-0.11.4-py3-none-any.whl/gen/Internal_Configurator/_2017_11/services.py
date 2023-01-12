from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0ConfiguratorPerspective
from tcsoa.gen.Internal.Configurator._2017_11.ConfiguratorManagement import ConfigurationSessionInfoInput, GetContextBasedVariantExprsResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getContextBasedVariantExpressions(cls, targetObjects: List[BusinessObject], perspective: Cfg0ConfiguratorPerspective) -> GetContextBasedVariantExprsResponse:
        """
        This operation returns the variant expressions associated with the given set of target objects based on the
        Configurator Perspective input which provides the Revision Rule and Configuration Context.
        
        Use cases:
        Use case 1 :
        User can get variant expressions of an existing object. For example 
        
        Create an instance of default rule (Cfg0DefaultRule) by using operation setVariantExpressions and set subject
        condition as "Color = Red". To retrieve this variant expression getContextBasedVariantExpressions   can be used
        which returns variant expression formula and the client representable structure format.
        
        Use case 2:
        If Option Value is not allocated in the input Configurator Context, only the Value text is returned in
        response, Option tag is empty. For Example,
        
        Create an instance of inclusion rule (Cfg0InclusionRule) under Context1 with following subject and
        applicability:
        Subject: Transmission = Manual (Manual is allocated to both Context1 and Context2)
        Applicability: Engine = V4 (V4 is allocated to only Context1)
        Now allocate the Inclusion Rule to Context2. Open Inclusion Rule from Context2 in Expression Editor. Option V4
        is shown as Read Only Text.
        """
        return cls.execute_soa_method(
            method_name='getContextBasedVariantExpressions',
            library='Internal-Configurator',
            service_date='2017_11',
            service_name='ConfiguratorManagement',
            params={'targetObjects': targetObjects, 'perspective': perspective},
            response_cls=GetContextBasedVariantExprsResponse,
        )

    @classmethod
    def setConfigurationSessionInfo(cls, inputs: List[ConfigurationSessionInfoInput]) -> ServiceData:
        """
        This operation attaches the configuration session information on the target objects. The information is
        extracted from the input perspective and the configuration profile parameters. The target objects must
        implement ConfigurationSession behavior. Please refer to the documentation of the business object to find out
        whether the object implements ConfigurationSession behavior. Also the input perspective should provide exactly
        one configurator context.
        
        Use cases:
        During Content Solve a user wants the Product Variability defined within the Configurator Context object to be
        honored. Call this service, pass the corresponding Cfg0ConfiguratorPerspective and Configuration Profile
        required for the Solve. This service will set this information on the target object and the same will be
        honored during Content Solve.
        """
        return cls.execute_soa_method(
            method_name='setConfigurationSessionInfo',
            library='Internal-Configurator',
            service_date='2017_11',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
