from __future__ import annotations

from tcsoa.gen.BusinessObjects import ApprSearchCriteriaInClass
from tcsoa.gen.Rdv._2012_09.ContextManagement import CreateSearchCriteriaScpResponse, UpdateSearchSCOInputInfo, CreateSearchSCOInputInfo, CreateSearchCriteriaScopeInfo, CreateFormAttrSearchCriteriaInputInfo, CreateSearchSCOResponse, UpdateSearchSCOResponse, CreateFormAttrSearchCriteriaResponse, GetICSClassNamesResponse
from typing import List
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def updateSearchSCO(cls, inputs: List[UpdateSearchSCOInputInfo]) -> UpdateSearchSCOResponse:
        """
        Updates the Search Structure Context Object (SearchSCO) based on the inputs attributes. It sets the following
        properties on SearchSCO object which is to be modified: Product Item Revision, Revision Rule, Variant Rule,
        Work parts selected, Search Criteria Group, Target and Background BOMLine objects, and result status from the
        input structure. This SearchSCO will contain the Item, Item revisions, Target BOMLine objects, Background
        BOMLine objects. The operation is designed to support multiple SearchSCOs creation in a single call. This
        operation first checks for the local ownership of the object to be updated. This operation will fail if null or
        incorrect reference to existing SearchSCO object is passed in the input.
        
        Use cases:
        You can update an SCO object of type SearchStructureContext using 'updateSearchSCO' operation by providing the
        'UpdateSearchSCOInputInfo' structure.
        - Create an SCO, object of SearchStructureContext, using the 'createSearchSCO' operation.
        - Retrieve the reference to SearchStructureContext returned from above step.
        - Modify the required search criteria and populate the 'UpdateSearchSCOInputInfo' structure.
        - Call 'updateSearchSCO' which will modify the existing SearchStructureContext object.
        
        """
        return cls.execute_soa_method(
            method_name='updateSearchSCO',
            library='Rdv',
            service_date='2012_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=UpdateSearchSCOResponse,
        )

    @classmethod
    def createFormAttrSearchCriteria(cls, inputs: List[CreateFormAttrSearchCriteriaInputInfo]) -> CreateFormAttrSearchCriteriaResponse:
        """
        Creates a list of Form Search Criteria objects based on the input parameters. It uses the following inputs from
        the input structure
        - Form type
        - Parent Type
        - Name of the property
        - Type of the property
        - Relation type
        - Operator and 
        - Search value
        
        
        Form Search Criteria object is created as part of creation of the VisStructureContext object to persist form
        attribute search criteria. 
        It is mandatory to provide all the input parameters. This operation will fail if null is provided for any of
        the string input parameters. The Form type or Relation type input should be valid string representing the name
        of a type in Teamcenter database. Empty string for Form type or Relation type input will cause the operation to
        fail.
        
        Use cases:
        1. Creating an Structure Context Oject(SCO)
        While pesristing the search criterias in Structure Context Oject, 'createFormAttrSearchCriteria' operation is
        called to persist the Form serach criteria related information . You can create this object by providing the
        'CreateFormAttrSearchCriteriaInputInfo' structure. This form search criteria object is wrapped in Appearance
        Search Criteria Group object and stored in StructureContext object.
        
        Exceptions:
        >Following are some possible errors returned in 'ServiceData':
        - 202017        The class cannot be instantiated.
        - 39007        The specified name is invalid for a type.
        - 39014        The specified type does not exist.
        
        """
        return cls.execute_soa_method(
            method_name='createFormAttrSearchCriteria',
            library='Rdv',
            service_date='2012_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=CreateFormAttrSearchCriteriaResponse,
        )

    @classmethod
    def createSearchCriteriaScope(cls, inputs: List[CreateSearchCriteriaScopeInfo]) -> CreateSearchCriteriaScpResponse:
        """
        This operation creates the Fnd0ApprSchCriteriaScpAttr object (ScpSrchCriteria) based on the inputs supplied. It
        creates a Scope Search Criteria object and stores the scope of the search. Scope Search Criteria object is
        created as part of the creation of the SearchStructureContext object to persist the scope of the search.
        If the input contains APNs or BOMLine objects, then these are saved in either appearance path nodes list or
        occurrence list property depending on the value of RDV_CREATE_SCO_WITHOUT_APN preference. If the input contains
        appearance groups, these are stored in occurrence group list property of ScpSrchCriteria object.
        
        Use cases:
        1. Creating a Search Search Criteria
        While persisting the search criteria in Search Structure Context object, 'createSearchCriteriaScope' operation
        is called to persist the scope of the search. User can create this object by providing the
        'CreateSearchCriteriaScopeInfo' structure. This scope search criteria object is wrapped in Appearance Search
        Criteria Group object and stored in SearchStructureContext object. 
        """
        return cls.execute_soa_method(
            method_name='createSearchCriteriaScope',
            library='Rdv',
            service_date='2012_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=CreateSearchCriteriaScpResponse,
        )

    @classmethod
    def createSearchSCO(cls, inputs: List[CreateSearchSCOInputInfo]) -> CreateSearchSCOResponse:
        """
        Creates the SearchStructureContext object (SearchSCO) based on the inputs supplied. It creates a SearchSCO
        object and then sets the following properties on SearchSCO object created: Product Item Revision, Revision
        Rule, Variant Rule, Work parts selected, Search Criteria Group, Target and Background BOMLine objects from the
        input structure, result stored status, object shared status. This SearchSCO will contain the Item, Item
        revisions, Target BOMLine objects, Background BOMLine objects. The operation is designed to support multiple
        SearchSCOs creation in a single call. The operation will initially create the SearchSCO object using the name,
        type and description. Subsequently it would set the additional parameters supplied through the input structure.
        SearchSCO object would still be created and saved even if setting of the additional parameters is not
        successful.
        
        Use cases:
        1. Create a Search SCO
        You can create a new SCO object of type SearchStructureContext using 'createSearchSCO' operation, by providing
        the 'CreateSearchSCOInputInfo' structure.
        """
        return cls.execute_soa_method(
            method_name='createSearchSCO',
            library='Rdv',
            service_date='2012_09',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=CreateSearchSCOResponse,
        )

    @classmethod
    def getICSClassNames(cls, searchCriteriaInClass: List[ApprSearchCriteriaInClass]) -> GetICSClassNamesResponse:
        """
        Creates a list of ICS class names for the ApprSearchCriteriaInClass objects passed in the input. Object of ICS
        class is stored inside ApprSearchCriteriaInClass object and this is persisted along with other search criteria
        in Structure Context object (SCO). During replay of SCO, in order to reconstruct the Classification object this
        operation is called to get the class name. Using this class name ICS object is recreated at client side. This
        method is required because the classification object cannot be retrieved in its original format from the SCO
        object.
        
        Use cases:
        1. Replaying an SCO
        You can reconstruct the classification object stored in SCO using the class name returned from the
        'getICSClassNames' operation by providing the reference to the ApprSearchCriteriaInClass object.
        - Create an SCO, object of StructureContext, using the 'createSCO' operation.
        - Retrieve the reference to StructureContext returned from above step.
        - Fetch the reference of ApprSearchCriteriaInClass stored in the Appearance Grouping object.
        - Provide the object retrieved above to 'getICSClassNames' operation.
        
        
        
        Exceptions:
        >Following are some possible errors returned in 'ServiceData':
        - 202023        The attribute of object cannot be retrieved
        - 202024        The object cannot be found.
        
        """
        return cls.execute_soa_method(
            method_name='getICSClassNames',
            library='Rdv',
            service_date='2012_09',
            service_name='ContextManagement',
            params={'searchCriteriaInClass': searchCriteriaInClass},
            response_cls=GetICSClassNamesResponse,
        )
