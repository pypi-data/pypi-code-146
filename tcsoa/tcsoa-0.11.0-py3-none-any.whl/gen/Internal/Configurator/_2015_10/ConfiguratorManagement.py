from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0AbsValue, Cfg0AbsFamily, RevisionRule, Cfg0ConfiguratorPerspective, Cfg0AbsConfiguratorWSO
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ValidateProductConfigOutput(TcBaseObj):
    """
    It is structure containing output information per input expressionsToValidate.
    
    :var updatedExpression: An expanded expression satisfying the given expression to validate and existing set of
    constraint in the configurator perspective.
    :var violations: The list of constraints that were violated for a given expression to validate.
    :var criteriaStatus: The status of the configuration. Valid  values  are: validAndComplete, validAndInComplete or
    inValid.  
    validAndComplete: all mandatory families in configuration have value selections.  
    validAndInComplete: not all mandatory families in configuration have value selections. 
    inValid: there are some violations .
    :var requiredFamilies: A list of mandatory families, which do not have any value selection based on input
    expression and default value in the context.
    """
    updatedExpression: BusinessObjectConfigExpression = None
    violations: List[Violation] = ()
    criteriaStatus: str = ''
    requiredFamilies: List[Cfg0AbsFamily] = ()


@dataclass
class ValidateProductConfigurationResponse(TcBaseObj):
    """
    The response structure for the operation ValidateProductConfiguration 
    
    :var serviceData: The service data for errors and returned objects.
    :var outputs: The list of expressions that was validated and updated with selections due to application of
    constraints.
    """
    serviceData: ServiceData = None
    outputs: List[ValidateProductConfigOutput] = ()


@dataclass
class AvailableProductVariabilityOutput(TcBaseObj):
    """
    The response structure returned by getAvailableProductVariability.
    
    :var availabilityExpressions: A list of AvailableVariability expressions defining available variability. The number
    of elements in this list should be equal to the number of  families which at least have a one available feature or
    default feature for the given input expression(criteriaExpression ). If an empty familiesToTest list was specified
    this vector would be empty.
    :var violations: A list of constraints that were violated for a given user selected values/input expression.
    :var suggestedSatisfyingExpr: A sample expression satisfying the given input expression and existing set of
    constraint in the configurator context. This is an output expression containing system suggested features from the
    available features.
    :var criteriaStatus: The status of the configuration. Valid values are: validAndComplete, validAndInComplete or
    inValid.  
    validAndComplete: all mandatory families in configuration have value selections.  
    validAndInComplete: not all mandatory families in configuration have value selections. 
    inValid: there are some violations.
    :var requiredFamilies: A list of mandatory families, which do not have any feature selection based on input
    expression and default feature in the context.
    :var serviceData: The service data for errors and returned objects.
    """
    availabilityExpressions: List[AvailableVariability] = ()
    violations: List[Violation] = ()
    suggestedSatisfyingExpr: ApplicationConfigExpression = None
    criteriaStatus: str = ''
    requiredFamilies: List[Cfg0AbsFamily] = ()
    serviceData: ServiceData = None


@dataclass
class Violation(TcBaseObj):
    """
    Represents a violated rule along with the message and severity associated with rule violation.
    
    :var message: The message to display if this rule is violated.
    :var severity: The severity associated with the message. Valid values for this parameter are defined by the
    ListOfValues "Cfg0ConstraintSeverity".
    :var violatedRule: The rule that was found to be violated.
    :var configuratorWSO: Validation constraint for product variant configurations. It might contain NULL in case user
    is not privileged to read validation constraint rule.
    """
    message: str = ''
    severity: str = ''
    violatedRule: ApplicationConfigExpression = None
    configuratorWSO: Cfg0AbsConfiguratorWSO = None


@dataclass
class AvailableVariability(TcBaseObj):
    """
    Defines available features for a given family along with the default features for operation
    getAvailableProductVariability. The AvailableVariability structure is interpreted as "NULL" if it has the following
    values set for its parameters:
    
    defaultValues: empty list
    
    availability: empty list
    
    :var defaultValues: Specifies the list of configuration expression terms referencing default features from the
    requested family. This list can have more than one element only if the family is a multi-select otherwise list
    would contain either zero or one element. If no default rules exist or they select a default feature such that it
    is ruled out due to other constraints, this will be an empty list to indicate  non-existing default values.
    :var availability: The list of configuration expressions referencing values only from the requested families. This
    is a list of discrete values or ranges.
    """
    defaultValues: List[ConfigExpressionTerm] = ()
    availability: List[ConfigExpressionTerm] = ()


@dataclass
class BusinessObjectConfigExpression(TcBaseObj):
    """
    Relates a business object (e.g. Cpd0DesignElement, VariantRule, or Cfg0ExcludeRule) to a list of configuration
    expressions.
    
    :var targetObject: The business object (e.g. Cpd0DesignElement, VariantRule, or Cfg0ExcludeRule), to which the
    configuration expressions specified in parameter 'expressions' are linked.
    :var expressions: The list of 'ApplicationConfigExpression' structures for the business object.
    :var clientId: The unique identifier to distinguish the input and corrosponding output.
    """
    targetObject: BusinessObject = None
    expressions: List[ApplicationConfigExpression] = ()
    clientId: str = ''


@dataclass
class ConfigExprWithDisplayString(TcBaseObj):
    """
    It contains the config expression populated with formula, SOA grid structure and display format.
    
    :var configExprDisplayString: Display string for configuration expression.
    """
    configExprDisplayString: str = ''


@dataclass
class ApplConfigExprWithDisplayString(TcBaseObj):
    """
    It contains the application configuration expression populated with formula,  grid structure and display format.
    
    :var applConfigExpr: The application configuration expression for which formula,  grid structure and display format
    is requested.
    :var applConfigExprDisplayString: Display string for application configuration expression.
    :var configExprSetsInfo: List of configuration expression set which will contain list of configuration expressions
    populated with formula,  grid structure and display format.
    """
    applConfigExpr: ApplicationConfigExpression = None
    applConfigExprDisplayString: str = ''
    configExprSetsInfo: List[ConfigExpressionSetInfo] = ()


@dataclass
class ConfigExpression(TcBaseObj):
    """
    Defines a Boolean expression to be used for configuration purposes.
    
    :var clientID: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var expressionType: The expression category and the intent of this expression.
    
    The valid values are as follows:
    - 9   - Variant Condition
    - 18 - Variant Rule
    - 25 - Applicability
    - 44 - Subject
    
    
    :var formula: The persistent formula string in Teamcenter syntax (see documentation for property
    ''cfg0SubjectCondition'' or BOMLine property ''bl_formula'').
    :var subExpressions: The list of sub-expressions in a Boolean variant expression. The sub-expressions are joined
    together by OR operator.
    """
    clientID: str = ''
    expressionType: int = 0
    formula: str = ''
    subExpressions: List[ConfigSubExpression] = ()


@dataclass
class ConfigExpressionGroup(TcBaseObj):
    """
    This structure groups 'ConfigExpressionTerm' structures. A mixture of positive and negated expression terms in the
    same expression group is not allowed. Positive terms within an expression group are combined with operator 'OR',
    e.g. Color=Red | Color=Green. Negated terms within an expression group are combined with operator 'AND', e.g.
    Color!=Red & Color!=Green.
    
    :var context: The family object instance to be used in a free form family expression term, or a feature range
    expression.
    :var groupName: The name for the group containing the expression terms. If the group name is provided as FALSE then
    group expression would be considered as FALSE. If the group name is provided as TRUE then group expression would be
    considered as TRUE.
    :var terms: the list of 'ConfigExpressionTerm' structures. The terms are combined together by OR operator.
    """
    context: Cfg0AbsFamily = None
    groupName: str = ''
    terms: List[ConfigExpressionTerm] = ()


@dataclass
class ConfigExpressionSet(TcBaseObj):
    """
    The collection of 'ConfigExpressions' refered as set for the business object. A set collects different type of
    varint expressions such as applicability and subject. These will be joined together by AND operation and evaluated
    as part of single statement.
    
    :var configExpressions: The list of 'ConfigExpression' structures which are collected as a set for the business
    object. Each structure defines a variant expression which can be used for the configuration purposes.
    """
    configExpressions: List[ConfigExpression] = ()


@dataclass
class ConfigExpressionSetInfo(TcBaseObj):
    """
    It contains the list of config expressions populated with formula, SOA grid structure and display format.
    
    :var configExprsWithDisplayString: List of configuration expressions populated with formula,  grid structure and
    display format.
    """
    configExprsWithDisplayString: List[ConfigExprWithDisplayString] = ()


@dataclass
class ConfigExpressionTerm(TcBaseObj):
    """
    Defines an elemental expression literal for a single feature, or feature range expression for a given family.
    
    :var family: The family object instance to be used in a free form family expression term, or a feature range
    expression.
    :var familyID: The ID of the family in the term
    :var familyNamespace: The family namespace by which the family object is uniquely identified.
    :var operatorCode: The operator code to use for this expression terms.
    
    The Valid values are as follows:
    - 5 - Equals
    - 6 - Not Equals
    - 10 - And
    - 11 - OR
    
    
    :var rangeExpressions: A list of elemental expression literals describing a feature range for a given  family.
    :var value: The feature object to be used in an elemental expression literal.
    :var valueText: The ID of the feature object or the feature to use for a free form family.
    :var selectionClass: Specifies the selection type of the feature object. This parameter specifies whether the
    feature object is user selected, default selected or system selected.
    
    Valid Values are as follow:
    - EmptyInitialized A constraint has initialized a family with the empty value.
    - Default          A constraint has assigned a default value.
    - PackageDefault   A package constraint has assigned a default value.
    - Unknown          An administrator authored constraint with unknown severity has assigned a value. If a feature
    selection is not known precisely, it will be represented as unknown.
    - Information      A constraint with Info severity has assigned a value. Refer Cfg0ConstraintSeverity list of
    values for details.
    - Warning          A constraint with Warning severity has assigned a value. Refer Cfg0ConstraintSeverity list of
    values for details.
    - Error            A constraint with Error severity has assigned a value. Refer Cfg0ConstraintSeverity list of
    values for details.
    - User             User has assigned a value.
    
    """
    family: Cfg0AbsFamily = None
    familyID: str = ''
    familyNamespace: str = ''
    operatorCode: int = 0
    rangeExpressions: List[RangeExpression] = ()
    value: Cfg0AbsValue = None
    valueText: str = ''
    selectionClass: str = ''


@dataclass
class ApplicationConfigExpression(TcBaseObj):
    """
    The configuration expression for the business object.
    
    :var formula: The persistent formula string in Teamcenter syntax.
    :var exprID: The application expression identifier used to distinguish the current expression from other variant
    expressions authored for the same business object.
    :var expressionType: Specifies the expression category and the intent of this expression. The valid values are as
    follows:
    -  9 -  Variant Condition
    - 18 - Variant Rule
    - 28 - Inclusive Constraint
    - 29 - Exclusive Constraint
    - 37 - Default Rule
    - 41 - Availability Rule
    
    
    :var configExprSets: The list of 'ConfigExpressionSet' which are relevant to the business object. The variant
    expression sets are combined by OR operator.
    """
    formula: str = ''
    exprID: str = ''
    expressionType: int = 0
    configExprSets: List[ConfigExpressionSet] = ()


@dataclass
class ConfigSubExpression(TcBaseObj):
    """
    This structure lists the 'ConfigExpressionGroup' structures which are joined together by "AND" operator.
    
    :var expressionGroups: The list of clauses in a Boolean expression. The groups are combined together by AND
    operator.
    """
    expressionGroups: List[ConfigExpressionGroup] = ()


@dataclass
class ConvertVariantExpressionInput(TcBaseObj):
    """
    An input structure defining the list of application configuration expressions for which formula,  grid structure
    and the display format is requested.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var exprsToConvert: List of application config expressions for which fomula, SOA grid struture and the display
    format is requested.
    :var context: The Cfg0ConfiguratorPerspective instance to specify the context and revision rule. This is a
    mandatory parameter.
    :var expressionFormat: This flag will indicate what will be populated in output 'ApplicationConfigExpression'
    structure. Following are valid values:
    0 - formulae, grid expression and display formulae
    1 - formulae
    2 - grid expression 
    3 - formulae and grid expression
    4 - display formulae 
    5 - formulae and display formulae
    6 - grid expression and display formulae
    """
    clientId: str = ''
    exprsToConvert: List[ApplicationConfigExpression] = ()
    context: Cfg0ConfiguratorPerspective = None
    expressionFormat: int = 0


@dataclass
class ConvertVariantExpressionOutput(TcBaseObj):
    """
    It contains the list of application config expressions populated with formula, SOA grid structure and display
    format.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with the input
    structure.
    :var applConfigExprsWithDisplayString: List of application configuration expression populated with formula,  grid
    structure and display format.
    """
    clientId: str = ''
    applConfigExprsWithDisplayString: List[ApplConfigExprWithDisplayString] = ()


@dataclass
class ConvertVariantExpressionsResponse(TcBaseObj):
    """
    The response structure for the operation with the converted variant expressions and in required formats.
    
    :var outputs: The list of converted variant expressions.
    :var serviceData: Service Data
    """
    outputs: List[ConvertVariantExpressionOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetProductDefaultsConfigOutput(TcBaseObj):
    """
    The list of expressions that was validated and status of configuration along with required families.
    
    :var expressionWithDefaults: The list of output variant expressions that result from applying default rules to the
    input variant expressions.
    :var criteriaStatus: The status of the configuration. Valid values are: validAndComplete, validAndInComplete or
    inValid.  
    validAndComplete: all mandatory families in configuration have value selections.  
    validAndInComplete: not all mandatory families in configuration have value selections. 
    inValid: there are some violations.
    :var requiredFamilies: A list of mandatory families, which do not have any value selection based on input
    expression and default feature in the context.
    """
    expressionWithDefaults: BusinessObjectConfigExpression = None
    criteriaStatus: str = ''
    requiredFamilies: List[Cfg0AbsFamily] = ()


@dataclass
class GetProductDefaultsResponse(TcBaseObj):
    """
    The response structure for operation GetProductDefaults.
    
    :var outputs: The list of the output expressions that result from applying default constraints to the input
    expressions.
    :var serviceData: The service data to return any additional information.
    """
    outputs: List[GetProductDefaultsConfigOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetRevisionRulesResponse(TcBaseObj):
    """
    The list of applicable RevisionRule objects with the service data.
    
    
    
     
    
    :var applicableRevisionRules: The list of RevisionRule instances.
    :var serviceData: The teamcenter service data
    """
    applicableRevisionRules: List[RevisionRule] = ()
    serviceData: ServiceData = None


@dataclass
class GetVariantExpressionsResponse(TcBaseObj):
    """
    The response structure for operation 'getVariantExpressions'.
    
    :var configObjectExpressions: A list of structures each relating a business object to a set of configuration
    expressions.
    :var serviceData: The Teamcenter service data
    """
    configObjectExpressions: List[BusinessObjectConfigExpression] = ()
    serviceData: ServiceData = None


@dataclass
class ProductDefaultsInput(TcBaseObj):
    """
    Input structure for the getProductDefaults operation.
    
    :var applyDefaults: The default actions to apply. The parameter is a bitwise OR the following values: 
    - 0 - Indicates that defaults should not be applied 
    - 1 - Will enable application of defaults 
    - 2 - Ignore all derived defaults and only process fixed defaults 
    - 4 - Skip derived defaults whose applicability or product model condition is not fully and explicitly satisfied.
    For example, a default rule 'set W=10 if H=10' is skipped for the input expression 'L=10' because 'L=10' also
    includes configurations that don't satisfy the applicability condition, such as 'L=10 & H=20'.
    - 8 - Force partially satisfied derived defaults.
    
    
    :var expressionsToUpdate: The list of expressions for which defaults are requested to be applied.
    :var families: This is an optional parameter. If specified, the server returns defaults only for these families. If
    null, the server returns defaults for all families
    :var context: The Cfg0ConfiguratorPerspective instance to provide the  configurator context(s) and RevisionRule. It
    may also include configuration information e.g. a variant rule. Expression with Variant Rule is used as additional
    criteria for validation.
    """
    applyDefaults: int = 0
    expressionsToUpdate: List[BusinessObjectConfigExpression] = ()
    families: List[Cfg0AbsFamily] = ()
    context: Cfg0ConfiguratorPerspective = None


@dataclass
class RangeExpression(TcBaseObj):
    """
    An elemental expression literal that is used in a value range expression for a given family. 
    Note: Operator PS_variant_operator_is_equal is not supported (use 'ConfigExpressionTerm' structures for equality
    literals).
    
    
    :var operatorCode: The operator code by which the value should be used in variant expression.
    :var valueText: The string value of the feature.
    :var feature: This is an optional parameter. If specified, the server and client should use it. If null, the server
    and client should work with valueText. Specifies feature object to be used in an range expression.
    """
    operatorCode: int = 0
    valueText: str = ''
    feature: Cfg0AbsValue = None


@dataclass
class AvailableProductVariabilityInput(TcBaseObj):
    """
    It is the object containing input information required to compute the available product variability.
    
    :var criteriaExpression: The input criteria expression for which the available product variability is to be
    calculated.
    :var familiesToTest: The list of configuration families of which available features are requested.
    :var context: Configurator context details.
    :var applyConstraints: How to apply the constraints. The action is a bitwise OR the following values: 
    0: disable configurator constraint evaluation 
    1: enable configurator constraint evaluation 
    2: skip constraints if they only reference unset families 
    4: skip constraints that don&apos;t reference all configExpression families 
    8: report warnings in addition to errors 
    16: report informational messages 
    32: don&apos;t stop if a violation is encountered (use with care) 
    64: treat constraints with warning severity as if they had error severity.
    
    1024: skip criteria update based on validation rules (For example configurator exclusion rule). If this flag is not
    set then the operation will update the variant criteria after applying validation rules.
    
    2048: enable Availability Constraint evaluation. 
    """
    criteriaExpression: BusinessObjectConfigExpression = None
    familiesToTest: List[Cfg0AbsFamily] = ()
    context: Cfg0ConfiguratorPerspective = None
    applyConstraints: int = 0


@dataclass
class SetVariantExpressionInput(TcBaseObj):
    """
    'SetVariantExpressionInput' represents a single transaction and partial error boundary for setting expressions on a
    list of target business objects.
    
    :var businessObjectExpressions: The list of business objects and corrosponding expressions.
    :var revisionRule: The revision rule to use to retrieve the correct revisions of the option data referenced by the
    expressions.
    :var saveExpressions: The flag which indicates if the configuration expressions should be saved on the target
    objects or set as transient configuration expressions. If an transient configuration expression is create, then
    user need to save the target object explicitly.
    """
    businessObjectExpressions: List[BusinessObjectConfigExpression] = ()
    revisionRule: RevisionRule = None
    saveExpressions: bool = False


@dataclass
class ValidateProductConfigInput(TcBaseObj):
    """
    It is structure containing input information required to validate product configuration.
    
    :var applyConstraints: The constraint rules application. The parameter is a bitwise OR of the following values: 
    - 0: disable configurator constraint evaluation 
    - 1: enable configurator constraint evaluation 
    - 2: skip constraints if they only reference unset families 
    - 4: skip constraints that don't reference all Expression families 
    - 8: report warnings in addition to errors 
    - 16: report informational messages 
    - 32: Continue even if a violation is encountered 
    - 64: treat constraints with warning severity as if they had error severity.
    - 1024: skip criteria update based on validation rules (For example configurator exclusion rule). If this flag is
    not set then the operation will update the variant criteria after applying validation rules.
    - 2048: enable Availability Constraint evaluation.
    
    
    :var expressionsToValidate: The input criteria expression for which the validation is requested.
    :var context: The Cfg0ConfiguratorPerspective instance which provides the RevisionRule and the configurator context.
    """
    applyConstraints: int = 0
    expressionsToValidate: List[BusinessObjectConfigExpression] = ()
    context: Cfg0ConfiguratorPerspective = None
