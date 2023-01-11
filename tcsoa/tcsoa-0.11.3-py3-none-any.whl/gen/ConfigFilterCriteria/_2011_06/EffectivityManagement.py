from __future__ import annotations

from tcsoa.gen.BusinessObjects import ConfigurationFamily, POM_object, RevisionRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductInfo(TcBaseObj):
    """
    The ProductInfo structure represents product name and product namespace combination. This structure is interpreted
    as NULL if it has empty ( ) values for 'productName' and 'productNameSpace' parameters.
    
    :var productName: Specifies a product. A ('productName,productNamespace') tuple is used as a parameter in
    configurator service calls so to allow the configurator to resolve any ambiguity in effectivity condition
    parameters. Applications using this 'EffectivityManagement' service should define a mechanism to obtain an
    appropriate value for this parameter. For example, 'ApplicationModel' objects like Collaborative Design models
    (Cpd0CollaborativeDesign) make them available via properties 'mdl0config_product_name', and
    'mdl0config_prod_namespace.'
    :var productNameSpace: Specifies a namespace in which parameter 'productName' has a unique definition, e.g. a
    specific model year, or product type. A ('productName,productNamespace') tuple is used as a parameter in
    configurator service calls so to allow the configurator to resolve any ambiguity in effectivity condition
    parameters. Applications using this 'EffectivityManagement' service should define a mechanism to obtain an
    appropriate value for this parameter. For example, 'ApplicationModel' objects like Collaborative Design models
    (Cpd0CollaborativeDesign) make them available via properties 'mdl0config_product_name', and
    'mdl0config_prod_namespace.'
    """
    productName: str = ''
    productNameSpace: str = ''


@dataclass
class AvailableProductEffectivityResponse(TcBaseObj):
    """
    Response structure containing available product effectivity information.
    
    :var configExpressions: Vector of expressions specifying an available range of effectivity. Together they cover the
    range of availability over all families given in the input parameters 'familiesToTest' and (indirectly)
    'exprsToTest'.
    :var serviceData: Partial errors are returned in Service Data.
    """
    configExpressions: List[ConfigExpression] = ()
    serviceData: ServiceData = None


@dataclass
class RevRuleEffectivityCriteria(TcBaseObj):
    """
    The RevRuleEffectivityCriteria structure represents a revision rule along with its effectivity criteria and
    associated validation records. The RevRuleEffectivityCriteria structure is interpreted to be NULL if the following
    values are set for its parameters:
    - revisionRule: NULLTAG
    - primaryEffectivity: a NULL ConfigFormula structure with all its parameters set to empty strings
    - solveType: neg 1
    - validationRecords: empty vector
    
    
    
    :var revisionRule: The modified RevisionRule. This could be a transient copy.
    :var primaryEffectivity: Original unprocessed effectivity criteria, before effectivity configurator rules were
    applied.
    :var solveType: Indicates the type of solve that will be performed when using the effectivity criteria in
    configuration filters.
    :var validationRecords: Validation records related to the effectivity criteria
    """
    revisionRule: RevisionRule = None
    primaryEffectivity: ConfigFormula = None
    solveType: int = 0
    validationRecords: List[EffectivityValidationRecord] = ()


@dataclass
class RevRuleEffectivityCriteriaResponse(TcBaseObj):
    """
    Response structure containing Revision Rule Effectivity Criteria Infomation.
    
    :var effectivityCriteria: Vector of effectivity criteria structures.
    :var serviceData: Partial errors are returned in Service Data.
    """
    effectivityCriteria: List[RevRuleEffectivityCriteria] = ()
    serviceData: ServiceData = None


@dataclass
class ConfigExpression(TcBaseObj):
    """
    The 'ConfigExpression' structure is interpreted as 'NULL' if it has the following values:
    - subExpressions: an empty vector
    - value: a 'NULL' 'ConfigOption' structure
    - opCode: neg 1
    - formula: a 'NULL' 'ConfigFormula' structure
    - effectivityTable: an empty vector
    
    
    
    :var subExpressions: The list of sub expressions to be combined with 'opcode'. 'subExpressions' and value must not
    both be present. If neither 'subExpressions' nor 'value' are present, the expression is treated as the identity
    element for all 'opcode' values.
    :var value: The value to which 'opCode' compares. 'subExpressions' and value must not both be present. If neither
    'subExpressions' nor 'value' are present, the expression is treated as the identity element for all 'opcode' values.
    :var opCode: - The operation code such as 'or', and, or 'equal'. See '$TC_INCLUDE/ps/ps_tokens.h.'
    
    
    :var formula: If present, contains the configuration expression as a configuration formula.
    :var effectivityTable: If present, contains a representation of the configuration expression formatted as a table
    where each row represents one validity range.
    """
    subExpressions: List[ConfigExpression] = ()
    value: ConfigOption = None
    opCode: int = 0
    formula: ConfigFormula = None
    effectivityTable: List[EffectivityTableRow] = ()


@dataclass
class ConfigFormula(TcBaseObj):
    """
    The 'ConfigFormula' structure represents a formula string associated with a configuration expression in
    configurator syntax. The 'ConfigFormula' structure is considered NULL if it has following values set for its
    parameters:
    - formula: empty string ( )
    - productName: empty string ( )
    - productNameSpace: empty string ()
    
    
    
    :var formula: Formula string in a configurator specific encoding. Teamcenter configurators used in the
    EffectivityManagement service interface encode formula in Explicit Teamcenter Language.
    :var productName: Specifies a product (e.g. using its Item ID). May be used in conjunction with parameter
    'productNameSpace' when resolving ambiguity in effectivity option value names.
    :var productNameSpace: Namespace in which parameter 'productName' has a unique definition, e.g. an Item Revision
    ID, a Model Year, or a Product Type. May be used in conjunction with parameter 'productNameSpace' when resolving
    ambiguity in effectivity option value names.
    """
    formula: str = ''
    productName: str = ''
    productNameSpace: str = ''


@dataclass
class ConfigOption(TcBaseObj):
    """
    The ConfigOption structure represents a configuration option that is unique in the context of a configuration
    family. The ConfigOption structure is interpreted as "NULL" if it has the following values set for its parameters:
     - family: NULLTAG
     - name: empty string ("")
     - description: empty string ("")
    
    :var family: Namespace in which this option has unique semantics.
    :var name: Name of the option value. "" is treated as NULL, i.e., it does not match any criteria, not even other
    NULL values.
    :var description: Description of the option value.
    """
    family: ConfigurationFamily = None
    name: str = ''
    description: str = ''


@dataclass
class ConfigRuleViolation(TcBaseObj):
    """
    The ConfigRuleViolation structure represents a violated rule along with the message associated with rule violation.
    The ConfigRuleViolation structure is interpreted to be NULL if following values are set to its parameters:
    - message: empty string ( )
    - violatedCondition: a NULL ConfigExpression structure
    
    
    
    :var message: The text string associated with the rule violation.
    :var violatedCondition: The rule that was found to be violated.
    """
    message: str = ''
    violatedCondition: ConfigExpression = None


@dataclass
class ConfigurableProductsResponse(TcBaseObj):
    """
    Response structure containing Configurable Product Information.
    
    :var configurableProducts: List of configurable products defined in the effectivity configurator.
    :var serviceData: Partial errors are returned in ServiceData.
    """
    configurableProducts: List[ProductInfo] = ()
    serviceData: ServiceData = None


@dataclass
class DefaultRule(TcBaseObj):
    """
    The DefaultRule structure represents the details of the default expression that is applied to a config condition.
    The DefaultRule structure is interpreted to be NULL if it has following values set to its parameters:
    - partiallyApplicable: false
    - restrictiveCondition: a NULL ConfigExpression structure
    - appliedDefault: NULL ConfigExpression structure
    - appliedTo: NULL ConfigExpression structure
    
    
    
    :var partiallyApplicable: If true, the DefaultRule is only applicable to a subset of the criteria.
    :var restrictiveCondition: The condition under which the default is applicable. A NULL ConfigExpression structure
    indicates that the rule is always applicable.
    :var appliedDefault: The default that is applied, e.g., whenever restrictiveCondition is met.
    :var appliedTo: The configuration criteria before applying the default.
    """
    partiallyApplicable: bool = False
    restrictiveCondition: ConfigExpression = None
    appliedDefault: ConfigExpression = None
    appliedTo: ConfigExpression = None


@dataclass
class EffectivityCondition(TcBaseObj):
    """
    The EffectivityCondition structure is interpreted to be "NULL" if the following values are set to its parameters:
    formula: a "NULL" ConfigFormula structure (with all its parameters sets to empty strings); affectedElement: NULLTAG
    
    :var formula: Effectivity condition formula
    :var affectedElement: Product element on which the effectivity condition has been set
    """
    formula: ConfigFormula = None
    affectedElement: POM_object = None


@dataclass
class EffectivityConditionResponse(TcBaseObj):
    """
    Response structure returning a set effectivity expressions. The response structure is returned from multiple
    operations and needs to be interpreted depending on the context in which it is returned.
    
    :var effectivityConditions: A vector of effectivity condition structures where each element references the
    resulting effectivity condition and the corresponding object. The return vector does not necessarily need to
    correspond to the input vector by index as it may need to contain information about additional modified objects
    along with their new effectivity condition. This could be the result of effectivity propagation to sub elements.
    :var serviceData: Partial errors are returned in Service Data.
    """
    effectivityConditions: List[EffectivityCondition] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityExpressionsResponse(TcBaseObj):
    """
    Response structure returning a set effectivity expressions. The response structure is returned from multiple
    operations and needs to be interpreted depending on the context in which it is returned.
    
    :var effectivityExpressions: A vector of effectivity expressions. The response structure is returned from multiple
    operations and needs to be interpreted depending on the context in which it is returned.
    :var serviceData: Partial errors are returned in Service Data.
    """
    effectivityExpressions: List[ConfigExpression] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityFormulaeResponse(TcBaseObj):
    """
    Response structure returning a set configuration formulae in a configurator specific encoding. The response
    structure is returned from multiple operations and needs to be interpreted depending on the context in which it is
    returned.
    
    :var effectivityFormulae: A vector configuration formulae each representing one effectivity expression in a
    configurator specific encoding. The response structure is returned from multiple operations and needs to be
    interpreted depending on the context in which it is returned.
    :var serviceData: Partial errors are returned in Service Data
    """
    effectivityFormulae: List[ConfigFormula] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityTable(TcBaseObj):
    """
    The 'EffectivityTable' structure represents the set of validity ranges for a configuration expression.
    If 'EffectivityTables' for different expressions (e.g. Unit = 5 and Unit > 4 & Unit 'EffectivityTableRows' might be
    different, but will still be logically equivalent to the input expressions they correspond to.
    The following example illustrates 3 different logically equivalent 'EffectivityTable' structures. A given
    Teamcenter server session will consistently return one of them.
    
    - Unit=1..2 Date=Jan..Feb
    - Unit=1..2 Date=Feb..Mar
    - Unit=1..2 Date=Mar..Apr
    - Unit=2..3 Date=Mar..Apr
    - Unit=3..4 Date=Mar..Apr 
    
    
    
    The effectivity table above is equivalent to
    
    - Unit=1..2 Date=Jan..Apr
    - Unit=2..4 Date=Mar..Apr
    
    
    
    But it is also equivalent to
    
    - Unit=1..4 Date=Mar..Apr
    - Unit=1..2 Date=Jan..Mar
    
    
    
    The 'EffectivityTable' structure is interpreted to be NULL if the following values are set to its parameters:
    
    - 'effectivityTableRows': an empty vector
    
    
    
    :var effectivityTableRows: A vector of EffectivityTableRow structures each representing an effectivity range. Some
    ranges may overlap.
    """
    effectivityTableRows: List[EffectivityTableRow] = ()


@dataclass
class EffectivityTableRow(TcBaseObj):
    """
    The EffectivityTableRow structure represents a validity range. The following constants have special meaning:
    - January 2, 1900 12:00 AM UTC: Open Start Date
    - December 30, 9999 12:00 AM UTC: Open End Date
    - December 26, 9999 12:00 AM UTC: Stock Out
    - 1: Open Start Unit
    - 2147483647: Open End Unit
    - 2147483646: Stock Out
    
    
    Effect in as well as effect out points may have NULL values, which indicate no value assigned:
    -     Neg 1: no unit value assigned
    -     NULL date: no date value assigned
    
    
    The 'EffectivityTableRow' structure is interpreted as NULL if the following values are set:
    -     unitIn: Neg 1
    -     unitOut: Neg 1
    -     dateIn: a NULL date
    -     dateOut: a NULL date
    -     rest: a NULL 'ConfigFormula' structure
    
    
    
    :var unitIn: Unit at which this validity range starts.
    :var unitOut: Unit at which the validity range ends.
    :var dateIn: Date at which the validity range starts.
    :var dateOut: Date at which the validity range ends.
    :var rest: Effectivity conditions in this range that are neither date nor unit related.
    """
    unitIn: int = 0
    unitOut: int = 0
    dateIn: datetime = None
    dateOut: datetime = None
    rest: ConfigFormula = None


@dataclass
class EffectivityTablesResponse(TcBaseObj):
    """
    'EffectivityTablesResponse' structure
    
    :var effectivityTables: A vector of effectivity table structures each representing one effectivity expression.
    :var serviceData: Partial errors are returned in Service Data
    """
    effectivityTables: List[EffectivityTable] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivityValidationRecord(TcBaseObj):
    """
    The EffectivityValidationRecord structure represents validation results for effectivity criteria associated with a
    revision rule. The EffectivityValidationRecord structure is interpreted to be "NULL" if the following values are
    set to its parameters:
     - validationDate: a null date representing "0001-01-01T00:00:00Z" ("January 1, 0001, midnight, UTC")
     - validationResult: a "NULL" ConfigFormula structure with all its parameters set to empty strings
     - undeterminedFamilies: an empty vector
     - violations: an empty vector
     - appliedDefaults: an empty vector
    
    :var validationDate: Date at which the validation was performed.
    :var validationResult: Validation result after applying effectivity configurator rules.
    :var undeterminedFamilies: Families that are not set to a single value. If empty, the criteria are complete.
    :var violations: Violation records. If empty, the effectivity criteria are valid.
    :var appliedDefaults: One record for each applied default in the sequence they were applied
    """
    validationDate: datetime = None
    validationResult: ConfigFormula = None
    undeterminedFamilies: List[ConfigurationFamily] = ()
    violations: List[ConfigRuleViolation] = ()
    appliedDefaults: List[DefaultRule] = ()
