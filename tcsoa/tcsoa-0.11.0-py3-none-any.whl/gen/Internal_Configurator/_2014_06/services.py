from __future__ import annotations

from tcsoa.gen.BusinessObjects import RevisionRule, Cfg0SearchCursor, Cfg0ConfiguratorPerspective, Cfg0AbsFamilyGroup, Cfg0AbsOptionFamily, ItemRevision
from tcsoa.gen.Internal.Configurator._2014_06.ConfiguratorManagement import SearchRecipe, VariantRuleInput, SearchResponse, ValidateProductConfigurationResponse, ProductDefaultsInput, GetVariantCacheInfoResponse, GetOptionFamiliesResponse, ConfigExpressionDisplayStringInput, SearchOptions, ValidateProductConfigInput, FilterCriteria, GetFamilyGroupResponse, GetProductDefaultsResponse, CreateUpdateVariantRulesResponse, GetDisplayStringResponse, GetOptionValuesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def createUpdateVariantRules(cls, rules: List[VariantRuleInput], revRule: RevisionRule) -> CreateUpdateVariantRulesResponse:
        """
        This operation created or update the variant criteria object. Any object which has variant behavior implemented
        can be used as an variant criteria object. If parameter 'saveRule' is set as FALSE then variant criteria object
        is not saved and transient object is returned. The relationship name used to associate the variant criteria
        object to the product Item.
        
        Use cases:
        This operation can be used for following cases
        
        - Create new persistent variant criteria object.
        - Create new transient variant criteria object by providing 'saveRule' as False.
        - Create new and attach variant criteria object to the given product item by relation as mentioned in
        'relationName' or if passed empty then by default relationship TC_Default_SVR_Relationship.
        - Update variant expressions of the existsing variant criteria by providing existsing object in 'ruleToUpdate'.
        
        """
        return cls.execute_soa_method(
            method_name='createUpdateVariantRules',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'rules': rules, 'revRule': revRule},
            response_cls=CreateUpdateVariantRulesResponse,
        )

    @classmethod
    def getDefaultRules(cls, context: Cfg0ConfiguratorPerspective, filterCriteria: FilterCriteria) -> ServiceData:
        """
        This internal service operation returns the default rule instances as per the specified product items(s) in
        'context' and filter criteria. 
        The parameter ''filterCriteria'' allows filtering the rules returned by this operation based on criteria.
        Note: In Teamcenter 10.1.2 the product model(s) member in context is not supported.
        
        
        Use cases:
        This operation can be used to retrieve rules for the given product item(s) or product model(s) from parameter
        context. Parameter filterCriteria can be used for filtering based on specific family group(s) or family
        (families) or feature(s). 
        Consider that following set data:
        
        Family Groups: 
        Engine-Box - It has families "Engine" and "Transmission". 
        Engine - Petrol, Diesel
        Transmission - Manual, Auto
        Wheel - It has families "Wheel-drive" and "Suspension". 
        Wheel-drive - 2-Wheels, 4-Wheels
        Suspension - Full-Thrust, Full-Boom
        
        The rules are created as follows 
        
        1.If Transmission=Manual Then Set Wheel-drive=2-Wheels. 
        2.If Transmission=Auto Then Set Wheel-drive=4-Wheels. 
        3.If Engine=Diesel And Transmission=Manual Then Set Suspension=Full-Thrust. 
        4.If Engine=Petrol And Transmission=Manual Then Set Suspension=Full-Boom. 
        
        The response of operation for filter criteria will be as follows:
        Criteria: { Group: Engine-Box, Family:-, feature:-} - Rules returned will be 1,2,3,4. 
        Criteria: { Group: Engine-Box, Family: Engine, feature:-} - Rules returned will be 3 and 4. 
        Criteria: { Group: Engine-Box, Family: Engine, feature:Diesel} - Rules returned will be 3. 
        Criteria: { Group: -, Family: -, feature: Manual} - Rules returned will be 1,3,4.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getDefaultRules',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'filterCriteria': filterCriteria},
            response_cls=ServiceData,
        )

    @classmethod
    def getExcludeRules(cls, context: Cfg0ConfiguratorPerspective, filterCriteria: FilterCriteria, severities: List[str]) -> ServiceData:
        """
        This internal service operation returns the exclusion rule instances based on the specified 'context', the
        filter criteria and rule severity. 
        The parameter ''filterCriteria'' allows filtering the rules returned by this operation based on criteria.
        Note: In Teamcenter 10.1.2, the product model(s) member in context is not supported.
        
        
        Use cases:
        This operation can be used to retrieve rules for the given product item(s) or product model(s) from parameter
        context. Parameter filterCriteria can be used for filtering based on specific family group(s) or family
        (families) or feature(s). 
        Consider that following set data: 
        Groups: 
              - Engine-Box - It has families "Engine" and "Transmission". 
              - Engine - Petrol, Diesel
        Transmission - Manual, Auto
              - Wheel - It has families "Wheel-drive" and "Suspension". 
              - Wheel-drive - 2-Wheels, 4-Wheels
        Suspension - Full-Thrust, Full-Boom
        
        
        The rules are created as follows 
        1. If Transmission=Manual And Set Wheel-drive=4-Wheels Error "Incompatible combination". 
        2. If Transmission=Auto And Set Wheel-drive=4-Wheels Info "Optimum configuration". 
        3. If Engine=Diesel And Transmission=Manual Warning "Suspension should be Full-Thrust". 
        4. If Engine=Petrol And Transmission=Manual Warning "Suspension should be Full-Boom". 
        
        The response of operation for filter criteria will be as follows 
        Criteria: { Group: Engine-Box, Family:-, Feature:-} - Rules returned will be 1,2,3,4. 
        Criteria: { Group: Engine-Box, Family: Engine, Feature:-} - Rules returned will be 3 and 4. 
        Criteria: { Group: Engine-Box, Family: Engine, Feature:Diesel} - Rules returned will be 3. 
        Criteria: { Group: -, Family: -, Feature: Manual} - Rules returned will be 1,3,4.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getExcludeRules',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'filterCriteria': filterCriteria, 'severities': severities},
            response_cls=ServiceData,
        )

    @classmethod
    def getFamilyGroups(cls, context: Cfg0ConfiguratorPerspective) -> GetFamilyGroupResponse:
        """
        This internal operation returns the family group instances. The parameter context may provide either the
        product item(s). 
        If the product item(s) of context is available then those instances of the family group ('Cfg0AbsFamilyGroup'
        or subtypes) are returned which are allocated to the given product item(s). 
        
        
        
        Use cases:
        User can query family groups allocated to the product item(s) mentioned in 'context' parameter.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getFamilyGroups',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context},
            response_cls=GetFamilyGroupResponse,
        )

    @classmethod
    def getIncludeRules(cls, context: Cfg0ConfiguratorPerspective, filterCriteria: FilterCriteria, severities: List[str]) -> ServiceData:
        """
        This internal service operation returns the inclusion rule instances based on the specified context, the filter
        criteria and rule severity. 
        The parameter ''filterCriteria'' allows filtering the rules returned by this operation based on criteria.
        Note: In Teamcenter 10.1.2, the product model(s) member in context is not supported.
        
        
        Use cases:
        This operation can be used to retrieve rules for the given product item(s) or product model(s) from parameter
        'context'. Parameter 'filterCriteria' can be used for filtering based on specific family group(s) or family
        (families) or feature(s). 
        Consider that following set data: 
        Groups: 
        Engine-Box - It has families "Engine" and "Transmission". 
        - Engine - Petrol, Diesel
        - Transmission - Manual, Auto
        
        
        
        Wheel - It has families "Wheel-drive" and "Suspension". 
        - Wheel-drive - 2-Wheels, 4-Wheels
        - Suspension - Full-Thrust, Full-Boom
        
        
        
        The rules are created as follows 
        1. If Transmission=Manual And Set Wheel-drive=4-Wheels Error "Incompatible combination". 
        2. If Transmission=Auto And Set Wheel-drive=4-Wheels Info "Optimum configuration". 
        3. If Engine=Diesel And Transmission=Manual Warning "Suspension should be Full-Thrust". 
        4. If Engine=Petrol And Transmission=Manual Warning "Suspension should be Full-Boom". 
        
        The response of operation for filter criteria will be as follows 
        Criteria: { Group: Engine-Box, Family:-, Feature:-} - Rules returned will be 1,2,3,4. 
        Criteria: { Group: Engine-Box, Family: Engine, Feature:-} - Rules returned will be 3 and 4. 
        Criteria: { Group: Engine-Box, Family: Engine, Feature:Diesel} - Rules returned will be 3. 
        Criteria: { Group: -, Family: -, Feature: Manual} - Rules returned will be 1,3,4.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getIncludeRules',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'filterCriteria': filterCriteria, 'severities': severities},
            response_cls=ServiceData,
        )

    @classmethod
    def getModelsForProduct(cls, context: Cfg0ConfiguratorPerspective, leafLevelOnly: bool) -> ServiceData:
        """
        This internal operation returns the product model instances for the given product item(s) in parameter context. 
        If the parameter ''leafLevelOnly'' is set to true, then all the product models (or subtypes) are returned and
        the summary models (or subtypes) are ignored. 
        
        
        Use cases:
        This operation can be used to retrieve the models for the product item(s).
        
        The product item "Car" has following option families and product models LXI,VXI,LDI and VDI in model family
        "Models". The product item also has summary models created "Petrol Models" and "Diesel Models" in summary model
        family "Summaries".
        
        User can use operation 'getModelsForProduct' as follows:
        
        If user wants to get all models i.e. product models and summary models, the parameter 'leafLevelOnly' should be
        passed as FALSE.
        
        If user wants get only product models i.e. LXI,VXI,LDI and VDI, the parameter 'leafLevelOnly' should be passed
        as TRUE.
        
        
        
        
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getModelsForProduct',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'leafLevelOnly': leafLevelOnly},
            response_cls=ServiceData,
        )

    @classmethod
    def getOptionFamilies(cls, context: Cfg0ConfiguratorPerspective, groups: List[Cfg0AbsFamilyGroup], otherFamilies: bool, unavailableFamilies: bool) -> GetOptionFamiliesResponse:
        """
        This internal operation returns the option family instances given 'context' information. If the product item(s)
        member is provided in context, then the option families that are allocated to any of the specified product
        item(s) are returned. If the product models member is provided in 'context', then the option families that are
        made available to at least one of given the product model(s) are returned.
        
        In addition, to filter the option families further, the ''groups'' input parameter can be leveraged. If this
        parameter is populated with the family group instances or IDs, then the option families that are allocated to
        any of the specified product item(s) and which are members of the specified family group instances are returned.
        If the parameter ''otherFamilies'' is set to 'true', then operation will return that option families which are
        not the members of any family group instances however are allocated to at least one of the specified product
        item(s).
        The default value for this parameter is 'false', which guides the system to only return the Option Families
        from the Family Groups specified in the input parameter 'groups'. 
        If  parameter ''unavailableFamilies'' is set to true, option families those are the  members of any of the
        specified groups and are allocated to specified product context are returned even if their availability rule is
        in an 'unavailable' state. 
        
        Note:  In Teamcenter 10.1.2 the product model(s) member of context is ignored.
        
        Use cases:
        This operation can be used to retrieve families for the given product item(s) or product model(s) from
        parameter 'context'. Parameter 'filterCriteria' can be used for filtering based on specific family group(s) or
        family (families) or feature(s). 
        
        Consider that following set data: 
        Groups: 
        Engine-Box - It has families "Engine" and "Transmission". 
        - Engine- Petrol, Diesel
        - Transmission - Manual, Auto
        
        
        
        Wheel - It has families "Wheel-drive" and "Suspension". 
        - Wheel-drive - 2-Wheels, 4-Wheels
        - Suspension - Full-Thrust, Full-Boom
        
        
        
        
        The response of operation for filter criteria will be as follows 
        Criteria: { Group: Engine-Box, Family:-, Value:-} - Option families returned will be Engine and Transmission. 
        Criteria: { Group: Engine-Box, Family: Engine, Value:-} - Option families returned will be Engine.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getOptionFamilies',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'groups': groups, 'otherFamilies': otherFamilies, 'unavailableFamilies': unavailableFamilies},
            response_cls=GetOptionFamiliesResponse,
        )

    @classmethod
    def executeSearch(cls, searchRecipe: SearchRecipe, searchOptions: SearchOptions) -> SearchResponse:
        """
        Executes a search based on a search recipe. The search results can contain any sub-types of POM_Object. The
        search recipe could be a complex search definition that combines multiple simpler search definitions in a
        logical sequence, e.g. multiple saved queries as defined in the Teamcenter application QueryBuilder.
        
        The search is executed in the context of a configurator perspective (Cfg0ConfiguratorPerspective). Configurator
        objects such as features, or constraint rules, are filtered based on their relationship to the product context
        items and product models in the configurator perspective.
        
        Variant and effecitvity configurable objects in the search results are filtered according to the criteria
        associated with the VariantRule and RevisionRule in the configurator perspective.
        
        Revisable objects in the search results are revision configured according to the RevisionRule in the
        configurator perspective.
        
        The results of a search are returned in batches based on the 'defaultLoadCount' specified in the search
        options. A search cursor object is returned in the response with which subsequent batches can be requested with
        operation 'fetchNextSearchResults'.
        
        Search options may be used to sort the results of a search using one or more attributes of the returned objects.
        
        Use cases:
        1. Get models for product. Provide product context, revision rule and filter list in parameter
        'searchRecipe'.'configuratorPerspecitve', 'searchRecipe'.'searchExpression'.'savedQueries' contains a saved
        query for searching models.
        
        2. Get Family Groups. Provide product context, revision rule and filter list in parameter
        'searchRecipe'.'configuratorPerspective'; 'searchRecipe'.'searchExpression'.'savedQueries' contains a saved
        query for searching Family Groups.
        
        3. Get Option Families. Provide product context, revision rule and filter list in parameter
        'searchRecipe'.'configuratorPerspecitve'; 'searchRecipe'.'searchExpression'.'savedQueries' contains a saved
        query for searching families. 
        
        4. Get Option Values. Provide product context, revision rule and filter list in parameter
        'searchRecipe'.'configuratorPerspecitve'; 'searchRecipe'.'searchExpression'.'savedQueries' will have a saved
        query for searching features.
        
        5. Get Derived Default Rules. Provide product context, revision rule and filter list in parameter
        'searchRecipe.configuratorPerspecitve; searchRecipe.searchExpression.savedQueries' will have a saved query for
        searching derived default rules, 'searchRecipe'.'searchExpression'.'filterCriteria' will have the filter
        information.
        
        6. Get Exclude Rules. Provide product context, revision rule and filter list in parameter
        'searchRecipe.configuratorPerspecitve; searchRecipe.searchExpression.savedQueries' will have a saved query for
        searching exclude rules, 'searchRecipe'.'searchExpression'.'filterCriteria' will have the filter information.
        
        7. Get Include Rules. Provide product context, revision rule and filter list in parameter
        'searchRecipe.configuratorPerspecitve; searchRecipe.searchExpression.savedQueries' will have a saved query for
        searching include rules,'searchRecipe.searchExpression.filterCriteria' will have the filter information.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='executeSearch',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'searchRecipe': searchRecipe, 'searchOptions': searchOptions},
            response_cls=SearchResponse,
        )

    @classmethod
    def getOptionValues(cls, context: Cfg0ConfiguratorPerspective, groups: List[Cfg0AbsFamilyGroup], families: List[Cfg0AbsOptionFamily], unavailableValues: bool) -> GetOptionValuesResponse:
        """
        This internal service operation returns the feature instances based on the specified 'context' and other
        parameters. If product item(s) member is provided in the 'context', then the features that are allocated to any
        of the product items are returned.  If product model(s) member is provided in the context, then the features
        that are made available to any of the product models are returned.
        If 'groups' parameter is populated with the family group instances, then only those feature instances which
        belong to the family instances of given list of family group members are returned.
        If 'families' parameter is populated with the family instances, then only those feature instances which belong
        to the given family instances are returned.
        If 'unavailableValues' is set to 'true', it would also return the features which are marked with negative
        availability. 
        
        Note: In Teamcenter 10.1.2 the product model(s) member in context is not considered. This member is used for
        availability feature and this feature will be supported in Teamcenter 10.1.3 onwards.
        
        Use cases:
        This operation can be used to retrieve features for the given product item(s) or product model(s) from
        parameter 'context'. Parameter 'filterCriteria' can be used for filtering based on specific family group(s) or
        family (families) or feature(s). 
        
        Consider that following set data: 
        Groups: 
        Engine-Box - It has families "Engine" and "Transmission". 
        - Engine- Petrol, Diesel
        - Transmission - Manual, Auto
        
        
        
        Wheel - It has families "Wheel-drive" and "Suspension". 
        - Wheel-drive - 2-Wheels, 4-Wheels
        - Suspension - Full-Thrust, Full-Boom
        
        
        
        
        The response of operation for filter criteria will be as follows 
        Criteria: { Group: Engine-Box, Family:-, Feature:-} - Features returned will be Petrol, Diesel, Manual and
        Auto. 
        Criteria: { Group: Engine-Box, Family: Engine, Feature:-} - Features returned will be Petrol and Diesel.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getOptionValues',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'context': context, 'groups': groups, 'families': families, 'unavailableValues': unavailableValues},
            response_cls=GetOptionValuesResponse,
        )

    @classmethod
    def getProductDefaults(cls, inputs: List[ProductDefaultsInput]) -> GetProductDefaultsResponse:
        """
        Gets the results of applying default rules to a set of input expressions in the context of the associated
        Cfg0ConfiguratorPerspective objects.
        
        Use cases:
        The 'getProductDefaults' operation can be used in following ways: 
        
        Example 1: System has default rule which states "If TYPE=CLASSIC and ENGINE=V4 then Apply COLOR=RED" 
        
        If user provides input as "TYPE=CLASSIC and ENGINE=V4" then response provided by operation as  "TYPE=CLASSIC
        and ENGINE=V4 and COLOR=RED" in  'expressionsWithDefaults'.
        
        To filter response based on option families 
        
        Example 2: System has default rule which states "If TYPE=CLASSIC and ENGINE=V4 then Apply COLOR=RED"
        
        If user provides input expression to getProductDefaults SOA as TYPE=CLASSIC and ENGINE=V4
        Input filter of Families is provided as TYPE AND ENGINE AND COLOR
        
        Then output of SOA in expressionsWithDefaults is expected as TYPE=CLASSIC and ENGINE=V4 and COLOR=RED
        
        Example 3: System has default rule which states "If TYPE=CLASSIC and ENGINE=V4 then Apply COLOR=RED"
        
        If user provides input expression to getProductDefaults SOA as "TYPE=CLASSIC and ENGINE=V4"
        Input filter of Families is provided as TRANSMISSION
        
        Then output of SOA in expressionsWithDefaults is expected same as input. Because the family provided in filter
        does not match with any of the term in updated expression.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getProductDefaults',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=GetProductDefaultsResponse,
        )

    @classmethod
    def getVariantCache(cls, productItem: ItemRevision, revRule: RevisionRule, productModelUID: str, productItemUID: str) -> GetVariantCacheInfoResponse:
        """
        This operation is designed to download revision configured variant data from a higher Teamcenter release at
        real time. Use this operation if data model changes in a higher Teamcenter release make it impossible to use
        offline data replication. The local replica of the product context ItemRevision will contain a stub
        VariantExpressionBlock.
        
        Use cases:
        'GetVariantCache' can be invoked to fetch variant data such as families, features and rules.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='getVariantCache',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'productItem': productItem, 'revRule': revRule, 'productModelUID': productModelUID, 'productItemUID': productItemUID},
            response_cls=GetVariantCacheInfoResponse,
        )

    @classmethod
    def getVariantExpressionDisplayStrings(cls, inputs: List[ConfigExpressionDisplayStringInput], revRule: RevisionRule) -> GetDisplayStringResponse:
        """
        This operation converts the input variant expressions of boolean expression format into displayable or user
        readable format.
        
        Use cases:
        This operation can be used to display formulae for 'ConfigExpression' structures returned by
        'getVariantExpressions' operation. The examples of display formulae are as follows:
        (NS is family namespace)
        
        1)    Boolean expression
        -  [NS]BOOL - reprepsents TRUE
        -  [NS]!BOOL - reprepsents FALSE
        
        
        
        2)    Date expressions
        -  [NS]REL_DATE = 22-Jan-2013 00:00      (dd-mmm-yyyy  HH:SS)
        
        
        
        3)    Range expressions
        -  [NS]A = a1 & [NS]LENGTH <= 50
        -  [NS]A = a1 & ([NS]LENGTH >= 1 & [NS]LENGTH <= 10)
        -  [NS]A = a1 & [NS]LENGTH >= 20
        -  [NS]A = a1 & !([NS]LENGTH >= 20)
        
        
        
        4)    Multiple column expressions must be grouped within brackets
        -  ([NS]A = a1 & [NS]B = b1) | ([NS]A = a2 & [NS]C = c1)
        
        
        
        5)    Multiple selections within a single column
        - ([NS]A = a1 | [NS]A = a2) & [NS]B = b1
        
        
        
        6)    Multiple selections in a family 'C' that has Multi-select=Yes
        - ([NS]A = a1 | [NS]A = a2) & [NS]C = c1 & [NS]C = c2
        
        
        
        7)    Optional family 'D' [Target]
        -  [NS]A = a1 & [NS]D = NONE (same as [NS]D = '')
        -  [NS]A = a1 & [NS]D = ANY (same as [NS]D != '')
        
        """
        return cls.execute_soa_method(
            method_name='getVariantExpressionDisplayStrings',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs, 'revRule': revRule},
            response_cls=GetDisplayStringResponse,
        )

    @classmethod
    def fetchNextSearchResults(cls, searchCursor: Cfg0SearchCursor, loadCount: int) -> SearchResponse:
        """
        This operation gets the next set of objects in the search result of a previously executed search. The returned
        results will be based on the load count specified in the SearchCursor input structure.
        
        Use cases:
        This API is used in conjunction with 'executeSearch' operation. 'executeSearch' operation is a prerequisite for
        invoking 'fetchNextSearchResults'. The search cursor returned by the 'executeSearch' is used to call
        'fetchNextSearchResults' operation. This operation could be called repeatedly by the caller, until all the
        search results are returned.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='fetchNextSearchResults',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'searchCursor': searchCursor, 'loadCount': loadCount},
            response_cls=SearchResponse,
        )

    @classmethod
    def stopSearch(cls, searchCursor: Cfg0SearchCursor) -> ServiceData:
        """
        This operation stops further loading of objects from a previously executed search and clears all the memory
        allocated for the search operation. It deletes the search cursor and the list of  Objects that are kept track
        by the Search cursor from the Server Memory. 
        
        The 'stopSearch' does not unload any previously loaded objects. Also there is no locking or unlocking performed
        by the 'stopSearch' operation. 
        
        
        Use cases:
        When a search is executed in Advanced Configurator and the search returns a large set of objects. The server
        process keeps the results of a search using a search cursor object. At each 'fetchNextSearchResults' operation,
        the results are further filtered and returned in batches specified by the load count. However if the caller is
        not interested in consuming the search results further, then a 'stopSearch' could be called to release all the
        resources allocated for that search operation. This includes dropping the runtime search cursor object and the
        list of Configurator Objects kept track by the cursor.
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='stopSearch',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'searchCursor': searchCursor},
            response_cls=ServiceData,
        )

    @classmethod
    def validateProductConfiguration(cls, inputs: List[ValidateProductConfigInput]) -> ValidateProductConfigurationResponse:
        """
        Validates the given expression by applying the constraint rules and returns violations and an updated
        expression resulting from the application of include rules that can be set on the expression.
        
        The value of TC_Default_Solve_Type preference is used for using solve type for this operation.
        
        Values for 'applyConstraints' are as integrated as follows
         1 //enable configurator constraint evaluation
        + 8 //report warnings in addition to errors
        + 16 //also report informational messages
        + 32 //don't stop if a violation is encountered
        + 256 //skip the check against _allocated_ variability which could raise a 
            "k_variant_criteria_outside" validation failure
        + 1024 //skip criteria update based on validation rules (For example configurator exclusion rule). If this flag
        is not set then the operation will update the variant criteria after applying validation rules.
        + 2048 //enable Availability Constraint evaluation.
        
        
        Use cases:
        This' 'operation validates the given variant expression for the product item.
        
        Use case 1:
        Consider that user has created exclusion rule which states If TYPE=CLASSIC and ENGINE=V4 And COLOR=RED then
        Error "COLOR cannot be RED for CLASSIC V4 model". 
        
        Now if user provides input expression as "TYPE=CLASSIC and ENGINE=V4 and COLOR=RED" to
        validateProductConfiuration operation to validate the expression. Then in output of the operation a violation
        is expected with message as "COLOR cannot be RED for CLASSIC V4 model". 
        
        Use Case 2:
        Consider that user has created an availability say 'RED' is available to model 'LUXURY'. User has not defined
        availability of 'BLUE' for model 'LUXURY'.
        Now, if availability constraint evaluation is enabled and user provides an expression as "MODEL=LUXURY and
        COLOR=BLUE", then in the output of the operation a violation is expected with message as "The Feature "BLUE" is
        not available to the following product models: LUXURY".
        
        Exceptions:
        >No error conditions result at this time for this operation.
        """
        return cls.execute_soa_method(
            method_name='validateProductConfiguration',
            library='Internal-Configurator',
            service_date='2014_06',
            service_name='ConfiguratorManagement',
            params={'inputs': inputs},
            response_cls=ValidateProductConfigurationResponse,
        )
