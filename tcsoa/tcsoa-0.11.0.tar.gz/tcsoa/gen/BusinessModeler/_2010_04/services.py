from __future__ import annotations

from tcsoa.gen.BusinessModeler._2010_04.BusinessRules import GetVerificationRulesResponse, VerificationRuleInput
from typing import List
from tcsoa.base import TcService


class BusinessRulesService(TcService):

    @classmethod
    def getVerificationRules(cls, input: List[VerificationRuleInput]) -> GetVerificationRulesResponse:
        """
        This operation gets a list of VerificationRule objects which match the given criteria each
        VerificationRuleInput supplied and its context_filter attribute which refers to a Condition object defined in
        Business Modeler IDE equals to true; Wild cards can be specified in strings using * in VerificationRuleInput
        which mean to match all cases for the criteria strings. This operation not only returns all VerificationRule
        objects which full match criteria in VerificationRuleInput, it also returns VerificationRule objects whose type
        attribute is the parent of the typeName defined in the VerificationRuleInput, meanwhile other criteria are
        matched.
        
        Use cases:
        4 samples Verification Rules created in Business Modeler IDE
        {Functionality= Fnd0BOMGrading, Business Object=Item, Context Filter =isTrue, Condition Rule=Condition1, Sub
        Group=*}
        {Functionality= Fnd0BOMGrading, Business Object=Part, Context Filter = isEngineeringGroup, Condition
        Rule=Condition1, Sub Group=*}
        {Functionality= Fnd0BOMGrading, Business Object= CommericalPart, Context Filter =isTrue, Condition
        Rule=Condition2, Sub Group= Americas}
        {Functionality= Fnd0APS, Business Object=Item, Context Filter =isTrue, Condition Rule=Condition1, Sub Group= *}
        Login Teamcenter as dba group and get VerificationRule objects by setting functionality as Fnd0BOMGrading and
        typeName as CommericalPart. Following VerificationRule objects in will be returned.
        {Functionality= Fnd0BOMGrading, Business Object=Item, Context Filter =isTrue, Condition Rule=Condition1, Sub
        Group=*}
        {Functionality= Fnd0BOMGrading, Business Object= CommericalPart, Context Filter =isTrue, Condition
        Rule=Condition2, Sub Group=Americas}
        The first rule applies to Item, if Condition1 could check Item, it could check CommericalPart, since
        CommericalPart is a sub type of Item and it is sure that CommericalPart contains all properties checked in
        Condition1, so it is valid. The second rule applies to all CommericalPart, so it is also valid. The other
        VerificationRule objects either do not match functionality or typeName, or else context_filter equals to false.
        """
        return cls.execute_soa_method(
            method_name='getVerificationRules',
            library='BusinessModeler',
            service_date='2010_04',
            service_name='BusinessRules',
            params={'input': input},
            response_cls=GetVerificationRulesResponse,
        )
