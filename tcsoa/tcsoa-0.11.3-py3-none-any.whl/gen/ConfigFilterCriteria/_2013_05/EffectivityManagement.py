from __future__ import annotations

from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OverlapStateList(TcBaseObj):
    """
    A list of indicators for the degree of overlap between two effectivity expressions.
    
    :var overlapStates: A vector of overlap enumeration values. Valid values for an overlap enumeration are:
    -    OverlapStateNone : The two expressions have no overlap. There is no satisfing solution common to both
    expressions. A conjunction (AND combination) of the two is unsatisfiable.
    -    OverlapStateSubset : The two expressions overlap. The expression's solution set is a subset of the reference
    expression's solution set. The conjunction (AND combination) of the expression with the negated reference
    expression is unsatisfiable.
    -    OverlapStateMatch : The two expressions are logically equivalent. Every solution that satifies one expression
    also satifies the other, and vice versa.
    -    OverlapStateSuperset : The two expressions overlap. The expression's solution set is a superset of the
    reference expression's solution set. The conjunction (AND combination) of the negated expression with the reference
    expression is unsatisfiable.
    -    OverlapStateIntersect : The two expressions overlap. The expression's solution set has some overlap with the
    refernce expression's solution set.
    
    """
    overlapStates: List[OverlapState] = ()


@dataclass
class EffectivityDisplayStringResponse(TcBaseObj):
    """
    A list of localized string representations for effectivity expressions. The format is a pure output format intended
    to increase ease of reading. It cannot be used as input because its format allows ambiguous syntax.
    
    :var displayString: Vector of effectivity display strings. This format is the same as for effectivity formula
    properties mdl0effectivity_formula and mdl0allowed_eff_formula.
    :var serviceData: Teamcenter service data.
    """
    displayString: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityOverlapStateResponse(TcBaseObj):
    """
    Indicates the degreee of overlap for pairs of effectivity expressions.
    
    :var overlapStates: A vector of overlap enumeration values.
    :var serviceData: Teamcenter service data.
    """
    overlapStates: List[OverlapStateList] = ()
    serviceData: ServiceData = None


class OverlapState(Enum):
    """
    Operlap states enumerations.
    
    :var OverlapStateNone: The two expressions have no overlap. There is no satisfing solution common to both
    expressions. A conjunction (AND combination) of the two is unsatisfiable.
    :var OverlapStateSubset: The two expressions overlap. The expression's solution set is a subset of the reference
    expression's solution set. The conjunction (AND combination) of the expression with the negated reference
    expression is unsatisfiable.
    :var OverlapStateMatch: The two expressions are logically equivalent. Every solution that satifies one expression
    also satifies the other, and vice versa.
    :var OverlapStateSuperset: The two expressions overlap. The expression's solution set is a superset of the refernce
    expression's solution set. The conjunction (AND combination) of the negated expression with the reference
    expression is unsatisfiable.
    :var OverlapStateIntersect: The two expressions overlap. The expression's solution set has some overlap with the
    refernce expression's solution set.
    """
    None_ = 'OverlapStateNone'
    Subset = 'OverlapStateSubset'
    Match = 'OverlapStateMatch'
    Superset = 'OverlapStateSuperset'
    Intersect = 'OverlapStateIntersect'
