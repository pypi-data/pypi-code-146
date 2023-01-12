from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, Dataset, ValidationData, ValidationResult, ItemRevision
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OneResultEvaluated(TcBaseObj):
    """
    OneResultEvaluated lists evaluation status for one validation result. Validation result object may be NULL if said
    validation is not performed.
    
    :var status: Validation result status defined in enum validationRunStatus.
    :var partDataset: Pointer to the validation target object.
    :var checker: Pointer to a validation checker object.
    :var result: Pointer to a ValidationResult object that was created for the specified validation checker and
    validation target.
    :var checkPassed: When TRUE, it indicates that the validation checker for the validation target is passed according
    to validation rule. When FALSE, the check failed according to the validation rules.
    """
    status: validationRunStatus = None
    partDataset: Dataset = None
    checker: ValidationData = None
    result: ValidationResult = None
    checkPassed: bool = False


@dataclass
class OneSetResultsEvaluated(TcBaseObj):
    """
    OneSetResultsEvaluated lists evaluation statuses for a set of validation results. Compound result status is TRUE if
    all results in current set passed validation rule verification. Otherwise, the status is FALSE.
    
    :var evaluatedResults: Evaluation statuses for each of validation result in a set.
    :var compoundResult: When TRUE, all validation results in the set satisfy validation rule. When FALSE, at least one
    validation result failed according to validation rule.
    :var clientId: Unique client identifier string.
    """
    evaluatedResults: List[OneResultEvaluated] = ()
    compoundResult: bool = False
    clientId: str = ''


@dataclass
class ValidationExpressionInfo(TcBaseObj):
    """
    The ValidationExpressionInfo structure represents input requirement formula for operation
    parseRequirementExpressions.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify returned ValidationParserOutput
    elements and partial errors associated with this input ValidationExpressionInfo.
    :var requirementExpression: A requirement formula string to be checked for syntax and to be parsed.
    """
    clientId: str = ''
    requirementExpression: str = ''


@dataclass
class ValidationParserOutput(TcBaseObj):
    """
    The ValidationParserOutput structure contains a list of variables names and a list of functions names parsed from
    the requirement formula string by operation parseRequirementExpressions.
    
    :var clientId: Identifying string from the source ValidationExpressionInfo.
    :var variableNames: A list of variables names parsed from requirement formula string.
    :var functionNames: A list of function names parsed from requirement formula string.
    """
    clientId: str = ''
    variableNames: List[str] = ()
    functionNames: List[str] = ()


@dataclass
class ValidationParserResponse(TcBaseObj):
    """
    The ValidationParserResponse structure holds the response from parseRequirementExpressions.
    
    :var output: List of names of variables and functions in the input requirement formula string in
    ValidationExpressionInfo.
    :var serviceData: The service data.
    """
    output: List[ValidationParserOutput] = ()
    serviceData: ServiceData = None


@dataclass
class EvaluateValidationResultsWithRulesInfo(TcBaseObj):
    """
    The EvaluateValidationResultsWithRulesInfo structure is the main input for evaluateValidationResultsWithRules
    operation to evaluate validation results. It may contain such workspace objects as items or item revisions or
    datasets or folders as well as validation rule set item revision or checkers. Client has the option to provide
    either validation rule item revision or list of checkers. When neither validation rule item revision nor checkers
    is provided, evaluation is performed without rule (in which case all existing validation results are evaluated as
    mandatory checks and all must PASS).
    
    :var selectedWSOs: List of Folder, Item, ItemRevision, Dataset to be evaluated.
    :var selectedCheckers: List of checkers used for evaluation.  The checker must be a NXValDataRevision or a subtype
    of it. This can be specified together with 'datasetTypes' when no rule set item revision is provided.  If a rule
    set item revision is already specified by 'ruleItemRevision', the checkers specified here will be ignored.
    :var datasetTypes: List of dataset types. This must be specified if a list of checkers is used for evaluation.  If
    it is not specified but the checkers are provided, then the checkers are ignored by this operation. Its array
    length does not need to match the list of selected checkers. All dataset types in this array applies to all
    checkers in 'selectedCheckers'. For example,if user provided checker1, checker2 and checker3 in 'selectedCheckers',
    then provided dataset type A and data set type B in 'datasetTypes', it means that the dataset type A and datatype B
    must have passed validation results for checker 1, 2 and 3.
    :var ruleItemRevision: Validation rule set item revision containing a ValidationRuleSet dataset. Can be NULL if a
    list of checkers is used for evaluation.
    :var clientId: A unique string supplied by the caller. This ID is used to identify returned OneSetResultsEvaluated
    elements and Partial Errors associated with this input EvaluateValidationResultsWithRulesInfo.
    """
    selectedWSOs: List[WorkspaceObject] = ()
    selectedCheckers: List[ValidationData] = ()
    datasetTypes: List[str] = ()
    ruleItemRevision: ItemRevision = None
    clientId: str = ''


@dataclass
class EvaluateValidationResultsWithRulesResponse(TcBaseObj):
    """
    The EvaluateValidationResultsWithRulesResponse structure holds the response from evaluateValidationResultsWithRules
    operation.
    
    :var evaluatedResultsList: List of sets of validation results that evaluated for each input
    EvaluateValidationResultsWithRulesInfo.
    :var serviceData: The service data.
    """
    evaluatedResultsList: List[OneSetResultsEvaluated] = ()
    serviceData: ServiceData = None


class validationRunStatus(Enum):
    """
    validationRunStatus lists validation result evaluation statuses.
    """
    upToDate = 'upToDate'
    outOfDatePartChanged = 'outOfDatePartChanged'
    outOfDateRequirementChanged = 'outOfDateRequirementChanged'
    verifyParameterFailed = 'verifyParameterFailed'
    missingReportLog = 'missingReportLog'
    notRun = 'notRun'
    notRequired = 'notRequired'
