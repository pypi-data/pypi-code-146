from __future__ import annotations

from tcsoa.gen.Core._2015_07.DataManagement import CreateIn2, CreatableSubBONamesInput, LocalizedPropertyValuesResponse, PropertyNamingruleInfo, DomainOfObjectOrTypeResponse, GetDomainInput, DeepCopyDataInput, CreatableSubBONamesResponse, GetDeepCopyDataResponse
from tcsoa.gen.Core._2008_06.DataManagement import CreateResponse
from tcsoa.gen.Core._2013_05.DataManagement import GenerateNextValuesResponse
from typing import List
from tcsoa.gen.Core._2010_04.DataManagement import PropertyInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createRelateAndSubmitObjects2(cls, createInputs: List[CreateIn2]) -> CreateResponse:
        """
        This is a generic operation for creation of business objects. This will also create any secondary (compounded)
        objects that need to be created, assuming the CreateInput2 for the secondary object is represented in the
        recursive CreateInput2 object e.g. Item is primary object that also creates Item Master and ItemRevision.
        ItemRevision in turn creates ItemRevision Master. The input for all these levels is passed in through the
        recursive CreateInput2 object.
        This operation also performs following tasks:
        &bull;  Relate the created business object and the additional data passed in through the dataToBeRelated input
        of CreateIn2 object.
        &bull;  Submit the created business object to the workflow process. The input for creating the workflow process
        is passed in through the workflowData input of CreateIn2 object.
        &bull;  Relate the created business object to the input target object.
        
        Use cases:
        Use this operation to create an object after obtaining user input on the fields of the create dialog. This call
        is typically preceded by a call to Teamcenter::Soa::Core::_2008_06::PropDescriptor::getCreateDesc or to the
        Client Meta Model layer to retrieve Create Descriptor for a business object.
        Create Item
        For example, to create an Item, client will get the Create Descriptor associated with the Item from the client
        Meta model (The associated descriptor type can be found by looking at the constant value for the CreateInput
        constant that is attached to Item). Alternatively, for clients that do not use the client Meta model, the
        Descriptor for Item can be obtained by invoking getCreateDesc operation. The descriptor information can then be
        used to populate the Create dialog for the business object. Once the Create dialog is populated the
        createObjects operation can be called to create the object.
        Create Problem Report
        User want to create a new Problem Report (Change) object and attach an existing Word doc dataset as "Reference"
        or "ProblemItem" relation. Here User also wants to submit the created Problem Report object to the workflow
        with predefined Workflow template for Problem Report object type.
        """
        return cls.execute_soa_method(
            method_name='createRelateAndSubmitObjects2',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'createInputs': createInputs},
            response_cls=CreateResponse,
        )

    @classmethod
    def generateNextValuesForProperties(cls, propertyNamingRuleInfo: List[PropertyNamingruleInfo]) -> GenerateNextValuesResponse:
        """
        This operation generates values for the given properties of an object(s) during create/revise/save as action
        based on the user exits or naming rules configured on those properties.Customer user exits are given priority
        over the naming rules if both of them are configured on the same property. The counter has to be set active on
        the naming rule in order to generate the next value for a property. This operation also performs naming rule
        and multi field key validation on the generated values and return appropriate partial errors if the validation
        fails.
        
        For user exit support, an existing user exit will be called to generate values. Right now we support below
        given user exits for corrosponding Objest type.
        
        Object: Item
        User exit name: USER_new_item_id
        Property: item_id
        
        Object: ItemRevision
        User exit name: USER_new_revision_id, USER_new_revision_id_from_alt_rule(Baseline)
        Property: item_revision_id
        
        Object: Dataset
        User exit name: USER_new_dataset_id
        Property: pubr_object_id
        
        Object: Dataset
        User exit name: USER_new_dataset_rev
        Property: rev
        
        Object: Identifier
        User exit name: IDFR_new_alt_id, IDFR_new_rev_id(In Revise case)
        Property: idfr_id
        
        Object: CPD Objects
        User exit name: USER_new_cpd_id
        Property: CPD Objects related property
        
        These each user exits need some specific inputs which are required by them to generate ids. These inputs are
        part of "generateNextValuesIn" structure and are described in details in its description.
        
        
        Use cases:
        a)    User clicks on assign button in Create/Revise/Saveas dialog:
        
        Autoassignable properties are those that have either a user exit or a naming rule with counter configured.A
        constant "autoassignable" is defined on the PropertyDescription class and its value can be obtained using
        PropertyDescription.getConstant() API. "Assign" button is displayed in create/revise/save as dialog to populate
        their values.
        
        This operation is used to generate the values for the autoassignable properties when the user clicks on the
        "Assign" button.The caller should collect the list of all autoassignable properties that do not have any user
        input and pass them to this operation. If the autoassignable property has a naming rule , the naming rule
        pattern selected by the user for that property should also be passed as input to this operation. In all other
        cases the naming rule pattern should be passed as empty string.
        
        b)    User clicks on finish button in Create/Revise/Saveas dialog:
        
        This operation is also used to generate the values for the autoassignable properties when the user clicks
        "Finish" button in in create/revise/save as dialog. The caller should collect the list of all autoassignable
        properties that do not have any value generated and pass them to this operation. If the autoassignable property
        has a naming rule , the naming rule pattern selected by the user for that property should also be passed as
        input to this operation. In all other cases the naming rule pattern should be passed as empty string.
        """
        return cls.execute_soa_method(
            method_name='generateNextValuesForProperties',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'propertyNamingRuleInfo': propertyNamingRuleInfo},
            response_cls=GenerateNextValuesResponse,
        )

    @classmethod
    def getCreatbleSubBuisnessObjectNames(cls, input: List[CreatableSubBONamesInput]) -> CreatableSubBONamesResponse:
        """
        This operation returns sub business object  names that are displayable to the login user in the object creation
        dialog and their display names for each primary business object given as the input, based on specified context.
        Returned business object lists have exclusions of business objects and their secondary business objects as per
        the exclusion preference and/or exlusion business object names specified in the input. If the context is
        specified as legacy, the sub business objects of the primary business object are returned only if the primary
        business object is listed in the site preference TYPE_DISPLAY_RULES_list_types_of_subclasses. If the context is
        left blank, then all creatable sub business objects are returned. This operation returns the hierarchy of
        creatable objects for each business object it returns.
        
        Use cases:
        Use Case 1: Get all Creatable sub business object names for a given business object
        While creating an object of a business object, user needs to know all the sub business objects that can be
        created. To get all creatable sub business objects for a given business object for the logged in user, this
        operation should be invoked by providing empty value for context. Any specific sub business objects that need
        to be excluded from the returned list, can be specified through exclusionPreference and/or exclusionBONames
        parameters.
        
        Use Case 2: Get Creatable sub business objects for a given primary business object, excluding sub business
        objects from its sub classes
        While creating an object of a primary business object, user needs to know only the sub business objects that
        can be created for the primary business object, excluding the business objects from its sub classes, for
        example, in the legacy Create wizards from Teamcenter Rich Application Client. To get only the creatable direct
        sub business objects for a given primary business object for the logged in user, this operation should be
        invoked by providing legacy as the value for context parameter.
        """
        return cls.execute_soa_method(
            method_name='getCreatbleSubBuisnessObjectNames',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreatableSubBONamesResponse,
        )

    @classmethod
    def getDeepCopyData(cls, deepCopyDataInput: DeepCopyDataInput) -> GetDeepCopyDataResponse:
        """
        This operation returns information required to perform save-as/revise after user changes the default copy
        action to one of the following copy actions for one of the secondary objects:
        - Copy As Object
        - Revise Object
        - Revise and Relate to Latest
        
        
        
        Use cases:
        After a user changes the copy action for one of the secondary objects in the DeepCopy panels, Client will need
        to call this operation to construct the DeepCopy panels in save-as wizard for user input for that secondary
        object. Once the user input is received, client can make subsequent invocation to the
        DataManagement.saveAsObjectsAndRelate operation to execute SaveAs on the object. 
        """
        return cls.execute_soa_method(
            method_name='getDeepCopyData',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'deepCopyDataInput': deepCopyDataInput},
            response_cls=GetDeepCopyDataResponse,
        )

    @classmethod
    def getDomainOfObjectOrType(cls, inputs: List[GetDomainInput]) -> DomainOfObjectOrTypeResponse:
        """
        This operation identifies the application domain information of the input design artifact object or type name
        and the domain value will be returned as part of the response. The input object can be any WorkspaceObject. The
        application domain where the object or the type belongs to is returned as domain value.  Out of the box the
        supported application domains are "Mechanical" and "Automation". The domain information is identified based on
        preferences. Every application domain will have a preference with type name applicable for it and preference
        with syntax as "MECH_domain_types_"+DomainName  [eg. MECH_domain_types_Automation]. And the domain name will be
        added to a master preference "MECH_domain_list".  For legacy objects whose domain information cannot be
        identified from type,  will have to have Fnd0AppDomain object associated with it. And Fnd0AppDomain will have
        the domain information. Based on the Fnd0AppDomain or the preference the domain of the input object or type
        will be identified.
        
        Use cases:
        When domain information for a design artifact (WorkspaceObject) cannot be identified by type name, user uses
        the exposed utility associate_domain_data to associate domain information.
        User, who wants to know the application domain where a design artifact (WorkspaceObject) or type belongs to,
        uses this operation to query for the domain information.
        """
        return cls.execute_soa_method(
            method_name='getDomainOfObjectOrType',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=DomainOfObjectOrTypeResponse,
        )

    @classmethod
    def getLocalizedProperties2(cls, propertyInfo: List[PropertyInfo]) -> LocalizedPropertyValuesResponse:
        """
        Typically business object property values are returned in the locale of the current session, this operation
        returns desired property values in any of the supported locales of the Teamcenter server. String type
        properties may be localized with values for each supported locale, this operation will return the translated
        values for one or more desired locales.
        
        Use cases:
        Retrieve the localized values for localizable property
        
        When running Teamcenter in language environment other than the English, user wants to see the localized
        property value to be displayed in corresponding language in the UI. This operation can be used to fulfill this
        requirement. By providing the desired business object, internal name of the properties, and specific locale
        name(s), this operation will return the localized property value(s) in that particular locale(s) and the
        internal value(s) of the status corresponding to localized value(s) in that locale(s).
        """
        return cls.execute_soa_method(
            method_name='getLocalizedProperties2',
            library='Core',
            service_date='2015_07',
            service_name='DataManagement',
            params={'propertyInfo': propertyInfo},
            response_cls=LocalizedPropertyValuesResponse,
        )
