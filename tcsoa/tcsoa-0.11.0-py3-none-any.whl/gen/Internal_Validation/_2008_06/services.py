from __future__ import annotations

from tcsoa.gen.Internal.Validation._2008_06.Validation import ValidationExpressionInfo, EvaluateValidationResultsWithRulesResponse, ValidationParserResponse, EvaluateValidationResultsWithRulesInfo
from typing import List
from tcsoa.base import TcService


class ValidationService(TcService):

    @classmethod
    def parseRequirementExpressions(cls, inputs: List[ValidationExpressionInfo]) -> ValidationParserResponse:
        """
        This operation checks the syntax of a requirement formula string and parses it into a list of variables and
        functions if the string has no syntax error.
        
        Use cases:
        The property requirement_formula on ValReqRevision object need to follow a specific syntax and the variable
        names in the property requirement_formula need to match with the objects in property requirement_expressions on
        ValReqRevision object.
        This operation can be used for following use cases:
        - Checks the syntax of a requirement formula string before setting it as the value of property
        requirement_formula on ValReqRevision object
        - Extract a list of variable names from a requirement formula string and use these names to populate the
        property requirement_expressions on ValReqRevision object.
        
        """
        return cls.execute_soa_method(
            method_name='parseRequirementExpressions',
            library='Internal-Validation',
            service_date='2008_06',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=ValidationParserResponse,
        )

    @classmethod
    def evaluateValidationResultsWithRules(cls, inputs: List[EvaluateValidationResultsWithRulesInfo]) -> EvaluateValidationResultsWithRulesResponse:
        """
        This operation evaluates a set of objects against a validation rule set or a set of validation checkers to
        verify whether the validation results on these objects satisfy the validation rule set or checkers.  
        The objects can be any combination of the following WorkspaceObject types: Folder, Item, ItemRevision and
        Dataset. The checking criteria can be either a validation rule set item revision or a set of validation
        checkers and the applicable dataset types.
        This operation will first find the validation target datasets from the input object list, and then evaluate all
        results on these target dataset against the validation rule set or checkers. This operation only supports the
        validation results for NX Agents, such as NX Check Mate and NX RDDV.
        
        Use cases:
        In some companies, to ensure the CAD model quality, all NX parts must pass certain NX Check Mate checks before
        it can be released or a new baseline can be created.  There are several existing workflow handlers and a
        baseline operation can be used check the existing validation results on the to be released or to be baselined
        item revisions against a validation rule set and indicate whether the item revision pass the rule set  or not.
        In the rule evaluation tab of Validation Results Viewer in the rich client, a user can also select a list of
        objects and a validation rule set to see the evaluation results.
        This operation provides a programmatic way to perform the similar evaluation as in above mentioned workflow
        handlers or rule evaluation capability in the rich client.
        In addition, this operation can also check the validation results against a set of checkers and dataset types
        if no validation rule set are provided.
        """
        return cls.execute_soa_method(
            method_name='evaluateValidationResultsWithRules',
            library='Internal-Validation',
            service_date='2008_06',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=EvaluateValidationResultsWithRulesResponse,
        )
