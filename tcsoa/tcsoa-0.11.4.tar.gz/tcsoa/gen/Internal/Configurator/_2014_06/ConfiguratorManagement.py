from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0AbsValue, Cfg0AbsFamily, Cfg0AbsAllocation, WorkspaceObject, POM_object, ImanQuery, TransferOptionSet, Cfg0AbsOptionValue, Cfg0SearchCursor, Cfg0AbsAssociation, Cfg0ConfiguratorPerspective, Cfg0AbsFamilyGroup, Cfg0AbsOptionFamily
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidateProductConfigOutput(TcBaseObj):
    """
    The output structure with the given input 'BusinessObjectConfigExpression' to 'validateProductConfiguration'
    operation and the list of violations for the given BusinessObjectConfigExpression. Each 'Volation' structure
    provides information about the rule which is violate with its severity and the error message.
    
    :var updatedExpression: Updated 'BusinessObjectConfigExpression' with values applied from inclusion rules of the
    given product item.
    :var violations: List of 'Violation' structures with rules and error messages.
    """
    updatedExpression: BusinessObjectConfigExpression = None
    violations: List[Violation] = ()


@dataclass
class ValidateProductConfigurationResponse(TcBaseObj):
    """
    The response structure for the operation 'ValidateProductConfiguration'
    
    :var serviceData: The service data for errors and returned objects.
    :var outputs: The list of expressions that was validated and updated with selections due to application of
    constraints.
    """
    serviceData: ServiceData = None
    outputs: List[ValidateProductConfigOutput] = ()


@dataclass
class ValueFilters(TcBaseObj):
    """
    A filter filtering rules for all features specified in this structure.
    
    :var valueIDs: List of value IDs (' cfg0object_id' ). If specified all values with matching criteria will be
    searched and will be used to filter rules. This parameter is mutually exclusive of 'values'.
    :var values: List of values. If specified values will be used to filter rules. This parameter is mutually exclusive
    of 'valueIds'.
    """
    valueIDs: List[str] = ()
    values: List[Cfg0AbsOptionValue] = ()


@dataclass
class VariantInfo(TcBaseObj):
    """
    A SOA structure representation of 'Cfg0BaseConfigurator'::'VaraintInfo'. This structure can be viewed as the
    serialization of the cache of variant data stored as a part of 'Cfg0BaseConfigurator'::'VaraintInfo'.
    
    :var lastUpdate: Last updated time of cache. Use this value to decide whether cache needs to be refreshed.
    :var variantOption: A collection of the option families and thier values associated with the variant cache of the
    item revision.
    :var validValueRanges: Collection of free from familiy value ranges associated with the item revision.
    :var defaultConditions: A collection of Expression (wrapper over Math::BooleanExpression) objects associated with
    the variant data. Default conditions are the combined expression of modelCondition, if any, and
    applicabilityCondition, if any, for each default rule, which need to be satisfied before the default value is
    applied to the expression.
    :var defaultExpressions: A collection of Expression (wrapper over Math::BooleanExpression) objects. Default
    expressions are the subject part of a default rules that would be applied on the input expression if default
    conditions are satisfied (earlier called derived defaults) or even without them (earlier called fixed defaults).
    :var ruleChecks: A collection of ConfiguratorConstraint objects that contain inclusion and exclusion rules defined
    on the variant data for this item revision.
    :var familyHash: The Map of pairs ( Cfg0AbsFamily, 'VariantOption' ) representing the family instance and its
    structure form.
    :var familyNameHash: A data structure comprising of map between the family name (as a key) and its family
    information (representation Math::VariantOption) as the value. Family name is used as the key in this map as
    against the fully qualified name used in familyHash.
    :var ruleCheckExpressions: Rule check expression is the combined boolean expression of all the inclusion and
    exclusion rules defined on the variant data associated with this item revision.
    """
    lastUpdate: datetime = None
    variantOption: List[VariantOption] = ()
    validValueRanges: List[Expression] = ()
    defaultConditions: List[Expression] = ()
    defaultExpressions: List[Expression] = ()
    ruleChecks: List[ConfiguratorConstraint] = ()
    familyHash: FamilyHash = None
    familyNameHash: FamilyNameHash = None
    ruleCheckExpressions: Expression = None


@dataclass
class VariantOption(TcBaseObj):
    """
    Varaint option is a wrapper over Math::VariantOption, an internal representation that holds the variant data
    associated with this item revision. Data from 'Math'::'VariantOption' would be transfered into the 'VariantOption'
    SOA structure during serialization and converted back into 'Math'::'VaraintOption' during de-serialization.
    
    :var optionNamespace: Option namespace
    :var name: Name of the option
    :var description: User entered description value of this option.
    :var tag: Concatenated value of the format dict.familyname{operator}value
    :var valueDataType: Data type of this family. Valid values for this parameter are defined by the ListOfValues
    "Cfg0FamilyValueDataType".
    :var uom: Unit of measure associated with this option.
    """
    optionNamespace: str = ''
    name: str = ''
    description: str = ''
    tag: str = ''
    valueDataType: str = ''
    uom: str = ''


@dataclass
class VariantRuleInput(TcBaseObj):
    """
    A structure that provides information required to create or update a variant rules.
    
    :var expressions: The list of variant expressions to set on the variant rule.
    :var saveRule: Indicates whether the rule should be saved before returning. If the value is FALSE a transient
    variant rule will be returned. Transient variant rules and transient variant rule changes are discarded at the end
    of the Teamcenter session unless they are explicitly saved in a separate operation.
    :var ruleToUpdate: If specified the expression on this rule is updated with the input expression; to create a new
    rule this param is set to null.
    :var creInputs: A map that ties properties to their values for the new rule.
    :var relationName: The relationship name to use when associating the variant rule to the object specified in
    parameter "'referenceObject'". This is an optional parameter. If specified a relationship of this type is used to
    associate the variant rule to the reference object. A NULL value causes the default relationship name to be used as
    specified in preference "TC_Default_SVR_Relationship".
    :var referenceObject: When specified the newly created rule is related to the given reference object.
    """
    expressions: List[ConfigExpression] = ()
    saveRule: bool = False
    ruleToUpdate: POM_object = None
    creInputs: CreateInput = None
    relationName: str = ''
    referenceObject: WorkspaceObject = None


@dataclass
class VariantRuleOutput(TcBaseObj):
    """
    Output structure for each 'VariantRuleInput' in 'createUpdateVariantRules' operation
    
    :var index: Specifies the corresponding variant rule input index.
    :var ruleObject: An object that carries variant configuration criteria.
    :var variantExpression: The list of  variant expressions that represent the variant configuration criteria
    associated with this object.
    """
    index: int = 0
    ruleObject: POM_object = None
    variantExpression: List[ConfigExpression] = ()


@dataclass
class Violation(TcBaseObj):
    """
    Represents a violated rule along with the message and severity associated with rule violation.
    
    :var message: The message to display if this rule is violated.
    :var severity: The severity associated with the message. Valid values for this parameter are defined by the
    ListOfValues "Cfg0ConstraintSeverity".
    :var violatedRule: The rule that was found to be violated.
    """
    message: str = ''
    severity: str = ''
    violatedRule: ConfigExpression = None


@dataclass
class BusinessObjectConfigExpression(TcBaseObj):
    """
    Relates a business object (e.g. Cpd0DesignElement, VariantRule, or Cfg0ExcludeRule) to a list of configuration
    expressions.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var targetObject: The business object (e.g. Cpd0DesignElement, VariantRule, or Cfg0ExcludeRule), to which the
    configuration expressions specified in parameter 'expressions' are linked.
    :var expressions: The list of expressions related to the business object specified in parameter 'targetObject'. The
    list of suported expression categories varies from business object type to business object type. The expression
    category is specified with the expressionType parameter in each expression.
    """
    clientId: str = ''
    targetObject: POM_object = None
    expressions: List[ConfigExpression] = ()


@dataclass
class ConfigExpression(TcBaseObj):
    """
    Defines a Boolean expression to be used for configuration purposes.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var expressionType: Specifies the expression category and the intent of this expression. 
    
    The valid values are as follows:
    - 25 - Applicability
    - 28 - Inclusive Constraint
    - 29 - Exclusive Constraint
    - 33 - Product Model
    - 37 - Default Rule
    
    
    :var formula: The persistent formula string in Teamcenter syntax (see documentation for property
    ''cfg0SubjectCondition'' or BOMLine property ''bl_formula'').
    :var subExpressions: Represents a list of sub-expressions in a Boolean expression. The sub-expressions in this list
    are combined with logical operator 'OR'.
    """
    clientId: str = ''
    expressionType: int = 0
    formula: str = ''
    subExpressions: List[ConfigSubExpression] = ()


@dataclass
class ConfigExpressionDisplayStringInput(TcBaseObj):
    """
    An input structure defining the expressions for which the display format is requested.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var expressions: The expressions for which the display format is requested.
    """
    clientId: str = ''
    expressions: List[ConfigExpression] = ()


@dataclass
class ConfigExpressionDisplayStringOutput(TcBaseObj):
    """
    Output structure returned by operation getVariantExpressionDisplayStrings. It contains the list of display strings
    for the input expressions.
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var expressionStrings: The display strings for each input expression.
    """
    clientId: str = ''
    expressionStrings: List[str] = ()


@dataclass
class ConfigExpressionGroup(TcBaseObj):
    """
    This structure groups 'ConfigExpressionTerm' structures. A mixture of positive and negated expression terms in the
    same expression group is not allowed.  Positive terms within an expression group are combined with operator 'OR',
    e.g. Color=Red | Color=Green. Negated terms within an expression group are combined with operator 'AND', e.g.
    Color!=Red & Color!=Green
    
    :var groupName: The name for the group containing the expression terms. If the group name is provided as FALSE with
    empty term expressions then group expression would be considered as FALSE. If the group name is provided as TRUE
    with empty term expressions then group expression would be considered as TRUE.
    :var terms: List of ConfigExpressionTerm structures
    """
    groupName: str = ''
    terms: List[ConfigExpressionTerm] = ()


@dataclass
class ConfigExpressionTerm(TcBaseObj):
    """
    Defines an elemental expression literal for a single feature, or feature range expression for a given family.
    
    :var familyNamespace: The option family namespace. This parameter is mutually exclusive with parameter 'value'.
    When this structure is used in a request, this parameter is ignored if a valid family business object is specified
    in parameter 'family'
    :var familyID: The ID of the family in the term. This parameter is mutually exclusive with parameter 'value'. When
    this structure is used in a request, this parameter is ignored if a valid family business object is specified in
    parameter 'family'
    :var operatorCode: The operator code to use for this expression terms.
    The Valid values are as follows:
    - 5 - Equals
    - 6 - Not Equals
    - 10 - And
    - 11 - OR
    
    
    :var valueText: The ID of the feature object or the feature to use for a free form family. This parameter is
    mutually exclusive with parameters 'family' and 'rangeExpressions'. It is recommended to author variant conditions
    involving free form features by using inequation operators in parameter 'rangeExpressions'. Equality condition for
    free form features should only be used in variant configuration criteria. In that case parameter 'valueText' may be
    used to specify a free form feature. When this structure is used in a request, this parameter is ignored if a valid
    feature business object is specified in parameter 'value'.
    :var rangeExpressions: A list of elemental expression literals describing a value range for a given family. This
    parameter requires a family to be specified with parameters 'familyNamespace' and 'familyID', or 'family'. This
    parameter is mutually exclusive with parameter 'value'.
    :var family: Specifies family object to be used in a free form family expression term, or a feature range
    expression. This parameter is mutually exclusive with parameter 'value'.
    :var value: Specifies feature object to be used in an elemental expression literal. This parameter is mutually
    exclusive with parameters 'family' and 'rangeExpressions'.
    """
    familyNamespace: str = ''
    familyID: str = ''
    operatorCode: int = 0
    valueText: str = ''
    rangeExpressions: List[RangeExpression] = ()
    family: Cfg0AbsFamily = None
    value: Cfg0AbsValue = None


@dataclass
class ConfigSubExpression(TcBaseObj):
    """
    This structure groups 'ConfigExpressionGroup' structures which are joined together by "AND" operator.
    
    :var expressionGroups: Represents a list of clauses in a Boolean expression. The clauses in this list are combined
    with logical operator AND.
    """
    expressionGroups: List[ConfigExpressionGroup] = ()


@dataclass
class ConfiguratorConstraint(TcBaseObj):
    """
    A SOA structure representation of Teamcenter::ConfiguratorConstraint. The data members of this SOA structure
    correspond the Teamcenter runtime objects in namespace Teamcenter::Math. For example, a
    ConfigurationManagement::VaraintOption corresponds to a Math::VariantOption.
    
    :var modelDesignator: Text representation of model condition defined on a rule.
    :var applicability: Text representation of applicability condition defined on a rule.
    :var restriction: Text representation of subject condition defined on a rule.
    :var comment: User entered message on the rule. This string is a localizable string which is displayed to the user
    when any rule execution fails.
    :var modelOptions: A list of Variation families that are associated with the model condition of a rule.
    :var applicabilityOptions: A collection of Variation families that are associated with the applicability condition
    of a rule.
    :var restrictionOptions: A collection of Variation families that are associated with the subject condition of a
    rule.
    :var ruleOptions: A unique collection of all the families, model, applicability and subject, that are contained
    within this constraint object.
    :var constraintType: The type of constraint.
    Valid values for this parameter are as follow:
    - IncludeConstraint: A constraint rule that is used to validate and possibly modify the configuration criteria.
    Validation fails whenever adding the condition of this constraint rule with operator AND would result in
    unsatisfiable configuration criteria. If the scope of the input variant criteria exceeds the scope of the
    constraint rule condition, the scope is reduced to stay within the bounds of the constraint rule scope by ANDing
    the rule condition to the configuration criteria.
    
    
    
    - ExcludeConstraint: A constraint rule that is used to validate configuration criteria without modifying it.
    Validation fails when the configuration criteria satisfy the condition of this constraint rule.
    
    
    :var constraintSeverity: The severity associated with the message. Valid values for this parameter are defined by
    the ListOfValues "Cfg0ConstraintSeverity".
    """
    modelDesignator: Expression = None
    applicability: Expression = None
    restriction: Expression = None
    comment: str = ''
    modelOptions: List[VariantOption] = ()
    applicabilityOptions: List[VariantOption] = ()
    restrictionOptions: List[VariantOption] = ()
    ruleOptions: List[VariantOption] = ()
    constraintType: str = ''
    constraintSeverity: str = ''


@dataclass
class CreateInput(TcBaseObj):
    """
    This structure captures the inputs required for creation of a business object. It is a nested structure containing
    the 'CreateInput'(s) for any secondary(compounded) objects that might be created (e.g Item also creates
    ItemRevision and ItemMaster Form, etc.). This structure should only be used for purposes specific to this Service
    Interface, e.g. when creating transient VariantRules. Generally business objects should be created with the
    DataManagement Service Interface.
    
    :var boName: Business object type name
    :var stringProps: Map of string property names to values ('string, string')
    :var doubleArrayProps: Map of double array property names to values map( string, double)
    :var floatProps: Map of float property names to values (string, bool)
    :var floatArrayProps: Map of float array property names to values map( string, float)
    :var objectProps: Map of BusinessObject property names to values ('string, BusinessObjec't)
    :var objectArrayProps: Map of BusinessObject array property names to values ('string, vector<BusinessObject>')
    :var compoundCreateInput: Map of reference or relation property name to secondary 'CreateInput' objects '(string,
    vector<CreateInput>')
    :var stringArrayProps: Map of string array property names to values ('string, vector<string>')
    :var boolProps: Map of boolean property names to values (string, bool)
    :var boolArrayProps: Map of boolean array property names to values ('string, vector<bool>')
    :var dateProps: Map of DateTime property names to values ('string, DateTime')
    :var dateArrayProps: Map of DateTime array property names to values ('string, vector<DateTime>')
    :var intProps: Map of integer property names to values (string, int)
    :var intArrayProps: Map of ineteger array property names to values map( string, int)
    :var doubleProps: Map of double property names to values (string, double)
    """
    boName: str = ''
    stringProps: StringMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    objectProps: TagMap = None
    objectArrayProps: TagVectorMap = None
    compoundCreateInput: CreateInputMap = None
    stringArrayProps: StringVectorMap = None
    boolProps: BoolMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None
    doubleProps: DoubleMap = None


@dataclass
class CreateUpdateVariantRulesResponse(TcBaseObj):
    """
    Response structure for the 'createUpdateVariantRules' operation.
    
    :var ruleOutputs: List of variant rule output structures
    :var serviceData: Service Data
    """
    ruleOutputs: List[VariantRuleOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DeclaredFamily(TcBaseObj):
    """
    A SOA structure representation of 'Teamcenter'::'ConfigurationFamilyFactory'::'DeclaredFamily'.
    
    :var family: SOA representation of Math::VaraintOption that defines an family.
    :var valueRange: A SOA expression representation of valueRange, Math::BooleanExpression, present in
    Teamcenter::ConfigurationFamilyFactory::DeclaredFamily.
    :var values: The map of values in pairs of (string, string) for family and feature.
    :var variantMode: A SOA representation of variantMode data member in
    Teamcenter::ConfigurationFamilyFactory::DeclaredFamily.
    """
    family: VariantOption = None
    valueRange: Expression = None
    values: StringVariantOptionMap = None
    variantMode: int = 0


@dataclass
class Expression(TcBaseObj):
    """
    A SOA structure that represents the 'Math'::'BooleanExpression' as a text. The collection of these text expressions
    in the vector is the output returned from 'Cfg'::'expressionsAsStrings'(). The string representation can be
    converted back into 'Math'::'BooleanExpression' by invoking 'Cfg'::'getExpressions'().
    
    :var id: A unique ID associated with this expression structure. Note: Currently this attribute is unused. The main
    intention of using this id is to be able to reduce the data over the wire by serializing only one Expression
    structure and leverage this ID wherever it is used.
    :var asTextExpression: Text representation of Math::BooleanExpression returned from Cfg::expressionsAsStrings().
    """
    id: int = 0
    asTextExpression: List[str] = ()


@dataclass
class ExpressionGroupInput(TcBaseObj):
    """
    Aggregates multiple search criteria into complex search expressions.
    
    :var clientId: Identifies this structure within the scope of an operation. The identifier allows this structure to
    be referenced from other search definition input strructures in the same operation, e.g. this structure could be
    referenced from within an enclosing ExpressionGroupInput structure.
    :var searchOperator: The set operator to use when combining the results from each search definition in this group.
    Possible values are:
    - "UnionAll"
    - "UnionUnique"
    - "Intersection"
    - "Difference"
    
    
    Use "UnionAll" if search results are not expected to contain duplicates, or if duplicates are not a concern. The
    search expressions in this group are combined in the sequence in which they appear in the group.
    
    "UnionAll" and "UnionUnique" combine the results of two search definitions into a set that contains all of the
    objects that are returned from either the left or the right search definition operand. "UnionAll" does not remove
    duplicates and is therefore often faster.
    
    "Intersection" combines the results of two search definitions into a set that contains all of the objects that are
    returned from the left as well as the right search definition operand.
    
    "Difference" combines the results of two search definitions into a set that contains all of the objects that are
    returned from the left but not from the right search definition operand.
    
    Search definitions constructed from a 'ResultTypeInput' are always combined with "Intersection".
    
    Exclude search definitions constructed from a 'ObjectReferenceInput' are always combined with "Difference".
    
    Include search definitions constructed from a 'ObjectReferenceInput' are combined with "UnionAll" if the set
    operator for the group is "UnionAll", otherwise with "UnionUnique".
    
    For example, a "UnionAll" group that combines the following search definitions:
    - "savedQuery"
    - "includeObjects"
    - "resultTypes"
    - "excludeObjects"
    
    
    would return:
    $savedQuery UnionAll $includeObjects Intersection $resultTypes Difference $excludeObjects.
    :var expressionIds: The list of client Ids of the search expressions to combine in this group. Any client ID that
    is assigned to a search definition input structure within the same 'SearchExpressionInput' can be used, including
    other 'ExpressionGroupInput' client ID values. For example you could specify two client ID values that are given in
    the "'savedQueries'" parameter of the SearchExpressionInput that also contains this 'ExpressionGroupInput'
    structure if you want to intersect or union the results from these two searches. Or you could combine one of the
    client ID values in parameter "'savedQueries'" with one of the ID values in parameter "'excludeObjects'" if you
    want to explicitly remove some objects from the search results of the saved query. This 'ExpressionGroupInput' then
    forms a new search criterion as a combination of the results from the search definitions that are referenced in
    this list.
    :var settings: Search pragmata, which describe how the server should should process the input. 
    Note: Support for search pragmata is not implemented in Teamcenter 10.1.2.
    """
    clientId: str = ''
    searchOperator: SearchGroupOperator = None
    expressionIds: List[str] = ()
    settings: SettingsMap = None


@dataclass
class ExpressionJoinCondition(TcBaseObj):
    """
    Defines the join condition for the results of two searches.
    An 'ExpressionJoinCondition' with values
    - left=2
    - operatorCode=1500
    - right=3
    
    
    defines a join condition between values in the 2nd column of the left and the 3rd column of the right search using
    the EQUAL comparison operator.
    
    :var left: The index of the column in the left search in this join.
    :var operatorCode: The operator to use in this join condition when matching the columns in the left and right
    search. Supported operators are:
    - 15000 (POM_enquiry_equal)
    
    
    :var right: The index of the column in the right search in this join.
    """
    left: int = 0
    operatorCode: int = 0
    right: int = 0


@dataclass
class ExpressionJoinInput(TcBaseObj):
    """
    Combines multiple search criteria into a single search expression returning a result table with multiple columns.
    
    :var clientId: Identifies this structure within the scope of an operation. The identifier allows this structure to
    be referenced from other search definition input strructures in the same operation, e.g. this structure could be
    referenced from within an enclosing ExpressionGroupInput structure.
    :var searchOperator: The join operator to use when combining the results from each search definition in this join.
    :var expressionIds: The list of client Ids of the search expressions to combine in this join. Any client ID that is
    assigned to a search definition input structure within the same 'SearchExpressionInput' can be used, including
    other 'ExpressionJoinInput' client ID values. For example you could specify two client ID values that are given in
    the "'savedQueries'" parameter of the 'SearchExpressionInput' that also contains this 'ExpressionGroupInput'
    structure if you want to join the results from these two searches. Or you could combine one of the client ID values
    in parameter "savedQueries" with one of the ID values in parameter "'includeObjects'" if you want to explicitly
    join some objects from the search results of the saved query. This 'ExpressionJoinInput' then forms a new search
    criterion as a combination of the results from the search definitions that are referenced in this list.
    :var settings: Search pragmata, which describe how the server should should process the input.
    Note: Support for search pragmata is not implemented in Teamcenter 10.1.3.
    :var joinConditions: Defines the join condition to use when joining the 1st search in parameter "'expressionIds'"
    with the other searches parameter "'expressionIds'".
    Teamcenter 10.1.3 only support one single join condition.
    """
    clientId: str = ''
    searchOperator: SearchJoinOperator = None
    expressionIds: List[str] = ()
    settings: SettingsMap = None
    joinConditions: List[ExpressionJoinCondition] = ()


@dataclass
class FamilyFilters(TcBaseObj):
    """
    A filter filtering rules for all features belonging to all families specified in this structure.
    
    :var familyIDs: List of family IDs ( 'cfg0object_id' ). If specified all families with matching criteria will be
    searched and values belongs to searched families will be used to filter rules. This parameter is mutually exclusive
    of 'families'.
    :var families: List of families. If specified values belongs to all families will be used to filter rules. This
    parameter is mutually exclusive of 'familyIds'.
    """
    familyIDs: List[str] = ()
    families: List[Cfg0AbsOptionFamily] = ()


@dataclass
class FilterCriteria(TcBaseObj):
    """
    Criteria that allows filtering rule objects. The filter criteria can be given in the following ways:
    - If 'groupFilters' is populated, then the system shall find all groups within the current context that match the
    filter and find rules that reference all features within families of the group.
    - If 'familyFilters' is populated, then the system shall find all families within the current context that match
    the filter and find rules that reference all features within the families.
    - If 'valueFilters' is populated, then the system shall find all features within the current context that match the
    filter and find rules that reference the features.
    - Criteria within multiple fields are intersected.
    
    
    
    :var groupFilters: Filter for filtering based on all features belonging to families in specified groups.
    :var familyFilters: Filter for filtering based on all features belonging to families specified.
    :var valueFilters: Filter for filtering based on all features specified.
    :var includeUnreferencedRules: This parameter determines whether or not rules that do not have any variant
    expressions set on them be returned or not.
    
    If this parameter is set to 'true', all such rules would be returned. If this parameter is set to 'false', such
    rules are not returned.
    """
    groupFilters: GroupFilters = None
    familyFilters: FamilyFilters = None
    valueFilters: ValueFilters = None
    includeUnreferencedRules: bool = False


@dataclass
class GetDisplayStringResponse(TcBaseObj):
    """
    Response structure for 'getVariantExpressionDisplayStrings' operation
    
    :var displayStrings: List of display strings for the input expressions
    :var serviceData: Service Data
    """
    displayStrings: List[ConfigExpressionDisplayStringOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetFamilyGroupResponse(TcBaseObj):
    """
    Response structure to return allocated groups and their corresponding allocation objects.
    
    :var groupAndAllocation: The Map of ( Cfg0AbsFamilyGroup, Cfg0AbsAssociation) having a family group to the
    corresponding allocation objects for the product item.
    :var serviceData: Teamcenter Service Data.
    """
    groupAndAllocation: GroupAllocationMap = None
    serviceData: ServiceData = None


@dataclass
class GetOptionFamiliesResponse(TcBaseObj):
    """
    A list of structures consisting of family groups and families that are attached to the respective family groups.
    
    :var groupAndFamilies: List of structure with the family groups and families associated with them. A
    'GroupAndFamilies' structure describes an instance of family group and the families which are associated with it.
    :var serviceData: Teamcenter service data.
    """
    groupAndFamilies: List[GroupAndFamilies] = ()
    serviceData: ServiceData = None


@dataclass
class GetOptionValuesResponse(TcBaseObj):
    """
    A list of structures having families and features of the respective families.
    
    :var valueAndAssocations: This is the map of feature objects and their corresponding association objects with the
    product item or the product model. The product item and the product model is associated with a features by an
    allocation object and an availability object, respectively.
    :var serviceData: Teamcenter service data.
    """
    valueAndAssocations: ValueAssociationMap = None
    serviceData: ServiceData = None


@dataclass
class GetProductDefaultsResponse(TcBaseObj):
    """
    The response structure for operation 'GetProductDefaults'
    
    :var expressionsWithDefaults: Contains the output expression that result from aplying default rules to the input
    expressions.
    :var serviceData: The service data to return any additional information.
    """
    expressionsWithDefaults: List[BusinessObjectConfigExpression] = ()
    serviceData: ServiceData = None


@dataclass
class GetVariantCacheInfoResponse(TcBaseObj):
    """
    Revision configured variant data for the given product 'context' item revision.
    
    :var variantInfo: Contains revision configured variant data such as variant features, families, and rules.
    :var serviceData: Service data of teamcenter.
    """
    variantInfo: VariantInfo = None
    serviceData: ServiceData = None


@dataclass
class GroupAndFamilies(TcBaseObj):
    """
    The structure with the family group and its associated families.
    
    :var familyGroup: A family group object.
    :var familyAndAssociation: The Map of ( Cfg0AbsFamilyGroup, Cfg0AbsAssociation)  having a family group to the
    corresponding allocation objects for the product item.
    """
    familyGroup: Cfg0AbsFamilyGroup = None
    familyAndAssociation: FamilyAssociationMap = None


@dataclass
class GroupFilters(TcBaseObj):
    """
    A filter structure specifying filtering rules for all option values belonging to all families to group.
    
    :var groupIDs: List of group IDs ( 'cfg0object_id' ). If specified all groups with matching criteria will be
    searched and values belongs to all families in searched groups will be used to filter rules. This parameter is
    mutually exclusive of 'groups'.
    :var groups: List of groups. If specified values belongs to all families in groups will be used to filter rules.
    This parameter is mutually exclusive of 'groupIds'.
    """
    groupIDs: List[str] = ()
    groups: List[Cfg0AbsFamilyGroup] = ()


@dataclass
class ObjectReferenceInput(TcBaseObj):
    """
    Represents a list of object to by explicitly included in, or explicitly excluded from, the search results.
    
    
    :var clientId: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var objects: Reference to a list of POM_Object objects used to create the include or exclude search expression.
    :var resultColumns: A list of additional columns to return in the search result. This search definition uses a
    predefined result table column for attribute "puid" at index 0. This parameter can be used to define additional
    columns to be returned in the result table for this search table.
    """
    clientId: str = ''
    objects: List[POM_object] = ()
    resultColumns: List[SearchResultTableColumn] = ()


@dataclass
class ProductDefaultsInput(TcBaseObj):
    """
    Input structure for the 'getProductDefaults' operation
    
    :var applyDefaults: Indicates whether or not to apply defaults. The parameter value is a bit pattern specifying one
    or more of the following: 
    0 - indicates that defaults should not be applied 
    1 - will enable application of defaults 
    2 - ignore all derived defaults and only process fixed defaults 
    4 - skip derived defaults whose applicability or product model condition is not fully and explicitly satisfied. For
    example, a default rule 'set W=10 if H=10' is skipped for the input expression 'L=10' because 'L=10' also includes
    configurations that don't satisfy the applicabliity condition, such as 'L=10 & H=20'.
    8 - force partially satisfied derived defaults. For example, applying a default rule 'set W=10 if H=10' to an input
    expression 'L=10' results in 'W=10 & H=10 & L=10'
    :var expressionsToUpdate: The expressions for which defaults are requested to be applied.
    :var families: This is an optional parameter. If specified, the server returns defaults only for these families. If
    null, the server returns defaults for all families.
    :var context: An Cfg0ConfiguratorPerspective object to provide input data which includes product item(s), product
    model(s). It may also include configuration information e.g. a revision rule and/or a variant rule.
    """
    applyDefaults: int = 0
    expressionsToUpdate: List[BusinessObjectConfigExpression] = ()
    families: List[Cfg0AbsFamily] = ()
    context: Cfg0ConfiguratorPerspective = None


@dataclass
class RangeExpression(TcBaseObj):
    """
    An elemental expression literal that is used in a value range expression for a given family.
    Supported operators are (see ):
     - PS_variant_operator_not_equal
     - PS_variant_operator_gt
     - PS_variant_operator_lt
     - PS_variant_operator_gt_eq
     - PS_variant_operator_lt_eq
    Operator PS_variant_operator_is_equal is not supported (use ConfigExpressionTerm structures for equality literals).
    
    :var operatorCode: Operator Code
    :var valueText: The ID of the feature object or the feature to use for a free form family.
    """
    operatorCode: int = 0
    valueText: str = ''


@dataclass
class ResultTypeInput(TcBaseObj):
    """
    Defines a search result filter based on a list of business object types. The search results of the enclosing
    ConfigExpressionGroup are limited to objects that match one of the given businesses object types, or one of their
    sub types. Search definitions enclosed in a ConfigExpressionGroup that are constructed from a ResultTypeInput are
    combined with operation "Intersection". ResultTypeInput can also be used to perform a SELECT operation on a list of
    business object type, or their subtypes tables. As the result could sometimes be very large, user can filter the
    result by providing a where clause condition. You can refer to the description of SearchPredicateParameters.
    
    :var clientId: Identifies this structure within the scope of an operation. The identifier allows this structure to
    be referenced from other search definition input strructures in the same operation, e.g. this structure could be
    referenced from within an enclosing ExpressionGroupInput structure.
    :var searchResultObjectTypes: List of the search result type names. The search will filter out objects that don't
    match any of the business object types in this list, or their sub types.
    :var resultColumns: A list of additional columns to return in the search result. This search definition uses a
    predefined result table column for attribute "puid" at index 0. This parameter can be used to define additional
    columns to be returned in the result table for this search table.
    :var predicateClauseParameters: A list of WHERE clause parameters to filter this ResultType search definition.
    Adding a WHERE clause can significantly improve the performance, especially when the corresponding database tables
    are large.
    """
    clientId: str = ''
    searchResultObjectTypes: List[str] = ()
    resultColumns: List[SearchResultTableColumn] = ()
    predicateClauseParameters: List[SearchPredicateParameters] = ()


@dataclass
class SavedQueryExpressionInput(TcBaseObj):
    """
    Defines a search based on a saved query that was created in the Teamcenter QueryBuilder application.
    
    :var clientId: Identifies this structure within the scope of an operation. The identifier allows this structure to
    be referenced from other search definition input strructures in the same operation, e.g. this structure could be
    referenced from within an enclosing ExpressionGroupInput structure.
    :var entries: The list of entry names specified in the saved query for which values are specified in parameter
    'values'.
    :var values: The list of values for the specified entries. Wild card characters are supported as documented for the
    Teamcenter QueryBuilder application.
    :var savedQuery: A saved query object that was created in the Teamcenter QueryBuilder application (or its
    corresponding APIs).
    :var resultColumns: A list of additional columns to return in the search result. This search definition uses a
    predefined result table column for attribute "puid" at index 0. This parameter can be used to define additional
    columns to be returned in the result table for this search table.
    """
    clientId: str = ''
    entries: List[str] = ()
    values: List[str] = ()
    savedQuery: ImanQuery = None
    resultColumns: List[SearchResultTableColumn] = ()


@dataclass
class SearchExpressionInput(TcBaseObj):
    """
    Describes the search criteria for the search operation
    
    :var traversals: Input structures to define traversal expressions. Teamcenter 10.1.2 does not support traversal
    expressions.
    :var excludeObjects: A list of search definitions for objects that explicitly excluded from the search results.
    Exclude lists are not subject to context filtering according to the product context items and product models in the
    'Cfg0ConfiguratorPerspective'. Exclude search definitions are always combined with operator "Difference", even if
    they are contained in a "UnionAll" group search definition.
    :var includeObjects: A list of search definitions for objects that explicitly included to the search results.
    Include lists are subject to context filtering according to the product context items and product models in the
    Cfg0ConfiguratorPerspective. Include search definitions that are contained in a "UnionAll" group search definition
    are combined with operator "UnionAll", all other include search definitions are combined with operator
    "UnionUnique" even if they are contained in a "Difference" group search definition.
    :var savedQueries: Input structures to construct search definitions based on saved queries. Each saved query search
    definitions references a saved query object along with a list of entries and values. Multiple values for a given
    entry need to be separated according to preference 'WSOM_find_list_separator'. The values support the standard
    Teamcenter saved query wildcards characters.
    :var expressionGroups: Input structures for constructing group search definitions. The input for a group search
    definition may contain references to other group search definitions for as long as the referencee precedes the
    referencer in this list. Group search definitions can be used to aggregate search criteria for complex searches.
    :var expressionJoins: Input structures for constructing join search definitions. Join search definitions can be
    used to combine multiple search criteria into a single search expression returning a result table with multiple
    columns.
    The input for a join search definition may contain references to other join search definitions for as long as the
    referencee precedes the referencer in this list.
    :var resultTypes: Input structure to define result type filter definitions. When applied to a search the result
    will contain only objects that match one of the business object type names listed in the applied 'ResultTypeInput',
    or one of their sub types.
    """
    traversals: List[TraversalExpressionInput] = ()
    excludeObjects: List[ObjectReferenceInput] = ()
    includeObjects: List[ObjectReferenceInput] = ()
    savedQueries: List[SavedQueryExpressionInput] = ()
    expressionGroups: List[ExpressionGroupInput] = ()
    expressionJoins: List[ExpressionJoinInput] = ()
    resultTypes: List[ResultTypeInput] = ()


@dataclass
class SearchOptions(TcBaseObj):
    """
    Search options for a given search, such as load count and sort criteria.
    
    :var defaultLoadCount: The number of objects to return in the initial batch of search results. The rest of them
    could be retrieved by calling fetchNextSearchResults. A defaultLoadCount of zero will return all the results found.
    :var sortAttributes: A list of attribute names of the class being searched based on which the results are sorted.
    The position of an attribute in this list defines its precedence ranking with respect to sorting. The result is
    first sorted based on the first attribute in this list.
    :var sortOrder: order in which results are sorted
    """
    defaultLoadCount: int = 0
    sortAttributes: List[str] = ()
    sortOrder: List[SortOperator] = ()


@dataclass
class SearchPredicateParameters(TcBaseObj):
    """
    A list of WHERE clause parameters to filter ResultType search definition. Adding a WHERE clause can significantly
    improve the performance, especially when the corresponding database tables are large.
    
    :var attribute: The name of the Column on which the where condition is to be applied.
    :var valueObjects: The list of Input value objects to be evaluated in the results, this forms the predicate
    condition.
    :var predicateOperator: The Predicate condition operator. The supported operators for this parameter are:
    - 15000 (POM_enquiry_equal)
    - 15005 (POM_enquiry_not_equal)
    - 16501 (POM_enquiry_in)
    - 16502 (POM_enquiry_not_in)
    
    
    The semantics for these values follow the definitions in pom_tokens.h
    """
    attribute: str = ''
    valueObjects: List[POM_object] = ()
    predicateOperator: int = 0


@dataclass
class SearchRecipe(TcBaseObj):
    """
    The recipe for executing a search.
    
    :var configuratorPerspective: Defines the scope of the search. Results are filtered based on the parameters defined
    by the perspective, e.g. revision rule, variant rule, product item(s), and product model(s).
    :var settings: Processing directives, for example parameters to pass on to the configurator for evaluation of
    variant configuration constraint rules. 
    
    The settings which are supported  are:
    
    Cfg0PerspectiveColumnsToReturn  - List of strings used to specify the column indices of the result table that
    should be returned back to the client. For example: if the list  contains { "0", "2" }, only columns at 0th and 2nd
    index will be returned back to the client. If no value is specified, all columns will be returned.
    :var searchExpression: Search criteria to be evaluated
    :var rootExpressionInputClientId: The 'clientId' value of the  root search definition structure . The search
    definitions that are contained in parameter "'searchExpression'" are the individual building blocks that aggregate
    into a single query. The "'rootExpressionInputClientId'" parameter identifies which of the search criteria
    definitions in "'searchExpression'" represents the composition of all individual search criteria. For example if
    "'searchExpression'" contained a 'savedQuery' "Q", an 'includeObject' definition "I", and an 'expressionGroup' "G"
    which combines "Q" and "I", then the 'rootExpressionInputClientId' would be "G".
    :var variantCriteria: Input Object with Variant Expression to be used for filtering the search result. 
    This filter is having 'AND' relation with the searchExpression and it is applied applied on top of
    searchExpression. 
     
    The expresion used for filtering is based on the 'opcode' passed as input in settings.
    If no Variant Expression is found for the 'opcode' passed as input or the input object is not Variant Configurable
    then following validation error is thrown:
    79008 - The search criteria provided in input is invalid.
    """
    configuratorPerspective: Cfg0ConfiguratorPerspective = None
    settings: SettingsMap = None
    searchExpression: SearchExpressionInput = None
    rootExpressionInputClientId: str = ''
    variantCriteria: BusinessObject = None


@dataclass
class SearchResponse(TcBaseObj):
    """
    Response SOA Structure for search results
    
    :var objectsDone: "Deprecated, use rowsDone instead"
    An integer value specifying the number of objects returned so far for executeSearch and fetchNextSearchResults
    operations.
    :var rowsDone: An integer value specifying the number of rows returned so far for executeSearch and
    fetchNextSearchResults operations.
    :var estimatedObjectsLeft: "Deprecated, use estimatedRowsLeft instead"
    An integer value specifying the estimated number of objects that still are potentially results of this search.
    :var estimatedRowsLeft: An integer value specifying the estimated number of rows that still are potentially results
    of this search.
    :var foundObjects: The list of objects returned by the executeSearch or fetchNextSearchResults operation.
    :var searchResultTable: A table of rows returned by the executeSearch or fetchNextSearchResults operation.
    :var searchCursor: Search cursor object that tracks the search results. This object is used to get the next set of
    results for this executeSearch operation.
    :var serviceData: Service Data for any error information. Typically this will contain errors about any malformed
    search recipes. 
    Following are some of the error codes that may be populated as partial errors in the ServiceData object(To be added
    later)
    """
    objectsDone: int = 0
    rowsDone: int = 0
    estimatedObjectsLeft: int = 0
    estimatedRowsLeft: int = 0
    foundObjects: List[POM_object] = ()
    searchResultTable: SearchResultTable = None
    searchCursor: Cfg0SearchCursor = None
    serviceData: ServiceData = None


@dataclass
class SearchResultTable(TcBaseObj):
    """
    Represents a set of search result records. Each result column is return in the member that corresponds to the data
    type for this column. For example, a search that produced a result table comprising an object column, a string
    column, and another object column will return the two object columns in member "'objectColumns'" as
    'objectColumns''["column__''0''"]' and 'objectColumns''["column__''2''"]', while the string value column will be
    returned in member "'stringColumns'" as 'stringColumns''["column__''1''"]'.
    
    :var objectColumns: A map tying a column header to a vector of objects. The column header corresponds to the
    "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the 'SearchExpressionInput' that
    produced this result column. If no 'alias' name was assigned a system generated column header like "column__0" will
    be used.
    :var stringColumns: A map tying a column header to a vector of string values. The column header corresponds to the
    "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the' ''SearchExpressionInput'
    that produced this result column. If no alias name was assigned a system generated column header like "column__0"
    will be used.
    :var intColumns: A map tying a column header to a vector of integer values. The column header corresponds to the
    "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the 'SearchExpressionInput' that
    produced this result column. If no alias name was assigned a system generated column header like "column__0" will
    be used.
    :var doubleColumns: A map tying a column header to a vector of double precision floating point values. The column
    header corresponds to the "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the
    'SearchExpressionInput' that produced this result column. If no alias name was assigned a system generated column
    header like "column__0" will be used.
    :var logicalColumns: A map tying a column header to a vector of Boolean values. The column header corresponds to
    the "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the 'SearchExpressionInput'
    that produced this result column. If no alias name was assigned a system generated column header like "column__0"
    will be used.
    :var dateColumns: A map tying a column header to a vector of date values. The column header corresponds to the
    "'alias'" field that was specified in the 'SearchResultTableColumn' definition in the 'SearchExpressionInput' that
    produced this result column. If no alias name was assigned a system generated column header like "column__0" will
    be used.
    """
    objectColumns: TagVectorMap = None
    stringColumns: StringVectorMap = None
    intColumns: IntVectorMap = None
    doubleColumns: DoubleVectorMap = None
    logicalColumns: BoolVectorMap = None
    dateColumns: DateVectorMap = None


@dataclass
class SearchResultTableColumn(TcBaseObj):
    """
    Defines a column to be returned in the search result table for this search definition. Some search definitions use
    a predefined column for attribute "puid" at index 0.
    
    :var index: The index of the column in the search result table. Some search definitions use a predefined column for
    attribute "puid" at index 0. For these search definitions the index should be >= 1.
    :var attribute: The name of the POM attribute to return in this column of the search result table.
    :var alias: The alias name of the search result table column. A NULL value indicates that no alias name is assigned.
    :var dataType: The data type of the search result table column. The value must match a POM type token between
    POM_MIN_type_token and POM_MAX_type_token defined in <pom/pom/pom_tokens.h>.
    """
    index: int = 0
    attribute: str = ''
    alias: str = ''
    dataType: int = 0


@dataclass
class TraversalExpressionInput(TcBaseObj):
    """
    Defines search criteria based on a TransferOptionSet along with a set of configuration parameters available for
    this TransferOptionSet. Search criteria defined by a 'TraversalExpressionInput' structure specify how the search
    results should be post processed. The given TransferOptionSet references a TransferMode and ClosureRule to traverse
    to objects that are related to the search results. TransferOptionSet search definitions are not supported in
    Teamcenter 10.1.2.
    
    :var clientID: This unique ID is used to identify return data elements and partial errors associated with this
    input structure.
    :var transferOptionsSet: Defines the traversal to apply as a post process after executing a search query. The
    specified TransferOptionSet object contains to reference a TransferMode object along with the list of defined
    parameters for this transfer mode. The selected transfer mode contains a reference to the traversal rule
    (ClosureRule) to be used along with the definition of the output format, and the filters to apply.
    :var optionNames: The list of the names of the parameters for which a value is provided. The list of available
    names depends on the TransferOptionSet that is specified in parameter.
    :var optionValues: Specifies the values of the provided parameters. TransferOptionSet objects represent a
    parameterized transfer mode. The list of valid values depends on the specific transfer mode that is selected by the
    option set given in parameter transferOptionsSet.
    :var resultColumns: A list of additional columns to return in the search result. This search definition uses a
    predefined result table column for attribute "puid" at index 0. This parameter can be used to define additional
    columns to be returned in the result table for this search table.
    """
    clientID: str = ''
    transferOptionsSet: TransferOptionSet = None
    optionNames: List[str] = ()
    optionValues: List[str] = ()
    resultColumns: List[SearchResultTableColumn] = ()


@dataclass
class ValidateProductConfigInput(TcBaseObj):
    """
    Input structure for the 'validateProductConfiguration' SOA
    
    :var applyConstraints: Indicates whether or not to apply the constraints. The parameter value is a bit pattern
    specifying the requested operation. A parameter value of 25 reports warnings and informational messages in addition
    to errors : 
    Apply constraints | Report Warnings | Report Info = 1+8+16 = 25 
    0 - indicates constraint application is not required 
    1 - apply configuration constraints 
    2 - skip constraints if they only reference unset families 
    4 - skip constraints that don't reference all configExpression families 
    8 - report warnings in addition to errors 
    16 - also report informational messages 
    32 - continue Validation On Error 
    64 - treat constraints with warning severity as if they had error severity
    128 - skip all variability checks which could raise a "k_variant_criteria_outside" validation failure
    256 - skip the check against allocated variability which could raise a "k_variant_criteria_outside" validation
    failure
    1024 - skip criteria update based on validation rules ( e.g. Exclude rule ). If this flag is not set it will update
    the criteria after applying validation rules
    2048 - enable Availability Constraint evaluation
    :var expressionsToValidate: The expressions to be validated.
    :var context: A runtime object to provide input data which include product item(s), product model(s). It also
    include configuration information e.g. revision rule and or variant rule.
    """
    applyConstraints: int = 0
    expressionsToValidate: List[BusinessObjectConfigExpression] = ()
    context: Cfg0ConfiguratorPerspective = None


class SearchGroupOperator(Enum):
    """
    Set operator values to use when combining the results from each search definition in a 'ExpressionGroupInput'.
    - UnionAll     - Combines the results of two search definitions into a set that contains all of the objects that
    are returned from either the left or the right search definition operand. Duplicates are not removed from the
    combined set.
    - UnionUnique -    Combines the results of two search definitions into a set that contains a unique list of objects
    that includes objects returned from either the left or the right search definition operand. The combined set will
    not contain duplicates.
    - Intersection -    Combines the results of two search definitions into a set that contains all of the objects that
    are returned from the left as well as the right search definition operand.
    - Difference    - Combines the results of two search definitions into a set that contains all of the objects that
    are returned from the left but not from the right search definition operand.
    
    
    
    :var UnionAll: Combines the results of two search definitions into a set that contains all of the objects that are
    returned from either the left or the right search definition operand. Duplicates are not removed from the combined
    set.
    :var UnionUnique: Combines the results of two search definitions into a set that contains a unique list of objects
    that includes objects returned from either the left or the right search definition operand. The combined set will
    not contain duplicates.
    :var Intersection: Combines the results of two search definitions into a set that contains all of the objects that
    are returned from the left as well as the right search definition operand.
    :var Difference: Combines the results of two search definitions into a set that contains all of the objects that
    are returned from the left but not from the right search definition operand.
    """
    UnionAll = 'UnionAll'
    UnionUnique = 'UnionUnique'
    Intersection = 'Intersection'
    Difference = 'Difference'


class SearchJoinOperator(Enum):
    """
    Join operator values to use when combining the results from each search definition in a 'ExpressionJoinInput'.
    
    - InnerJoin - Combines the column values of two searches (A and B) based upon a join condition. The join compares
    each row of A with each row of B to find all pairs of rows which satisfy the join condition.
    - LeftJoin - The result of a left join for searches A and B always contains all records of the "left" search (A),
    even if the join condition does not find any matching record in the "right" search (B).
    - RightJoin - The result of a right join for searches A and B always contains all records of the "right" search
    (B), even if the join condition doesn't find any matching record in the "left" search (A).
    - FullJoin - The result of a full join for searches A and B always contains all records of both searches. Where
    records in A and B don't match, the result set will have NULL values for every column of the search that lacks a
    matching row. For those records that do match, a single row will be produced in the result set (containing fields
    populated from both searches).
    
    """
    InnerJoin = 'InnerJoin'
    LeftJoin = 'LeftJoin'
    RightJoin = 'RightJoin'
    FullJoin = 'FullJoin'


class SortOperator(Enum):
    """
    Sort operator values which decide the sort order for attributes in Search Options
    
    :var Ascending: Sort in ascending order
    :var Descending: Sort in descending order
    """
    Ascending = 'Ascending'
    Descending = 'Descending'


"""
Map of bool property names to values '(string, bool').
"""
BoolMap = Dict[str, bool]


"""
Map of bool array property names to values ('string, vector< bool >').
"""
BoolVectorMap = Dict[str, List[bool]]


"""
A map of family and its association with product item and model. Association object representing the family in the context of the product item or model.  If a product item has been specified, then an allocation object is included.  If a product model has been specified, then an availability object is included.
"""
FamilyAssociationMap = Dict[Cfg0AbsOptionFamily, List[Cfg0AbsAssociation]]


"""
A map comprising of fully qualified name of a family as a key and its contents - name, data type and other attributes.
"""
FamilyHash = Dict[str, DeclaredFamily]


"""
A map comprising of name of a family as a key and its contents - name, data type and other attributes.
"""
FamilyNameHash = Dict[str, List[DeclaredFamily]]


"""
Map of float property names to values ('string', 'float').
"""
FloatMap = Dict[str, float]


"""
Map of float array property names to values ('string', 'vector').
"""
FloatVectorMap = Dict[str, List[float]]


"""
A map which contains all allocation records for a group in product model.
"""
GroupAllocationMap = Dict[Cfg0AbsFamilyGroup, List[Cfg0AbsAllocation]]


"""
Map of ineteger property names to values ('string', 'int').
"""
IntMap = Dict[str, int]


"""
Map of integer array property names to values ('string', 'vector').
"""
IntVectorMap = Dict[str, List[int]]


"""
Maps processing directive names to their values, or value list
"""
SettingsMap = Dict[str, List[str]]


"""
Map of Strings
"""
StringMap = Dict[str, str]


"""
Map between family and variant option
"""
StringVariantOptionMap = Dict[str, VariantOption]


"""
Map of string array property names to values ('string, vector<string>').
"""
StringVectorMap = Dict[str, List[str]]


"""
Map of BusinessObject property names to values ('string, BusinessObject').
"""
TagMap = Dict[str, BusinessObject]


"""
Map of BusinessObject array property names to values ('string, vector<BusinessObject>').
"""
TagVectorMap = Dict[str, List[BusinessObject]]


"""
A map of values and its corresponding association with product item or model. Association object representing the feature in the context of the product item or model.  If a product item has been specified, then an allocation object is included.  If a product model has been specified, then an availability object is included.
"""
ValueAssociationMap = Dict[Cfg0AbsOptionValue, List[Cfg0AbsAssociation]]


"""
Map of reference or relation property name to secondary 'CreateInput' objects ('string, vector<CreateInput>').
"""
CreateInputMap = Dict[str, List[CreateInput]]


"""
Map of date property names to values ('string, date').
"""
DateMap = Dict[str, datetime]


"""
Map of DateTime array property names to values ('string, vector<DateTime>').
"""
DateVectorMap = Dict[str, List[datetime]]


"""
Map of  double property names to values (string, float).
"""
DoubleMap = Dict[str, float]


"""
Map of double array property names to values (string, vector).
"""
DoubleVectorMap = Dict[str, List[float]]
