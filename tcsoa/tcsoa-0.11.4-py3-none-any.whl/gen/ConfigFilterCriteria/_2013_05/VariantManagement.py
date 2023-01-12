from __future__ import annotations

from tcsoa.gen.BusinessObjects import Variant, ConfigurationFamily, POM_object
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TeamcenterConfiguratorInfo(TcBaseObj):
    """
    Contains additional information about variant data that is only available when using Teamcenter configurators. For
    any non Teamcenter configurator, this structure may contain null elements.
    The 'TeamcenterConfiguratorInfo' structure is interoperated as "NULL" if it has following values set for its
    parameters:
    variant : NULLTAG
    optionValue : NULLTAG
    
    
    :var variant: Teamcenter family business object of type Variant. It can be null if information is retrieved from
    non Teamcenter configurator.
    :var optionValue: Workspace representation of option value code. This parameter can be null if information is being
    retrieved from non Teamcenter configurator.
    """
    variant: Variant = None
    optionValue: POM_object = None


@dataclass
class VariantCriteria(TcBaseObj):
    """
    The 'VariantCriteria' structure represents a criteria object along with its variant criteria and associated
    validation records. The 'VariantCriteria' structure is interpreted to be "NULL" if the following values are set for
    its parameters:
    - 'variantCriteriaObject': NULLTAG
    - 'primaryVariantScope': a "NULL" ConfigFormula structure
    - 'solveType': -1
    - 'validationRecords': empty vector
    
    :var variantCriteriaObject: The VariantRule with which the criteria defines in this structure is associated.
    :var primaryVariantScope: Nominal variant criteria before applying constraints and defaults.
    :var solveType: Indicates how the variant criteria need to be solved. For possible values see preference
    'TC_Default_Solve_Type'.
    :var validationRecords: Validation records related to the variant criteria.
    """
    variantCriteriaObject: POM_object = None
    primaryVariantScope: ConfigExpression = None
    solveType: int = 0
    validationRecords: List[VariantValidationRecord] = ()


@dataclass
class VariantCriteriaResponse(TcBaseObj):
    """
    Returns variant configuration criteria along with default and constraint processing results.
    
    :var variantCriteria: Vector of variant criteria structures
    :var serviceData: Teamcenter ServiceData
    """
    variantCriteria: List[VariantCriteria] = ()
    serviceData: ServiceData = None


@dataclass
class VariantValidationRecord(TcBaseObj):
    """
    Represents validation results for variant criteria associated with a variant criteria object (VariantRule ).
    The 'VariantValidationRecord' structure is interpreted to be "NULL" if the following values are set to its
    parameters:
    
    '-validationDate': a NULLDATE as defined for the SOA client side binding in use.
    
    '-validationResult': a "NULL" ConfigFormula structure
    
    '-undeterminedFamilies': an empty vector
    
    '-violations': an empty vector
    
    '-appliedDefaults': an empty vector
    
    :var validationDate: Date of validation.
    :var validationResult: Validation result reflecting constraints and defaults.
    :var undeterminedFamilies: Families that are not set to a unique value. If empty, the criteria are complete.
    :var violations: Violation records. If empty, the variant criteria are valid.
    :var appliedDefaults: One record for each applied default in the sequence they were applied.
    """
    validationDate: datetime = None
    validationResult: ConfigExpression = None
    undeterminedFamilies: List[ConfigurationFamily] = ()
    violations: List[ConfigRuleViolation] = ()
    appliedDefaults: List[DefaultRule] = ()


@dataclass
class ConfigExpression(TcBaseObj):
    """
    Represents a configuration expression. The 'ConfigExpression' structure is interpreted as "'NULL'" when it has
    following values set for its parameters:
    'subExpressions' : An empty vector of 'ConfigExpression' structure
    'value' : A "NULL" 'ConfigOption' structure
    'opCode' : -1
    'formula' : A "NULL" 'ConfigFormula' structure
    'tnf' : An empty vector of 'ConfixExpression' structures.
    A 'ConfigExpression' that is equivalent to the Boolean constant 'TRUE' returns a TNF parameter comprising one
    expression with an 'opcode' value of '39'.
    A 'ConfigExpression' that is equivalent to the Boolean constant 'FALSE' returns a TNF parameter comprising one
    expression with an 'opcode' value of '40'.
    
    :var subExpressions: A vector of 'ConfigExpression'. If this parameter is present the enclosing expression
    represents a compound expression combining this set of subexpressions with the operator specified in the opCode
    parameter. If the enclosing expression is non-NULL either this parameter or the "'value'" parameter must be present.
    :var value: It is a 'ConfigOption' struct. If this parameter is present the enclosing expression represents an
    elemental expression literal. The parameter specifies the value to which 'opCode' compares. If the enclosing
    expression is non-NULL either this parameter or the 'subExpressions' parameter must be present. 'subExpressions'
    'and' value must not both be present.
    :var opCode: Operation code such as "and" and "or", see ps/ps_tokens.h.
    :var formula: It is a 'ConfigFormula' struct. If present, contains the configuration expression in string format
    (courtesy info).
    :var tnf: If present, this parameter provides a representation of the enclosing expression in Teamcenter Normal
    Form (TNF).
    The parameter is intended as "courtesy information" so to make additional SOA calls unnecessary by providing
    information that is expected to be of value if performance permits it. Based on the assumption that the vast
    majority of ConfigExpression structs can be converted to TNF very efficiently the server can afford to convert them
    to TNF as a "free gift". If this becomes a performance bottleneck the server may return a response with an empty
    tnf member, in which case the application can explicitly request a tnf representation using operation
    'convertVariantExpressions', if need be. Preference 'TC_tnf_timeout_period' controls the timeout mechanism. If TNF
    generation takes more time than specified in preference 'TC_tnf_timeout_period', server returns an empty 'tnf'
    member.
    If combined with OR the list of tnf expressions is logically equivalent to the enclosing expression. Each TNF is
    provided as a conjunction of Disjunctive Normal Forms (DNF) where all DNFs reference a single variant option
    family. Each clause in the outermost conjunction can reference a different variant option family.
    Example 1:
    Formula: (ENG = V6 | ENG = V8) & (D = 2.6L | D >= 3L & D <= 3.6L)
    TNF: Yes
    Note: DNF1 references family ENG and DNF2 references family D
    Example 2:
    Formula: (ENG = V6 | TRANS = AUTO) & (TRANS = M5 | ENG = V8)
    TNF: No
    Note: DNF1 references family ENG as well as TRANS and  DNF2 references family ENG as well as TRANS
    """
    subExpressions: List[ConfigExpression] = ()
    value: ConfigOption = None
    opCode: int = 0
    formula: ConfigFormula = None
    tnf: List[ConfigExpression] = ()


@dataclass
class ConfigFormula(TcBaseObj):
    """
    Represents a formula string associated with a configuration expression in configurator syntax. 
    A formula of the form "[OptionNamespace]FamilyName = UniqueValue" is called "explicit" because no product context
    is required to determine the family name for the value, or the option namespace for the family name.
    OptionNamespace and FamilyName are explicitly spelled out. A variant formula is in "explicit Teamcenter language"
    if its form is explicit and comprised of the lexemes documented for the Variant Formula property.
    A formula of the form "UniqueValue" is called "stenographic" because a parser has to infer OptionNamespace and
    FamilyName. This is possible if there is only one value with that name throughout the entire product.
    If lexemes other than those documented for the Variant Formula property are used the formula is in "external
    variant language" and a custom configurator is required to decode the formula.
    If a formula is explicit Teamcenter language, productName and productNameSpace can be empty ("").
    The ConfigFormula structure is considered "NULL" if it has following values set for its parameters:
    - formula: empty string ("")
    - productName: empty string ("")
    - productNameSpace: empty string ("")
    
    :var formula: Formula string in configurator syntax.
    :var productName: Name of the product(e.g.ItemID). Used in conjunction with productNameSpace parameter to resolve
    any ambiguity in variant option value names.
    :var productNameSpace: Namespace of the product in which the "product" has unique semantics, e.g., ItemRevID,
    model_year or product_type. Used in conjunction with productName parameter to resolve any ambiguity in variant
    option value names.
    """
    formula: str = ''
    productName: str = ''
    productNameSpace: str = ''


@dataclass
class ConfigOption(TcBaseObj):
    """
    Represents a configuration option that is unique in the context of a ConfigurationFamily. 
    The ConfigOption structure is interpreted as "NULL" if it has the following values set for its parameters: 
    family: NULLTAG
    valueCode: empty string ("")
    description: empty string ("")
    additionalInfo : Null Structure
    
    
    :var family: A ConfigurationFamily object which represents a configuration option.
    :var valueCode: Name of the option value. "" is treated as NO VALUE SELECTED, i.e. it does not match any non-empty
    name.
    :var description: Description of the option value.
    :var additionalInfo: A 'TeamcenterConfiguratorInfo' struct having additional information about Teamcenter
    configurator objects.
    """
    family: ConfigurationFamily = None
    valueCode: str = ''
    description: str = ''
    additionalInfo: TeamcenterConfiguratorInfo = None


@dataclass
class ConfigRuleViolation(TcBaseObj):
    """
    Represents a violated rule along with the message and severity associated with rule violation.
    
    The 'ConfigRuleViolation' structure is interpreted to be "NULL" if following values are set to its parameters:
    
    - 'message': empty string ("")
    
    - 'severity': ConstraintSeverityInformation
    
    - 'violatedCondition': a "NULL" 'ConfigExpression' structure
    
    :var message: The message to display if this rule is violated.
    :var severity: The severity code for the message. Valid values are:
    
    - ConstraintSeverityInformation : Classifies information associated with this constraint as additional information,
    such as hints, which are of interest if configuration criteria satisfy this constraint.
    
    - ConstraintSeverityWarning : Classifies information associated with this constraint as considerations, such as
    recommendations, which are important to review if configuration criteria satisfy this constraint.
    
    - ConstraintSeverityError : Configuration criteria that satisfy this constraint are classified as invalid.
    :var violatedCondition: The rule that was found to be violated.
    """
    message: str = ''
    severity: ConstraintSeverity = None
    violatedCondition: ConfigExpression = None


@dataclass
class DefaultRule(TcBaseObj):
    """
    A rule to determine the default value, or value range, for a variant option family. 
    The 'DefaultRule' structure is interpreted to be "NULL" if it has following values set to its parameters:
    
    - 'partiallyApplicable': false
    
    - 'restrictiveCondition': a "NULL" ConfigExpression
    
    - 'appliedDefault': "NULL" ConfigExpression structure
    
    - 'appliedTo': "NULL" ConfigExpression structure
    
    :var partiallyApplicable: If "true", the default is only applicable to a subset of the criteria (courtesy info).
    :var restrictiveCondition: The condition under which the default is applicable. Can be NULL.
    :var appliedDefault: The default condition that was applied, indicating that "'restrictiveCondition'" was met.
    :var appliedTo: The config condition before applying the default."'appliedDefault'".
    """
    partiallyApplicable: bool = False
    restrictiveCondition: ConfigExpression = None
    appliedDefault: ConfigExpression = None
    appliedTo: ConfigExpression = None


class ConstraintSeverity(Enum):
    """
    Severity code for error message.
    
    :var ConstraintSeverityInformation: Classifies information associated with this constraint as additional
    information, such as hints, which are of interest if configuration criteria satisfy this constraint.
    :var ConstraintSeverityWarning: Classifies information associated with this constraint as considerations, such as
    recommendations, which are important to review if configuration criteria satisfy this constraint.
    :var ConstraintSeverityError: Configuration criteria that satisfy this constraint are classified as invalid.
    """
    Information = 'ConstraintSeverityInformation'
    Warning = 'ConstraintSeverityWarning'
    Error = 'ConstraintSeverityError'
