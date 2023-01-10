from __future__ import annotations

from tcsoa.gen.ConfigFilterCriteria._2011_06.EffectivityManagement import ConfigExpression
from tcsoa.gen.ConfigFilterCriteria._2013_05.EffectivityManagement import EffectivityOverlapStateResponse, EffectivityDisplayStringResponse
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.ConfigFilterCriteria._2013_05.VariantManagement import VariantCriteriaResponse


class EffectivityManagementService(TcService):

    @classmethod
    def getEffectivityDisplayString(cls, expressions: List[ConfigExpression], productName: str, productNameSpace: str, configuratorURL: str) -> EffectivityDisplayStringResponse:
        """
        This operation returns a localized string representation for effectivity expressions. This string
        representation is the same that is used for display values of effectivity formula properties
        mdl0effectivity_formula and mdl0allowed_eff_formula. Applications can use this API to display effectivity
        conditions for objects that have not yet been saved with this effectivity, e.g. if multiple effectivity
        modifications are accumulated in a client session before they are saved. In this scenario effectivity
        properties are not (yet) available prior to saving modified objects.
        This operation connects to the effectivity configurator service whose service endpoint is specified by the
        'configuratorURL' parameter. The actual conversion to formula strings is performed by this configurator
        service. Depending on the (configurator specific) encoding the operation might require the specification of a
        product context using parameters 'productName' and 'productNameSpace'. For example, a given configurator might
        use  shorthand representations for formulae if these are unique in the context of the specified product.
        Teamcenter 10.1 only supports local built in Teamcenter configurators where parameter 'configuratorURL' can be
        set to an empty string. Teamcenter configurators don't require a product context if the formulae are in
        Explicit Teamcenter Language. The encoding is explicit if all lexemes are uniquely identified, e.g.
        [OptionNamespace]FamilyName = UniqueValue, where no product context is required to determine the family name
        for a value, or the option namespace for the family. A configuration condition formula is in Explicit
        Teamcenter Language if its form is explicit and comprised of the lexemes documented for the Teamcenter Variant
        Formula property. Teamcenter configurators support shorthand encodings like FamilyName = UniqueValue or
        UniqueValue if the lexemes used in the shorthand encoding are unique in the specified product context.
        
        Use cases:
        An application prepares several effectivity conditions with the intent to save them to a set of objects using
        operation setEffectivityConditions. The application wants to display the effectivity display string that would
        get saved with setEffectivityConditions before actually saving them.
        
        Exceptions:
        >This operation may raise 'Teamcenter::Soa::Server::ServiceException 'wrapping around following Teamcenter
        errors:
        
        256000    An internal configurator error occurred.
        256001    A general configurator error occurred.
        256002    The following product is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256003    The following feature value is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256004    The following feature family is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256005    An invalid feature combination was found (Context: info).
        256006    An invalid product configuration was found (Context: info).
        256007    An invalid expression was found (Context: info).
        256008    The following Boolean operator is invalid: opcode (Context: info).
        256009    An invalid effectivity date was found (Context: info).
        256010    A time-out occurred (Context: info).
        256011    A resource is not available (Context: info).
        256012    The following functionality is not implemented: function (Version: TcVersion).
        256013    A configurator implementation specific error occurred (Context: info).
        256014    The effectivity expression contains unmatched quote at position number.
        256015    The effectivity expression contains unmatched bracket at position number.
        256016    An unexpected token 'text' was found at position number.
        256017    The entry 'text' was found at position number when an option value was expected.
        256018    The token 'text' is missing after 'text' at position number.
        256019    The effectivity expression adaptor does not support text used at position number.
        256020    The XML tag 'text' has no text value.
        256021    The string 'formula' cannot be converted into an expression. 
        256022    The operator code 'opcode' in token at position number is unknown.
        256023    The effectivity value 'text' in token at position number is unknown.
        256024    The effectivity family 'text' in token at position number is unknown.
        256025    An ambiguous option value name 'FamilyName' in namespace 'DictionaryNamespace' in token at position
        number was found: text.
        256026    An ambiguous option family name 'FamilyName' in token at position number was found: 'text'.
        256027    The option namespace 'DictionaryNamespace' in token at position number is invalid.
        256028    The effectivity family 'FamilyName' in token at position number is invalid.
        256029    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid.
        256030    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid:
        its value is not numeric.
        256031    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid:
        the value unit of measure 'text' does not match the family unit of measure 'text'.
        256032    The option / family / family namespace combination 'text' / 'FamilyName' / 'DictionaryNamespace' in
        token at position number is invalid.
        256033    The family 'FamilyName' for option / family namespace combination 'text' / 'DictionaryNamespace' in
        token at position number is invalid. 
        256034    There is no option value in token at position number.
        256035    The effectivity option value 'text' for family 'FamilyName' in token at position 'number' is invalid:
        the value is not a valid date.
        """
        return cls.execute_soa_method(
            method_name='getEffectivityDisplayString',
            library='ConfigFilterCriteria',
            service_date='2013_05',
            service_name='EffectivityManagement',
            params={'expressions': expressions, 'productName': productName, 'productNameSpace': productNameSpace, 'configuratorURL': configuratorURL},
            response_cls=EffectivityDisplayStringResponse,
        )

    @classmethod
    def getEffectivityOverlapStates(cls, referenceExpressions: List[ConfigExpression], expressions: List[ConfigExpression], productName: str, productNameSpace: str, configuratorURL: str) -> EffectivityOverlapStateResponse:
        """
        This operation determines and returns the degree of overlap between a set of effectivity expressions and a set
        of reference effectivity criteria expressions. When applications create or update DesignElements (DE) and
        assign effectivity, the UI may want to qualify the degree of overlap between the effectivity of the DE and the
        currently active RevRule effectivity criteria.
        The following example illustrates the overlap states for a set of expressions:
        'RevisionRule:     |---------------|
        Object 0:  |----|                            : OverlapStateNone
        Object 1:     |------|                       : OverlapStateIntersect
        Object 2:                |----|              : OverlapStateSubset
        Object 3:                    |------|        : OverlapStateIntersect
        Object 4:  |-----------------------------|   : OverlapStateSuperset
        Object 5:         |---------------|          : OverlapStateMatch
        Object 6:         |-------------------|      : OverlapStateSuperset
        Object 7:     |-------------------|          : OverlapStateSuperset'
        This operation connects to the effectivity configurator service whose service endpoint is specified by the
        'configuratorURL' parameter. Any conversion from formula strings is performed by this configurator service.
        Depending on the (configurator specific) encoding the operation might require the specification of a product
        context using parameters 'productName' and 'productNameSpace'. For example, a given configurator might
        recognize shorthand representations for formulae if these are unique in the context of the specified product.
        Teamcenter 10.1 only supports local built in Teamcenter configurators where parameter 'configuratorURL' can be
        set to an empty string. Teamcenter configurators don't require a product context if the formulae are in
        Explicit Teamcenter Language. The encoding is explicit if all lexemes are uniquely identified, e.g.
        [OptionNamespace]FamilyName = UniqueValue, where no product context is required to determine the family name
        for a value, or the option namespace for the family. A configuration expression formula is in Explicit
        Teamcenter Language if its form is explicit and comprised of the lexemes documented for the Teamcenter Variant
        Formula property. Teamcenter configurators support shorthand encodings like FamilyName = UniqueValue or
        UniqueValue if the lexemes used in the shorthand encoding are unique in the specified product context.
        
        Use cases:
        An application wants to qualify effectivity conditions that were retrieved with getEffectivityConditions as to
        whether the condition is equal to, intersects with, or is a subset or superset of the effectivity criteria
        associated with one or more RevisionRules. This cannot be achieved with properties on effectivity conditions or
        RevisionRules because the result depends on the combination of an effectivity condition and the effectivity
        configuration criteria on a RevisionRule. One and the same condition may have different overlap states with
        different RevisionRules.
        The application calls getEffectivityOverlapStates and passes the effectivity criteria (as obtained from a
        RevisionRule using getRevRuleEffectivityCriteria) as 'referenceExpressions', and the effectivity conditions (as
        obtained from a set of product data elements using getEffectivityConditions) as 'expressions'.
        
        
        Exceptions:
        >This operation may raise 'Teamcenter::Soa::Server::ServiceException 'wrapping around following Teamcenter
        errors:
        
        256000    An internal configurator error occurred.
        256001    A general configurator error occurred.
        256002    The following product is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256003    The following feature value is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256004    The following feature family is invalid: [DictionaryNamespace]FamilyName (Context: info).
        256005    An invalid feature combination was found (Context: info).
        256006    An invalid product configuration was found (Context: info).
        256007    An invalid expression was found (Context: info).
        256008    The following Boolean operator is invalid: opcode (Context: info).
        256009    An invalid effectivity date was found (Context: info).
        256010    A time-out occurred (Context: info).
        256011    A resource is not available (Context: info).
        256012    The following functionality is not implemented: function (Version: TcVersion).
        256013    A configurator implementation specific error occurred (Context: info).
        256014    The effectivity expression contains unmatched quote at position number.
        256015    The effectivity expression contains unmatched bracket at position number.
        256016    An unexpected token 'text' was found at position number.
        256017    The entry 'text' was found at position number when an option value was expected.
        256018    The token 'text' is missing after 'text' at position number.
        256019    The effectivity expression adaptor does not support text used at position number.
        256020    The XML tag 'text' has no text value.
        256021    The string 'formula' cannot be converted into an expression. 
        256022    The operator code 'opcode' in token at position number is unknown.
        256023    The effectivity value 'text' in token at position number is unknown.
        256024    The effectivity family 'text' in token at position number is unknown.
        256025    An ambiguous option value name 'FamilyName' in namespace 'DictionaryNamespace' in token at position
        number was found: text.
        256026    An ambiguous option family name 'FamilyName' in token at position number was found: 'text'.
        256027    The option namespace 'DictionaryNamespace' in token at position number is invalid.
        256028    The effectivity family 'FamilyName' in token at position number is invalid.
        256029    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid.
        256030    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid:
        its value is not numeric.
        256031    The effectivity option value 'text' for family 'FamilyName' in token at position number is invalid:
        the value unit of measure 'text' does not match the family unit of measure 'te    xt'.
        256032    The option / family / family namespace combination 'text' / 'FamilyName' / 'DictionaryNamespace' in
        token at position number is invalid.
        256033    The family 'FamilyName' for option / family namespace combination 'text' / 'DictionaryNamespace' in
        token at position number is invalid. 
        256034    There is no option value in token at position number.
        256035    The effectivity option value 'text' for family 'FamilyName' in token at position 'number' is invalid:
        the value is not a valid date.
        """
        return cls.execute_soa_method(
            method_name='getEffectivityOverlapStates',
            library='ConfigFilterCriteria',
            service_date='2013_05',
            service_name='EffectivityManagement',
            params={'referenceExpressions': referenceExpressions, 'expressions': expressions, 'productName': productName, 'productNameSpace': productNameSpace, 'configuratorURL': configuratorURL},
            response_cls=EffectivityOverlapStateResponse,
        )


class VariantManagementService(TcService):

    @classmethod
    def getProductConfigurations(cls, productName: str, productNameSpace: str, configuratorURL: str) -> VariantCriteriaResponse:
        """
        This operation returns a set of product configurations managed at the configurator level, say for product
        tracking or reporting purposes.
        Teamcenter variant configurators manage product configurations as VariantRules which are attached to an
        ItemRevision representing the product using any relationship type (see also preference
        'TC_Default_SVR_Relationship'). The product is identified by 'productName' and 'productNameSpace' parameters.
        Teamcenter configurators use a Multiple Field Key (MFK) stable identifier (see property'
        Item::fnd0VariantNamespace') of the product item for 'productName', and the revision ID for 'productNameSpace'.
        The identifiers of the product associated with a Collaborative Design (Cpd0CollaborativeDesign) can be obtained
        from properties 'Mdl0ApplicationModel::mdl0config_product_name', and
        'Mdl0ApplicationModel::mdl0config_prod_namespace'.
        
        Use cases:
        An engineering project administrator has created a product ItemRevision. A manufacturing engineering user
        creates and maintains VariantRules that represent a set of configurations for prototype builds. The project
        administrator attaches these VariantRules to the product ItemRevision. Product engineering users can use
        operation 'getProductConfigurations' to review existing prototype configurations. The user can then chose one
        of the configurations to initialize variant configuration criteria with operation 'setVariantCriteria'.
        
        Exceptions:
        >This operation may raise 'Teamcenter::Soa::Server::ServiceException' wrapping around following Teamcenter
        errors:
        
        92002: The Product Name and Product Namespace must not be empty.
        """
        return cls.execute_soa_method(
            method_name='getProductConfigurations',
            library='ConfigFilterCriteria',
            service_date='2013_05',
            service_name='VariantManagement',
            params={'productName': productName, 'productNameSpace': productNameSpace, 'configuratorURL': configuratorURL},
            response_cls=VariantCriteriaResponse,
        )
