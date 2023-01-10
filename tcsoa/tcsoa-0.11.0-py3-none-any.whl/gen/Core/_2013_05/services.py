from __future__ import annotations

from tcsoa.gen.Core._2013_05.DataManagement import GetChildrenInputData, ValidateValuesResponse, ValidateInput, ReviseIn, SubTypeNamesInput, GetPasteRelationsInputData, GenerateNextValuesResponse, GenerateNextValuesIn, SubTypeNamesResponse, ReviseObjectsResponse, GetChildrenResponse, GetPasteRelationsResponse
from tcsoa.gen.Core._2013_05.LOV import LOVData, InitialLovData, LOVSearchResults, ValidateLOVValueSelectionsResponse, LOVInput
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getSubTypeNames(cls, inBOTypeNames: List[SubTypeNamesInput]) -> SubTypeNamesResponse:
        """
        This operation returns sub business object type names for each business object type name given as the input for
        the specified context.
        
        It returns the input base type in the sub business object type names list too.
        """
        return cls.execute_soa_method(
            method_name='getSubTypeNames',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'inBOTypeNames': inBOTypeNames},
            response_cls=SubTypeNamesResponse,
        )

    @classmethod
    def reviseObjects(cls, reviseIn: List[ReviseIn]) -> ReviseObjectsResponse:
        """
        This operation is generic single revise operation for revisable business objects. This operation revises the
        given objects and copies or creates new objects using the data for the property values and deep copy data. Deep
        copy processing is recursive such that relations between secondary objects, or from secondary objects to the
        revised object, are replicated during this revise operation based upon deep copy rule configuration. This
        operation supports codeless configuration of custom properties. The following lists of revisable types are
        supported for this operation:
        - ItemRevision ( foundation template) and its sub-types
        - Identifier ( foundation template ) and its sub-types
        - Mdl0ConditionalElement (CPD solution ) and its sub-types
        
        """
        return cls.execute_soa_method(
            method_name='reviseObjects',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'reviseIn': reviseIn},
            response_cls=ReviseObjectsResponse,
        )

    @classmethod
    def validateValues(cls, inputs: List[ValidateInput]) -> ValidateValuesResponse:
        """
        This' 'operation validates whether the input property values are valid according to defined naming rules and
        specified user exits for the input property.  Also, for the properties used in the multifield key (MFK)
        definition for the input type, this operation validates whether the combined property values makes up a unique
        value.
        
        The 'validateValues' operation can be called before other service operations that create new objects, such as
        the 'createObjects' or 'saveAsObjects' operations, in order to avoid errors that would occur during object
        creation due to invalid property values.  For example, if a large set of objects to be created is passed to the
        'createObjects' operation, where half of the set could fail due to invalid property values, the
        'validateValues' operation could be used to avoid those failures by checking whether the input object property
        values are valid.
        
        All of the input property names and their values should be included in 'ValidateInput' 'propValuesMap'.
        
        For user exit support, an existing user exit will be called if a specific property is specified along with
        additional input according to the user exit parameter names.  The specific property, referred to as the
        identifying property below, dictates which user exit will be called.  The additional input name and its value
        should also be include in 'ValidateInput' 'propValuesMap'.
        
        User exit name: 'USER_validate_dataset_name'
        Identifying property:
            'object_name': The Dataset name to be validated. This must be set in 'propValuesMap'
        Additional user exit parameter names:
            'vdnItemType': The Item type for the new Item, which has not necessarily been created yet.
            'vdnOldDataset': The old Dataset object for SaveAs.
            'vdnOldDatasetOwner': The old ItemRevision object.
            'vdnNewDatasetItemId': The Item ID for the new item, which has not necessarily been created yet.
            'vdnNewDatasetRevisionId': The ItemRevision ID for the new revision, which has not necessarily been created
        yet.
        
        Example 1:
        The following populated ValidateValuesInput will be used to call user exit for validating Dataset name:
        <ns1:ValidateValuesInput 
        <ns1:inputs clientId="42777::Dataset" operationType="0" businessObjectName=" Dataset ">
        <ns1:propValuesMap key="object_name"><ns1:value>DS003183</ns1:value></ns1:propValuesMap>
        </ns1:inputs></ns1:ValidateValuesInput>
        
        Example 2:
        The following populated ValidateValuesInput will be used to call user exit for validating Dataset name:
        <ns1:ValidateValuesInput 
        <ns1:inputs clientId="42777::Dataset" operationType="0" businessObjectName=" Dataset ">
        <ns1:propValuesMap key="object_name"><ns1:value>New DS</ns1:value></ns1:propValuesMap>
        <ns1:propValuesMap key="vdnItemType"><ns1:value>Item</ns1:value></ns1:propValuesMap>
        <ns1:propValuesMap key="vdnOldDataset"><ns1:value> SqYNv38Gx6sBFD </ns1:value> </ns1:propValuesMap>
        <ns1:propValuesMap key=" vdnOldDatasetOwner "><ns1:value></ns1:value></ns1:propValuesMap>
        <ns1:propValuesMap key=" vdnNewDatasetItemId "><ns1:value>003183</ns1:value> </ns1:propValuesMap>
        <ns1:propValuesMap key=" vdnNewDatasetRevisionId"><ns1:value>A</ns1:value> </ns1:propValuesMap>
        </ns1:inputs></ns1:ValidateValuesInput>
        
        User exit name: 'USER_validate_item_rev_id_3'
        The user exit will be called if the specified property is either 'item_id' or item_revision_id along with
        additional input according to the user exit parameter names.
        Identifying property:
            'item_id': The Item ID to be validated.  This must be set in 'propValuesMap'.
        Additional user exit parameter names:
            'item_revision_id': The ItemRevision ID to be validated.  This must be set in 'propValuesMap'.
            'object_type': The type of Item or ItemRevision for which the ID is being validated. If this property is
        not specified, system will use 'businessObjectName' in 'ValidateInput' as 'object_type'.  
            'viriItemObject': For Revise, this is ItemRevsion object&rsquo;s parent Item object. For Create and SaveAs,
        this is optional and can be empty value if specified.
        
        Example 1:
        The following populated ValidateValuesInput will be used to call user exit for validating Item ID:
        <ns1:ValidateValuesInput 
        <ns1:inputs clientId="42777::Item" operationType="0" businessObjectName="Item">
        <ns1:propValuesMap key="item_id"><ns1:value>003183</ns1:value></ns1:propValuesMap>
        </ns1:inputs></ns1:ValidateValuesInput>
        
        Example 2:
        The following populated ValidateValuesInput will be used to call user exit for validating ItemRevision ID:
        <ns1:ValidateValuesInput 
        <ns1:inputs clientId="42777::ItemRevision" operationType="1" businessObjectName="ItemRevision">
        <ns1:propValuesMap key="item_revision_id"><ns1:value>C</ns1:value></ns1:propValuesMap>
        <ns1:propValuesMap key=" viriItemObject "><ns1:value> SqYNv38Gx6sBFD </ns1:value></ns1:propValuesMap>
        </ns1:inputs></ns1:ValidateValuesInput>
        
        User exit name: 'USER_validate_alternate'
        Identifying property:
            'altid_of': The identifiable type object to which the alternate ID is associated.
        Additional user exit parameter names:
            'idcontext': The IDContext object which holds the cardinality rule for the given identifiable type object
        and the Identifier type object.
            'vaAltIdObject': The alternate ID object.
            'vaAltIdType': The Identifier type object.
        
        User exit name: 'USER_validate_alt_id'
        Identifying property:
            'idfr_id': The alternate ID which is to be validated against any of the naming rule associated with the
        Identifier type.
        Additional user exit parameter names:
            'idcontext': No longer used.
            'vaiIdfrType': The name of the Identifier type whose alternate ID is being validated.
            'vaiPatternName': The preferred name of the Identifier type or IdentifierRevision type wh ose alternate ID
        is being validated. Note:' USER_validate_alt_id' will choose 'pattern_name' as validating type if specified and
        will ignore 'idfr_type'.
        
        For the MFK uniqueness validation, it is important to note that the check for uniqueness is done against
        existing objects in Teamcenter and not between separate client inputs.  It is the responsibility of the client
        to validate whether separate input values in a single call would conflict with each other.
        
        The 'ValidateInput' 'operationType' input is currently a placeholder for future functionality that
        differentiates validation according to the workflow type, where validation for creating an object may be
        different then validation for saving an object.
        
        
        Use cases:
        Use Case 1:
        Prior to calling the service operation 'saveAsObjects', which may fail due to an error with any input property
        value, the client would call 'validateValues' for the properties to have Teamcenter check whether the values
        are valid.
        
        Use Case 2:
        Prior to making a call to the service operation 'createObjects' for several objects, the client wants to ensure
        that each object will be created with a unique identifier according to the MFK definition for the object type.
        The client would call 'validateValues' for the properties to have Teamcenter check that the values are valid
        and that the combined values would make a unique MFK value.
        """
        return cls.execute_soa_method(
            method_name='validateValues',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ValidateValuesResponse,
        )

    @classmethod
    def generateNextValues(cls, generateNextValuesIn: List[GenerateNextValuesIn]) -> GenerateNextValuesResponse:
        """
        This operation generates values for the given properties of an object(s) during create/revise/save as action
        based on the user exits or naming rules configured on those properties. Customer user exits are given priority
        over the naming rules if both of them are configured on the same property. The counter has to be set active on
        the naming rule in order to generate the next value for a property. This operation also performs naming rule
        and multi field key validation on the generated values and return appropriate partial errors if the validation
        fails.
        This operation does not support generating values for attached Revision Name Rules on an Object type.
        For user exit support, an existing user exit will be called to generate values. Right now we support below
        given user exits for corresponding Object type.
        
        Object: Item
        User exit name: USER_new_item_id
        Property: item_id
        
        Object: ItemRevision
        User exit name: USER_new_revision_id, USER_new_revision_id_from_alt_rule (Baseline)
        Property: item_revision_id
        
        Object: Dataset
        User exit name: USER_new_dataset_id
        Property: pubr_object_id
        
        Object: Dataset
        User exit name: USER_new_dataset_rev
        Property: rev
        
        Object: Identifier
        User exit name: IDFR_new_alt_id, IDFR_new_rev_id (In Revise case)
        Property: idfr_id
        
        Object: CPD Objects
        User exit name: USER_new_cpd_id
        Property: CPD Objects related property
        
        Each of these user exits need some specific inputs which are required by them to generate IDs. These inputs are
        part of "generateNextValuesIn" structure and are described in details in its description.
        
        Use cases:
        a)    User clicks on assign button in Create/Revise/Saveas dialog:
        
        Autoassignable properties are those that have either a user exit or a naming rule with counter configured.A
        constant "autoassignable" is defined on the PropertyDescription class and its value can be obtained using
        PropertyDescription.getConstant() API. "Assign" button is displayed in create/revise/save as dialog to populate
        their values.
        
        This operation is used  to  generate the values for the autoassignable properties  when the user clicks on the
        "Assign" button.The caller should collect the list of all autoassignable properties  that do not have any user
        input and pass them to this operation. If  the autoassignable  property has a naming rule , the  naming rule
        pattern selected by the user  for  that property should also be passed as input to this operation. In all other
        cases the naming rule pattern should be passed as empty string.
        
        b)    User clicks on finish button in Create/Revise/Saveas dialog:
        
        This operation is also used to generate the values for the autoassignable properties  when the user clicks
        "Finish" button in in create/revise/save as dialog. The caller should collect the list of  all autoassignable
        properties that do not have any value generated and pass them to this operation. If  the autoassignable 
        property has a naming rule , the  naming rule pattern selected by the user  for  that property should also be
        passed as input to this operation. In all other cases the naming rule pattern should be passed as empty string.
        """
        return cls.execute_soa_method(
            method_name='generateNextValues',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'generateNextValuesIn': generateNextValuesIn},
            response_cls=GenerateNextValuesResponse,
        )

    @classmethod
    def getChildren(cls, inputs: List[GetChildrenInputData]) -> GetChildrenResponse:
        """
        This operation returns the children for each input object.  The children returned is determined by the input
        'propertyNames' list of strings which defines the properties which are to be processed in order to collect the
        children to be returned  If the 'propertyNames' list is empty, then the properties which are processed to
        object the children is based on the <Type>_DefaultChildProperties and <Type>_DefaultPseudoFolder preferences. 
        Please see the Preferences and Environment Variables Reference and the RichClient Interface Guide for
        information on configuring these preferences. Children for which the user does not have read-access will be
        excluded from the returned list of children. No partial error is given if the 'propertyNames' list or the
        <Type>_DefaultChildProperties preference contains an invalid property name for the input object, children for
        the remaining 'propertyNames' will be returned.
        
        Use cases:
        Assume the following data exists in Teamcenter:
        Item
            Item Revision
            Item Master Form
        
        The ItemRevision exists in the Item's "revision_list" property.
        Item Item Master Form exists in the Item's "IMAN_master_form" property.
        
        Use case 1 (Get all children/no filter)
        1.    The user selects the Item in the above data in a tree viewer which shows all objects.
        2.    The user clicks the "+" to expand the Item.
        3.    The client then invokes getChildren with the selected object (Item), and no entries in the
        'propertyNames' argument.
        4.    getChildren determines the selected object's type, retrieves <Type>_DefaultChildProperties and
        <Type>_PseudoFolders preferences, and returns the Item Revision and Item Master Form, their type objects, and
        the propertyName in which they exist related to the parent.
        5.    The client then displays the returned list of children as child nodes in the tree.
        
        Use case 2 (Get subset of children/with filter)
        1.    The user selects the Item in the above data in a tree viewer which only shows object related via the
        revision_list property.
        2.    The user clicks the "+" to expand the Item.
        3.    The client then invokes getChildren with the selected object (Item), and gives "revision_list" in the
        'propertyNames' list.
        4.    getChildren iterates over the propertyNames list, and returns the Item Revision object, its child type
        object, and the propertyName in which it exists related to the parent.
        5.    The client then displays the returned list of children as child nodes in the tree.
        """
        return cls.execute_soa_method(
            method_name='getChildren',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=GetChildrenResponse,
        )

    @classmethod
    def getPasteRelations(cls, inputs: List[GetPasteRelationsInputData]) -> GetPasteRelationsResponse:
        """
        Returns the paste relation names for the given parent types and the child types, within which the expandable
        relations and the preferred paste relation are indicated.
        """
        return cls.execute_soa_method(
            method_name='getPasteRelations',
            library='Core',
            service_date='2013_05',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=GetPasteRelationsResponse,
        )


class LOVService(TcService):

    @classmethod
    def validateLOVValueSelections(cls, lovInput: LOVInput, propName: str, uidOfSelectedRows: List[str]) -> ValidateLOVValueSelectionsResponse:
        """
        This operation can be invoked after selecting a value from the LOV.  Use this operation to do additional
        validation to be done on server such as validating Range value, getting the dependent properties values in case
        of interdependent LOV (resetting the dependendent property values), Coordinated LOVs ( populating dependent
        property values )
        """
        return cls.execute_soa_method(
            method_name='validateLOVValueSelections',
            library='Core',
            service_date='2013_05',
            service_name='LOV',
            params={'lovInput': lovInput, 'propName': propName, 'uidOfSelectedRows': uidOfSelectedRows},
            response_cls=ValidateLOVValueSelectionsResponse,
        )

    @classmethod
    def getInitialLOVValues(cls, initialData: InitialLovData) -> LOVSearchResults:
        """
        This operation is invoked to query the data for a property having an LOV attachment. The results returned from
        the server also take into consideration any filter string that is in the input.  This operation returns both
        LOV meta data as necessary for the client to render the LOV and partial LOV values list as specified.
        
        The operation will return the results in the LOVSearchResults data structure. Maximum number of results to be
        returned are specified in the InitialLOVData data structure. If there are more results, the moreValuesExist
        flag in the LOVSearchResults data structure will be true. If the flag is true, more values can be retrieved
        with a call to the getNextLOVValues operation.
        """
        return cls.execute_soa_method(
            method_name='getInitialLOVValues',
            library='Core',
            service_date='2013_05',
            service_name='LOV',
            params={'initialData': initialData},
            response_cls=LOVSearchResults,
        )

    @classmethod
    def getNextLOVValues(cls, lovData: LOVData) -> LOVSearchResults:
        """
        This operation is invoked after a call to getInitialLOVValues if the moreValuesExist flag is true in the
        LOVSearchResults output returned from a call to the getInitialLOVValues operation. The operation will retrieve
        the next set of LOV values
        """
        return cls.execute_soa_method(
            method_name='getNextLOVValues',
            library='Core',
            service_date='2013_05',
            service_name='LOV',
            params={'lovData': lovData},
            response_cls=LOVSearchResults,
        )
