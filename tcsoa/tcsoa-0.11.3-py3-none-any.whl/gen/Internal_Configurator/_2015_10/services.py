from __future__ import annotations

from tcsoa.gen.Internal.Configurator._2015_10.ConfiguratorManagement import AvailableProductVariabilityInput, ConvertVariantExpressionsResponse, ValidateProductConfigurationResponse, ProductDefaultsInput, ConvertVariantExpressionInput, GetVariantExpressionsResponse, AvailableProductVariabilityOutput, SetVariantExpressionInput, ValidateProductConfigInput, GetProductDefaultsResponse, GetRevisionRulesResponse
from tcsoa.gen.BusinessObjects import BusinessObject, RevisionRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def convertVariantExpressions(cls, inputs: List[ConvertVariantExpressionInput]) -> ConvertVariantExpressionsResponse:
        """
        This operation converts the input application config configuration expressions  given in formulae and/or grid
        format into formulae, grid and displayable or user readable format.
        
        Use cases:
        1: Create an ApplicationConfigExpression structure providing only formula and not provide the grid expression 
        ConfigExpressionSet structure.
        2: Create an ApplicationConfigExpression structure providing the grid expression ConfigExpressionSet structure
        and not provide the formula.
        3: Create an ApplicationConfigExpression structure providing the formula as well as the grid expression
        ConfigExpressionSet structure.
        
        In all the three cases, the output ApplicationConfigExpression structure will be populated with formulae, grid
        expression ConfigExpressionSet structure and display formulae.
        
        
        The string "NS" is the family namespace. The family namespace defines the uniqueness of the family within
        itself. System ensures that the combination of the family namespace and the family id is unique in the
        database. For family "F" with namespace "NS" system will identify it as "[NS]F".
        
        The examples of display formulae are as follows:
        
        1)  Boolean expression
        
        [NS]BOOL - represents TRUE
        [NS]!BOOL - represents FALSE
        
        
        2)  Date expressions
        Date features are displayed in the standard Teamcenter locale-specific date format.
        3)  Range expressions
        
        [NS]A = a1 &amp; [NS]LENGTH <= 50
        [NS]A = a1 &amp; ([NS]LENGTH >= 1 &amp; [NS]LENGTH <= 10)
        [NS]A = a1 &amp; [NS]LENGTH >= 20
        [NS]A = a1 &amp; !([NS]LENGTH >= 20)
        
        
        4)  Multiple column expressions must be grouped within brackets
        
        ([NS]A = a1 &amp; [NS]B = b1) | ([NS]A = a2 &amp; [NS]C = c1)
        
        
        5)  Multiple selections within a single column
        
        ([NS]A = a1 | [NS]A = a2) &amp; [NS]B = b1
        
        
        6)  Multiple selections in a family 'C' that has Multi-select=Yes
        
        ([NS]A = a1 | [NS]A = a2) &amp; [NS]C = c1 &amp; [NS]C = c2
        
        
        7)  Optional family 'D' [Target]
        
        [NS]A = a1 &amp; [NS]D = NONE (same as [NS]D = '')
        [NS]A = a1 &amp; [NS]D = ANY (same as [NS]D != '')
        """
        return cls.execute_soa_method(
            method_name='convertVariantExpressions',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=ConvertVariantExpressionsResponse,
        )

    @classmethod
    def getAvailableProductVariability(cls, input: AvailableProductVariabilityInput) -> AvailableProductVariabilityOutput:
        """
        This operation computes the available features within a set of requested families. The parameters
        criteriaExpression and familiesToTest are used to pass in the input expression and families of interest
        requesting the available features. The operation in response returns the available product variability for the
        requested families satisfying the input expression in criteriaExpression and the constraint(s) present in the
        system. If the input parameter criteriaExpression is empty, then the response will return the product
        variability for the requested families satisfying all the system constraints. If the requested family list is
        empty, the operation will not return any variability information.
        
        Use cases:
        Consider the following Variability data in a Configurator context say MyProductItem:
        
        Family&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;Features
        A
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;A1
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;A2
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;A3
        
        B
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;B1
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;B2
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;B3
        
        C
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;C1
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;C2
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;C3
        
        Rules:
        &amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;A3 Includes B2:  This is an inclusion rule stating that if the
        configuration has the feature A3 (of the family A) then include the feature B2 as well (of the family B).
        B2 Excludes C2:  This is an exclusion rule state that if the configuration has the feature B2 (of the family B)
        then exclude/remove the feature C2 (of the family C)
        
        Use case 1:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        CriteriaExpression = {}
        familiesToTest = {A, B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1(enable configurator constraint evaluation)
        
        Response would contain - A1, A2, A3, B1, B2, B3, C1, C2 &amp; C3
        
        Use case 2:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        CriteriaExpression = {A=A3}
        FamiliesToTest = {B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1
        
        Response would - B2, C1 &amp; C3
        
        Use case 3:
        Operation getAvailableProductVariability is invoked with AvailableProductVariabilityInput populated as:
        criteriaExpression = {A=A1}
        FamiliesToTest = {B, C}
        context containing reference to Item MyProductItem
        applyConstraints = 1
        
        Response would - B1, B2, B3, C1, C2 &amp; C3
        
        
        Use case 4: 
        Initialize a variant criteria dialog for a new VariantRule in the Configurator context MyProductItem:
        The application uses operation getAvailableProductVariability with AvailableProductVariabilityInput populated
        as below:
        criteriaExpression = {}
        familiesToTest = {}
        context containing reference to Item MyProductItem
        ApplyConstraints = 0
        
        A service exception will be thrown by the  getAvailableProductVariability operation as familiesToTest is empty.
        """
        return cls.execute_soa_method(
            method_name='getAvailableProductVariability',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'input': input},
            response_cls=AvailableProductVariabilityOutput,
        )

    @classmethod
    def getProductDefaults(cls, inputs: List[ProductDefaultsInput]) -> GetProductDefaultsResponse:
        """
        This operation returns the product defaults for the input expression(s) by applying the default rule(s). The
        revision rule is used to determine the correct revision of configurator objects like rules, families, features,
        availability statements etc, that take part in the process. The parameter expressionsToUpdate specifies the
        input variant expressions for the variant configuration. The parameter families specifies the option families
        for which a default value assignment is requested. If specified, the server assigns default features for only
        these families in the response. If the list is empty, the server assigns default features for all the families.
        
        This operation also returns the list of mandatory families, which  do not have any value selection. The
        response returns this list of families in parameter requiredFamilies. The parameter criteriaStatus conveys the
        information about the status of the configuration.
        
        Use cases:
        Consider the following Variability data in a Configurator context :
        Family Features
        TYPE  CLASSIC, HATCHBACK, SEDAN
        ENGINE  L4, V6, V8
        COLOR RED, GREEN, BLUE
        ABS ABS
        Default Rules:
        Default Rule 1 - "If TYPE=CLASSIC and ENGINE=L4 then Apply COLOR=RED"
        Default Rule 2 - "If TYPE=CLASSIC and ENGINE=L4 then Apply ABS=TRUE"
        The getProductDefaults operation can be used in following ways:
        
        Example 1: 
        User provides the input expression to getProductDefaults as "TYPE=CLASSIC and ENGINE=L4" then the response will
        be "TYPE=CLASSIC and ENGINE=L4 and COLOR=RED and ABS=TRUE" in expressionsWithDefaults. The parameter
        requiredfamilies will be blank and the parameter criteiaStatus has value validAndComplete.
        
        Example 2:
        User provides input expression to getProductDefaults as TYPE=CLASSIC and ENGINE=L4, the input parameter
        families contains family COLOR. The response returns the variant expression as "TYPE=CLASSIC and ENGINE=L4 and
        COLOR=RED". ABS=TRUE is not expected in the response because family ABS didn't exist in the input parameter
        families. The parameter requiredfamilies will contain "ABS" and the parameter criteriaStatus has value
        validAndInComplete.
        
        Example 3:
        User provides input expression to getProductDefaults as TYPE=HATCHBACK and ENGINE=L4, the input parameter
        families contains family as COLOR. The response will have the variant expression as "TYPE=HATCHBACK and
        ENGINE=L4". The parameter requiredfamilies will contain the Family COLOR and the parameter criteriaStatus has
        value validAndInComplete. Consider the following Variability data in a Configurator context : Family Values
        Models  VXI, LXI TYPE CLASSIC, HATCHBACK, SEDAN  
        Availability Rules:  "TYPE = CLASSIC" is available to "Models = VXI"  "TYPE = SEDAN" is available to "Models =
        LXI"  Default Rules: Default Rule 1: "TYPE = SEDAN".
        
        Example 4:
        User provides input expression to getProductDefaults as "Models = VXI | Models = LXI".  The response will have
        the variant expression as "Models = VXI | Models = LXI &amp; TYPE = SEDAN". Here we have two branches in the
        input criteria expression.  The first branch is "Models = VXI" and the second branch is "Models = LXI". As
        SEDAN is not available to VXI and it is available to LXI, default rule gets applied to second branch only.
        The parameter requiredfamilies will contain blank and the parameter criteriaStatus has value validAndComplete.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getProductDefaults',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=GetProductDefaultsResponse,
        )

    @classmethod
    def getRevRulesForConfiguratorContext(cls) -> GetRevisionRulesResponse:
        """
        This operation provides the list of RevisionRule objects which can be used for configuration of the
        Configurator contexts in Product Configurator application. 
        
        The operation will return the RevisionRule instances. The supported rule entries in the Revision Rule mentioned
        below:
        - Has Released Status
        - Working 
        - Latest Created
        
        
        
        Use cases:
        When user queries the allocated features and families with the RevisionRule instance, the configured revisions
        of the families and features as per the input RevisionRule are returned.
        """
        return cls.execute_soa_method(
            method_name='getRevRulesForConfiguratorContext',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={},
            response_cls=GetRevisionRulesResponse,
        )

    @classmethod
    def getVariantExpressions(cls, targetObjects: List[BusinessObject], revisionRule: RevisionRule) -> GetVariantExpressionsResponse:
        """
        This operation returns the variant expressions associated with the given set of target objects. The revision
        rule specified in 'revRule' is used to retrieve the correct revision of variant data referenced by variant
        expressions.  Setting revRule to nullTag is valid.  In this case  any unconfigured wso would be returned and
        caller should use it only for thread related properties like objectId, namespace, datatype, UOM.
        
        For example using a valid revRule, An inclusion rule has variant expression set as   "[Dict]familyA.feature1
        AND NOT [Dict]familyB.feature2" . The grid expression structure returned by this operation in the response will
        have values populated as follows
        
        Use cases:
        User can get variant expressions of an existing object. For example 
        
        Using any existing revision rule and using operation 'setVariantExpressions' set subject condition as "Color =
        Red". To retrieve this variant expression 'getVariantExpressions' can be used which returns variant expression
        formula and the client representable structure format.
        """
        return cls.execute_soa_method(
            method_name='getVariantExpressions',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'targetObjects': targetObjects, 'revisionRule': revisionRule},
            response_cls=GetVariantExpressionsResponse,
        )

    @classmethod
    def setVariantExpressions(cls, inputs: List[SetVariantExpressionInput], revisionRule: RevisionRule) -> ServiceData:
        """
        This operation sets a variant expression for the input business object. The variant expressions can be set for
        rules which includes include rule, exclude rule, default rule and availability rules, variant conditions and
        variant criteria. 
        
        On configurator rules multiple variant expressions or conditions can be set such as constraint and
        applicability condition. The variant expression is identified with the "'expressionType'" set on input.
        
        User can set transient or in memory variant expression on the target object.. The input flag saveExpressions
        can be used only for the objects having session recovery feature supported, for example VariantRule. If the
        parameter saveExpressions is set as TRUE then the variant expression object is saved and the persistent variant
        expression is returned. 
        
        If the saveExpressions is set to FALSE, then the operation will create a transient variant expression. If
        configuration need not be persisted and is for temporary use, the transient variant expression can be used. If
        a transient configuration expression is created, then user needs to save the target object explicitly or else
        the changes are lost when the user session ends. Transient changes or objects provide a convenient way to make
        temporary changes that automatically go out of scope when the session ends.
        
        Use cases:
        User can use this operation set variant expressions of an existing object. For example
        
        Create an instance of default rule (Cfg0DefaultRule) The operation 'setVariantExpressions' will set
        applicability condition as "Color = Red". User can provide variant expression for applicability condition in
        form of formula i.e. "[Dictionary]Color=Red" or populated grid expression service structure. 
        """
        return cls.execute_soa_method(
            method_name='setVariantExpressions',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs, 'revisionRule': revisionRule},
            response_cls=ServiceData,
        )

    @classmethod
    def validateProductConfiguration(cls, inputs: List[ValidateProductConfigInput]) -> ValidateProductConfigurationResponse:
        """
        This operation validates the input expression(s) by applying the constraint rules such as inclusion rule,
        exclusion rule or availability rule for the input configurator perspective. The revision rule is used to
        determine the correct revision of configurator objects like rules, families, features, availability statements
        etc, that will take part in validation and configuration process. The parameter expressionsToValidate specifies
        the input variant expressions that needs to be validated. 
        
        This operation also returns the list of mandatory families, which don't have any feature selection. The
        response returns this list of families in parameter requiredFamilies. The parameter criteriaStatus conveys the
        information about the status of the configuration.
        
        Use cases:
        Consider the following Variability data and Rules in a Configurator context:
        Family  Features
        Model  Luxury, Economy
        TYPE  CLASSIC, HATCHBACK, SEDAN
        ENGINE  L4, V6, V8
        COLOR  RED, GREEN, BLUE
        # All the families are non-discretionary families.
        Rules:
        Exclude Rule 1 - If 'ENGINE=L4' then exclude 'TYPE=SEDAN else Error "TYPE cannot be SEDAN for L4 ENGINE".
        Include Rule 2 - If 'TYPE=CLASSIC' then include 'COLOR=RED' else Error "Classic comes with Red Color only".
        
        Use case 1:
        User provides the input expression to validateProductConfiuration as "TYPE=SEDAN and ENGINE=L4" to validate the
        expression. The output of the operation is a violation expected with message as "TYPE cannot be SEDAN for L4
        ENGINE" and updated expression as "TYPE=SEDAN and ENGINE=L4". The parameter requiredFamilies will be empty, as
        there are violations and parameter criteriaStatus has value inValid.
        
        Use Case 2:
        User creates an availability say 'RED' is available to model 'LUXURY'. User does not define any availability of
        the value 'BLUE' for the product model 'LUXURY'. System is configured to evaluate the availability constraints
        and the user provides an expression as "MODEL=LUXURY and COLOR=BLUE Then the output of the operation returns a
        violation with the message "The option value 'BLUE' is not available to the following product models: LUXURY".
        The parameter requiredFamilies will be empty, as there are violations and parameter criteriaStatus has value
        inValid.
        
        Use Case 3:
        User provides the input expression as "TYPE=CLASSIC" to validateProductConfiuration operation will validate the
        expression. Then the output of the operation returns the updated expression will "TYPE=CLASSIC and COLOR=RED"
        with no violation. The parameter requiredFamilies will contain family "ENGINE" and parameter criteriaStatus has
        value validAndInComplete. 
         
        Use Case 4:
        User provides the input expression as "TYPE=CLASSIC and COLOR=BLUE" The output of the operation returns a
        violation with message as "Classic comes with Red Color only". The parameter requiredFamilies will be empty, as
        there are violations and parameter criteriaStatus has value inValid.
        """
        return cls.execute_soa_method(
            method_name='validateProductConfiguration',
            library='Internal-Configurator',
            service_date='2015_10',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=ValidateProductConfigurationResponse,
        )
