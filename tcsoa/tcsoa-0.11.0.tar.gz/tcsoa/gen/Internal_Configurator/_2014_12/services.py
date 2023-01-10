from __future__ import annotations

from tcsoa.gen.BusinessObjects import Cfg0ConfiguratorPerspective
from tcsoa.gen.Configurator._2014_12.ConfiguratorManagement import GetAdmissibilityResponse
from tcsoa.gen.Internal.Configurator._2014_12.ConfiguratorManagement import GetModelOptionCondInput, OverlapStateResponse, UpdateAdmissibilityInputList, OverlapStateInput, GetModelOptionCondResponse
from typing import List
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getModelAndOptionConditions(cls, operationConfigPerspective: Cfg0ConfiguratorPerspective, inputStructs: List[GetModelOptionCondInput]) -> GetModelOptionCondResponse:
        """
        This operation splits the given input expressions into the list of model and option condition expressions.
        The business object type of the Cfg0AbsValue value objects, with which the input expressions are formed,
        divides these values into a set of Cfg0AbsModel objects and a set of Cfg0AbsOptionValue objects. This operation
        decomposes each input expression into a two lists. One expression list that is formed exclusively with
        Cfg0AbsModel objects and other expression list that is formed exclusively with Cfg0AbsOptionValue objects.
        
        Use cases:
        Input expression will be spitted into model and option condition expressions.
        Use Case1: 
        Example: Input expression - "Model=m1 OR Model=m2 AND Engine=e1" is decomposed into 2 lists with 2 elements
        each. 
        The model expression list will contain: modelExpressions[0]="Model=m1" 
                                                                         modelExpressions[1]= "Model=m2". 
        The option condition list will contain: optionConditions[0]= "" (an empty expression representing the Boolean  
                      constant TRUE)                                      
                                                                        optionConditions[1]="Engine=e1". 
        ORing the AND combinations of each model expression with the option condition at the same index forms an
        expression that is logically equivalent to the input expression:
        ModelExpression[0] &amp; OptionCondition[0] | ModelExpression[1] &amp; OptionCondition[1] == InputExpression
        Use Case2:
        Example: InputExpression= "OF1 = V1 AND (ModelFamily = M1 OR ModelFamily = M3) AND OF3 = V3)"
        The Output will contain two list corresponding to the input expression. One list will correspond to the model
        expression and the other list will correspond to the option condition expression.
        ModelExpression will contain:  modelExpressions[0]="ModelFamily=M1"
                                                               modelExpressions[1]="ModelFamily=M3"
        Variant condition list will contain: optionConditions[0]= " OF1=V1 &amp; OF3=V3"
                                                                  optionConditions[1]= " OF1=V1 &amp; OF3=V3"
        
        Exceptions:
        >The operation will return a ServiceException if an unknown error occurs. A possible source for unknown errors
        could be a codeful configurator component customization.
        """
        return cls.execute_soa_method(
            method_name='getModelAndOptionConditions',
            library='Internal-Configurator',
            service_date='2014_12',
            service_name='ConfiguratorManagement',
            params={'operationConfigPerspective': operationConfigPerspective, 'inputStructs': inputStructs},
            response_cls=GetModelOptionCondResponse,
        )

    @classmethod
    def getOverlapStates(cls, context: Cfg0ConfiguratorPerspective, overlapStateInputs: List[OverlapStateInput]) -> OverlapStateResponse:
        """
        This operation determines and returns the degree of overlap between a set of configuration expressions and a
        reference configuration expression.
        
        Use cases:
        An application wants to qualify variant conditions that were retrieved with getVariantExpressions as to whether
        the condition is equal to, intersects with, or is a subset or superset of the variant criteria associated with
        the currently active variant configuration criteria (VariantRule). This cannot be achieved with properties on
        variant conditions or VariantRules because the result depends on the combination of a variant condition and the
        variant configuration criteria on a VariantRule. One and the same condition may have different overlap states
        with different VariantRules.
        The application calls getOverlapStates and passes the variant criteria (as obtained from a VariantRule using
        getVariantExpressions) as referenceExpression, and the variant conditions (as obtained from a set of product
        data elements using getVariantExpressions) as expressions.
        """
        return cls.execute_soa_method(
            method_name='getOverlapStates',
            library='Internal-Configurator',
            service_date='2014_12',
            service_name='ConfiguratorManagement',
            params={'context': context, 'overlapStateInputs': overlapStateInputs},
            response_cls=OverlapStateResponse,
        )

    @classmethod
    def updateAdmissibility(cls, updateAdmissibilityInputList: List[UpdateAdmissibilityInputList]) -> GetAdmissibilityResponse:
        """
        This operation updates the admissibility state for the families in context of the input context object. The
        admissibility of a target object such as family is defined as whether that target object is available or not
        available for the given context object such as partition..:
        The instance of Cfg0AbsAdmissibility object represents the relation and state between a configurator specific
        object and a non-configurator specific object. For example, the pair of a partition and a family is associated
        with state "Available". This operation will help to update the state for this pair to "Not Available".
        If the input state provided is blank then this operation will delete the corresponding Cfg0AbsAdmissibility
        object and related objects such as Cfg0AbsAdmissibilityThread.
        
        Use cases:
        This operation can be used to update admissibility for the families for the given business object.
         
        Consider that following set data-
        
        Engine-Box (A Family Group) - It has families "Engine" and "Transmission". 
        1. Engine- Petrol, Diesel
        2. Transmission - Manual, Auto
        Wheel (An Option Family Group) - It has families "Wheel-drive" and "Suspension".
        1. Wheel-drive - 2-Wheels, 4-Wheels
        2. Suspension - Full-Thrust, Full-Boom
        For the Engine partition instance, the families Engine and Transmission are "Available" while the families
        Wheel-drive and Suspension are "Not Available".
        If user wants to update the admissibility of Wheel-drive for Engine Partition as "Available" then using
        updateAdmissibility operation the admissibility state can be updated.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='updateAdmissibility',
            library='Internal-Configurator',
            service_date='2014_12',
            service_name='ConfiguratorManagement',
            params={'updateAdmissibilityInputList': updateAdmissibilityInputList},
            response_cls=GetAdmissibilityResponse,
        )
