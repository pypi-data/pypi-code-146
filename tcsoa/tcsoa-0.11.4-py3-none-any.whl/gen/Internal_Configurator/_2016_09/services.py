from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2016_09.ConfiguratorManagement import AvailabilityOutput, AvailabilityInput
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getOptionValueAvailability(cls, input: AvailabilityInput) -> AvailabilityOutput:
        """
        This operation computes the available features within a set of requested families and models. The parameters
        criteriaExpression and familiesToTest are used to pass in the input expression representing a model and
        families of interest for which available features are requested. The operation response returns the available
        product variability for all the features in the requested families, if the features satisfy the input
        expression in criteriaExpression and the constraint(s) present in the system. The input parameter
        criteriaExpression is required to contain expression representing models. Iif they don't the the
        criteriaExpression is empty the operation throws an  error, . The input parameter familiesToTest is required to
        contain list of Family. If the requested family list is empty, the operation throws an error.
        
        Use cases:
        Consider the following Variability data in a Configurator Ccontext itemsay "MyProductItem":
        
        Model Family    Features
        M
        - m1
        - m2
        - m3
        
        
        
        Family    Features   
        A
        - a1
        - a2
        - a3
        
        
        
        B
        - b1
        - b2
        - b3
        
        
        
        C
        - c1
        - c2
        - c3
        
        
        
        Rules:
        - a1 is available with m1:  This is anavailability rule stating that the configuration feature a1 (of the
        family A) is available with the model m1 (of model family M).
        - a2 is available with m1:  This is an availability rule stating that the configuration feature a2 (of the
        family A) is available with the model m1 (of model family M).
        - b1 is available with m2:  This is an availability rule stating that the configuration feature b1 (of the
        family B) is available with the model m2 (of model family M).
        
        
        
        
        Use case 1:
        Operation getOptionValueAvailability is invoked with AvailabilityInput populated as:
        Configurator Context item = "MyProductItem"
        criteriaExpression = { M=m1}
        familiesToTest = {A}
        applyConstraints = 1(enable configurator constraint evaluation)
        
        Response -  
        For Model M1 - a1(Available ) , a2(Available ), a3( Not Available )
        
        Use case 2:
        Operation getOptionValueAvailability is invoked with AvailabilityInput populated as:
        Configurator Context item = "MyProductItem"
        CriteriaExpression = { M=m1, M=m2 }
        FamiliesToTest = { A,B }
        applyConstraints = 1
        
        Response - 
        For Model M1 - a1(Available ) , a2(Available ), a3( Not Available ), b1(Not Available) , b2(Not Available), b3(
        Not Available )
        For Model M2 - a1(Not Available) , a2(Not Available), a3( Not Available ), b1(Available) , b2(Not Available),
        b3( Not Available )
        
        Use case 3:
        Operation getOptionValueAvailability is invoked with AvailabilityInput populated as:
        Configurator Context item = "MyProductItem"
         CriteriaExpression = { M=m1, M=m2 }
        FamiliesToTest =  {}
        applyConstraints = 1
        
        Response - 
        The parameter serviceData will contain appropriate error(s), because familiesToTest is empty
        
        Use case 4:
        Operation getOptionValueAvailability is invoked with AvailabilityInput populated as:
        Configurator Context item = "MyProductItem"
         CriteriaExpression = { }
        FamiliesToTest = { A,B }
        applyConstraints = 1
        
        Response - 
        The parameter serviceData will contain  appropriate error(s), because CriteriaExpression is empty.
        """
        return cls.execute_soa_method(
            method_name='getOptionValueAvailability',
            library='Internal-Configurator',
            service_date='2016_09',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=AvailabilityOutput,
        )
