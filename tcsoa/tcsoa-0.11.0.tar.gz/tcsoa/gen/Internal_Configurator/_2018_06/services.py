from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Cfg0ConfiguratorPerspective
from tcsoa.gen.Internal.Configurator._2018_06.ConfiguratorManagement import MatrixCell, GetVariabilityResponse, ExpressionMatrix, GetConfigurationSessionInfoResponse, ValidateProductConditionResponse
from typing import List
from tcsoa.base import TcService


class ConfiguratorManagementService(TcService):

    @classmethod
    def getConfigurationSessionInfo(cls, sessionConfigObjs: List[BusinessObject]) -> GetConfigurationSessionInfoResponse:
        """
        This operation retrieves the Product Configurator configuration session information from the objects that are
        marked to carry such information. User starts a Product Configurator session to create product configurations
        using configuration features. The session holds product information such as the, Cfg0ConfContext, RevisionRule,
        Effectivity, Rule Date. The product information is also represented as Cfg0ConfiguratorPerspective object. The
        product information configures the features  which user can select to build product configuration. The session
        also holds parameters called as Configuration Profile which govern the evaluation of configurator constraints
        during validation and expansion of the product configuration. The objects must implement ConfigurationSession
        behavior, so that Product Configurator configuration session information can be attached and retrieved from
        them.
        
        Use cases:
        User wants to view a Configurator Criteria which has the Product Configurator configuration session information
        attached. User may use this information to apply the product configuration associated with the Configurator
        Criteria on product content and configure it. The session information will recreate the Product Configurator
        configuration session with features and constraints against which the product content configuration will be
        evaluated.
        """
        return cls.execute_soa_method(
            method_name='getConfigurationSessionInfo',
            library='Internal-Configurator',
            service_date='2018_06',
            service_name='ConfiguratorManagement',
            params={'sessionConfigObjs': sessionConfigObjs},
            response_cls=GetConfigurationSessionInfoResponse,
        )

    @classmethod
    def getVariability(cls, configuratorPerspectives: List[Cfg0ConfiguratorPerspective]) -> GetVariabilityResponse:
        """
        This operation returns variability for list of input Configurator perspectives. The variability can be all
        configured model families, models, groups, families and values based on the corresponding Configurator Context
        Item, Revision Rule, Effectivity and Rule date in the input Configurator perspectives. If an allocated object
        is a member of a group it will be returned as grouped variability. Otherwise it will be returned as ungrouped
        variability.
        
        Use cases:
        The getVariability operation should be invoked to fetch variability such as all configured model families,
        models, groups, families and values based on the corresponding Configurator Context Item, Revision Rule,
        Effectivity and Rule date in the input Configurator perspective.
        
        Example:
        Consider the following Variability data in a Configurator context:
        Car_Product_Context
        Models
            ATS
            CTS
        Group
            Engine (Cfg0LiteralValueFamily) - Released
                2.0L Turbo (Cfg0LiteralOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                3.0L (Cfg0LiteralOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                SumValue1
                3.0L Turbo (Cfg0LiteralOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                SumValue1
            Fuel (Cfg0LiteralValueFamily) - Working
                Diesel (Cfg0LiteralOptionValue) - Working   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                Electrical (Cfg0LiteralOptionValue) - Working   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
            Transmission (Cfg0LiteralValueFamily) - Released
                Automatic (Cfg0LiteralOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                Manual (Cfg0LiteralOptionValue) - Released   Effectivity: 01-Jan-2026&hellip;31-Dec-2030
            FeatureColor (Cfg0FeatureFamily) - Released
                Red (Cfg0Feature) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                Green (Cfg0Feature) - Released   Effectivity: 01-Jan-2026&hellip;31-Dec-2030
            StandAloneFeature (Cfg0Feature)
                StandAloneFeature (Cfg0Feature) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
        Unassigned Families
            FeatureSet (Cfg0FeatureSet) - Released
                StandAloneFeature (Cfg0Feature) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                Green (Cfg0Feature) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
            SummaryFamily (Cfg0SummaryOptionFamily) - Released
                SumValue1 (Cfg0SummaryOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
            PackageFamily (Cfg0PackageOptionFamily) - Released
                PackageValue1 (Cfg0PackageOptionValue) - Released   Effectivity: 01-Jan-2021&hellip;31-Dec-2030
                        Electrical
                        Green
        Use case 1:
        &#61656;   Configurator Context Item : Car_Product_Context
        &#61656;   Revision Rule: Any Status; Working
        &#61656;   Effectivity: No Effectivity
        &#61656;   Rule date: System Default
        The output of getVariability operation will be all the variability mentioned above.
        Use case 2:
        &#61656;   Configurator Context Item: Car_Product_Context
        &#61656;   Revision Rule: Any Status; Working
        &#61656;   Effectivity: 01-Jan-2020&hellip;31-Dec-2025
        &#61656;   Rule date: System Default
        The output of getVariability operation will be all the variability mentioned above except Manual value of
        Transmission family and Green feature of FeatureColor family, because their effectivity is not present in the
        input effectivity criteria.
        Use case 3:
        &#61656;   Configurator Context Item: Car_Product_Context
        &#61656;   Revision Rule: Any Status; No Working
        &#61656;   Effectivity: No Effectivity
        &#61656;   Rule date: System Default
        The output of getVariability operation will be all the variability mentioned above except Fuel family and its
        Diesel and Electrical option values because they are not released and input Revision Rule is Any Status; No
        Working.
        """
        return cls.execute_soa_method(
            method_name='getVariability',
            library='Internal-Configurator',
            service_date='2018_06',
            service_name='ConfiguratorManagement',
            params={'configuratorPerspectives': configuratorPerspectives},
            response_cls=GetVariabilityResponse,
        )

    @classmethod
    def validateProductConditions(cls, sessionConfigObj: BusinessObject, expressionMatrix: ExpressionMatrix, matrixSubset: List[MatrixCell]) -> ValidateProductConditionResponse:
        """
        This operation process cells of Expression matrix expressionMatrix to validate satisfiability of Expression(s)
        against optional scope Expression(s). Expression matrix row(s) represents Expressions(s) to validate and
        column(s) represent scope Expression(s). So each cell in the Expression matrix represents a combination of two
        expressions, one is referred to as an "Expression to validate" the other as a "Scope Expressions".
        
        Cell(s) of the Expression matrix to be process for validation operation are determined with matrixSubset which
        is a list of cells of Expression matrix. Validation operation also does the application of the constraint rules
        such as inclusion rule, exclusion rule or availability rule for the Configurator Perspective.
        
        This operation retrieves the Product Configurator configuration session information from the sessionConfigObj
        object that is marked to carry such information. A operation user starts a Product Configurator session to
        create product configurations using configuration features. The session holds product information such as the,
        Cfg0ConfContext, RevisionRule, Effectivity, Rule Date. The product information is also represented as
        Cfg0ConfiguratorPerspective object. The product information configures the features which user can select to
        build product configuration. The session also holds parameters called as Configuration Profile which govern the
        evaluation of configurator constraints during validation and expansion of the product configuration.
        sessionConfigObj must implement ConfigurationSession behavior, so that Product Configurator configuration
        session information can be attached and retrieved from them. For example operation caller can use VariantRule
        or Cfg0AbsConfiguratorCriteria type of objects to which they can attach required Configuration session
        information.
        The operation response conveys the information about the status of the configuration and independent set of
        constraint rules which are responsible together for conflict to occur.
        
        Use cases:
        Consider the following Variability data and Rules in a Configurator context:
        
        Variability:
        Models  
         ATS 
         CTS 
         SRX 
         Sedan 
        
        Trim 
         Luxury
         Performance
         Premium
        Standard
        
        DriveTrain 
        RearWheel
        xDrive
        
        Engine 
         2.0L Turbo
         3.0L
         3.0L Turbo
        
        Fuel 
         Diesel
         Electrical
         Gasoline
         Hybrid
         
        Transmission 
         Automatic
         Manual
        
        ABS 
         3Wheel
         4Wheel
        
        FrontBreak 
         Disc
         Drum
        
        RearBreak 
         Disc
         Drum
        
        Wheel 
         17"
         18"
         19"
        
        Rules:
        Include Rule1 ATS Model--> Wheel Type = 18"
        Include Rule2 Performance Trim Type -> Transmission = Manual
        Include Rule3   ATS Model--> Trim Type = Performance"
        All the families are non-discretionary families.
        
        Use Case1:
        expressionMatrix populated with Expression To Validate as '(Transmission=Automatic OR Manual) AND Wheel=19"'
        and 
        Scope Expression as &lsquo;Model=ATS'.  In-order to perform validation, matrixSubset need to have an entry as
        (0,0) as index for first expression to validate is 0 and scope expression index is 0.
        
        There are violations and parameter criteriaStatus has value inValid.
        The output of the operation will contain two set of violation lists.
        
        First list will contain Include Rule1 'ATS Model--> Wheel Type = 18"' and
        
        second list will contain following rules 
        Include Rule2 Performance Trim Type -> Transmission = Manual
        Include Rule3   ATS Model--> Trim Type = Performance"
        
        Looking at two set of violation List user will be able to isolate the problem.
        """
        return cls.execute_soa_method(
            method_name='validateProductConditions',
            library='Internal-Configurator',
            service_date='2018_06',
            service_name='ConfiguratorManagement',
            params={'sessionConfigObj': sessionConfigObj, 'expressionMatrix': expressionMatrix, 'matrixSubset': matrixSubset},
            response_cls=ValidateProductConditionResponse,
        )
