from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2015_10.ConfiguratorManagement import ApplicationConfigExpression
from tcsoa.gen.BusinessObjects import Cfg0AbsAdmissibility, POM_object, Cfg0ConfiguratorPerspective
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetModelOptionCondInput(TcBaseObj):
    """
    Input structure containing the expressions which are to be split in the model and the option variant condition
    components. Each GetModelOptionCondInput forms a partial error boundary.
    
    :var configPerspective: The Cfg0ConfiguratorPerspective instance to specify the context and revision rule. This
    parameter can be NULL if the operation parameter for the perspective is not NULL. If a perspective is specified
    here it overwrites the operation parameter operationConfigPerspective for corresponding processing of
    inputExpressions.
    :var inputExpressions: The List of input expression to be split in the model and the option variant condition
    expressions.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    inputExpressions: List[ApplicationConfigExpression] = ()


@dataclass
class GetModelOptionCondOutput(TcBaseObj):
    """
    Output structure containing the model and the option variant condition expressions for the input expressions.
    
    :var index: The index corresponding to input structure index.
    :var modelOptionCondList: The list of structures having condition information one for each input condition.
    """
    index: int = 0
    modelOptionCondList: List[ModelOptionCondStruct] = ()


@dataclass
class GetModelOptionCondResponse(TcBaseObj):
    """
    Response structure for getModelAndOptionConditions operation.
    Each entry will correspond to the partial error boundary of one input structure.
    
    :var modelOptionCondOutputList: The list of output structures one for each input having variant expression
    information.
    :var serviceData: ServiceData to return partial errors.
    """
    modelOptionCondOutputList: List[GetModelOptionCondOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ModelOptionCondStruct(TcBaseObj):
    """
    Structure containing the model expressions and the option variant conditions corresponding to the one input
    ApplicationConfigExpression.
    
    :var modelExpressions: The list of application configuration expression structures for processing.
    :var optionConditions: The list of expression providing information of the option conditions.
    """
    modelExpressions: List[ApplicationConfigExpression] = ()
    optionConditions: List[ApplicationConfigExpression] = ()


@dataclass
class OverlapStateInfo(TcBaseObj):
    """
    Contains information about the degree of overlap between a set of configuration expressions and a given reference
    configuration expression.
    
    :var index: This index identifies the input structure for which overlap states are recorded.
    :var overlapStates: Each overlap state value indicates the degree of overlap between the expression at a given
    index in the corresponding input structure and the reference expression in that input structure.
    The getDisplayStrings operation in the SessionService can be used to obtain a display value for each of the
    following overlap state keys:
    - k_overlapstate_none: The two expressions have no overlap. There is no satisfying solution common to both
    expressions. A conjunction (AND combination) of the two is unsatisfiable.
    - k_overlapstate_subset: The two expressions overlap. The solution set of the expression is a subset of the
    solution set of the reference expression. The conjunction (AND combination) of the expression with the negated
    reference expression is unsatisfiable.
    - k_overlapstate_match: The two expressions are logically equivalent. Every solution that satisfies one expression
    also satisfies the other, and vice versa.
    - k_overlapstate_superset: The two expressions overlap. The solution set of the expression is a superset of the
    solution set of the reference expression. The conjunction (AND combination) of the negated expression with the
    reference expression is unsatisfiable.
    - k_overlapstate_intersect: The two expressions overlap. The solution set of the expression has some overlap with
    the solution set of the reference expression.
    
    """
    index: int = 0
    overlapStates: List[str] = ()


@dataclass
class OverlapStateInput(TcBaseObj):
    """
    Contains a reference expression and a list of configuration expressions with the intent to determine the degree of
    overlap between them.
    
    :var referenceExpression: The reference expression for which the degree of overlap with each of the expressions
    should be determined.
    :var expressions: The list of application configuration expressions for which the overlap state with the
    referenceExpression should be determined.
    """
    referenceExpression: ApplicationConfigExpression = None
    expressions: List[ApplicationConfigExpression] = ()


@dataclass
class OverlapStateResponse(TcBaseObj):
    """
    Returns the degree of overlap between the expressions in each input structure.
    
    :var overlapInfo: Contains overlap state information for the expression in each input record.
    :var serviceData: The standard Teamcenter ServiceData structure.
    """
    overlapInfo: List[OverlapStateInfo] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateAdmissibilityData(TcBaseObj):
    """
    The admissibility data to be updated.
    
    :var admissibilityObject: The admissibility Cfg0AbsAdmissibility object to be updated.
    :var admissibilityState: The new admissibility state to be updated. The admissibility state is driven by LOV
    Cfg0AdmissibilityState.
    """
    admissibilityObject: Cfg0AbsAdmissibility = None
    admissibilityState: str = ''


@dataclass
class UpdateAdmissibilityInputList(TcBaseObj):
    """
    List of update admissibility input.
    
    :var updateAdmissibilityInputs: The list of admissibility input to be updated.
    """
    updateAdmissibilityInputs: List[UpdateAdmissibilityInputStruct] = ()


@dataclass
class UpdateAdmissibilityInputStruct(TcBaseObj):
    """
    The input structure for the operation updateAdmissibility corresponding to one context object.
    
    :var contextObject: The context business object (POM_object) for which admissibility data to be updated.
    :var updateAdmissibilityData: The list of admissibility data corresponding to one context object.
    """
    contextObject: POM_object = None
    updateAdmissibilityData: List[UpdateAdmissibilityData] = ()
