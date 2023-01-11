from __future__ import annotations

from tcsoa.gen.Core._2012_02.DataManagement import BulkCreIn, WhereUsedResponse, WhereUsedInputData, ValidationResponse, WhereUsedConfigParameters
from tcsoa.gen.Core._2008_06.DataManagement import CreateResponse, CreateIn
from tcsoa.gen.Core._2012_02.OperationDescriptor import DeepCopyDataInput, GetDeepCopyDataResponse
from typing import List
from tcsoa.gen.Core._2012_02.Session import SetPolicyResponse, RegisterIndex
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def registerState(cls, level: str) -> RegisterIndex:
        """
        Register desired level for server state as used by the Server Manager to control server timeout. Note that an
        attempt to register at LEVEL_STATELESS is ignored since this is the default level when no registrations are in
        effect. To move from a higher level to the stateless level the 'unregister' operation should be used to delete
        the earlier registration. Note that it is possible to be registered at more than one level and there may be
        multiple registrations at each level.
        """
        return cls.execute_soa_method(
            method_name='registerState',
            library='Core',
            service_date='2012_02',
            service_name='Session',
            params={'level': level},
            response_cls=RegisterIndex,
        )

    @classmethod
    def setObjectPropertyPolicy(cls, policyName: str, useRefCounting: bool) -> SetPolicyResponse:
        """
        Sets the current object property policy. The business logic of a service operation determines what business
        objects are returned, while the object property policy determines which properties are returned on each
        business object instance. This allows the client application to determine how much or how little data is
        returned based on how the client application uses those returned business objects. The policy is applied
        uniformly to all service operations. 
        By default, all applications use the Default object property policy, defined on the Teamcenter server
        '$TC_DATA/soa/policies/default.xml. 'It is this policy that is applied to all service operation responses until
        the client application changes the policy. Siemens PLM Software strongly recommends that all applications
        change the policy to one applicable to the client early in the session.
        The object property policy is set to the policy named in the file '$TC_DATA/soa/policies/<policyName>.xml' The
        reserved policy name "Empty", will enforce a policy that only returns minimum data required for each object
        (UID and type name).The object property policy will stay in affect for this session until changed by another
        call to 'setObjectPropertyPolicy'.  The full policy is returned where the client application can modify it
        throughout the session via calls to 'updatObjectPropertyPolicy'.
        
        Like any other service operation, this operation cannot be called before establishing a session with the
        'login' serivce operation, so if you need a policy other than the Default policy for the business objects
        returned by the login operation, use the _2011_06 version of the 'login/loginSso' operation to authenticate and
        establish a session without returning business objects. The 'setObjectPropertyPolicy' operation can then be
        called to establish the policy for the session.
        
        
        Exceptions:
        >If the named policy does not exist or there are errors parsing the XML file (error code 214104).
        """
        return cls.execute_soa_method(
            method_name='setObjectPropertyPolicy',
            library='Core',
            service_date='2012_02',
            service_name='Session',
            params={'policyName': policyName, 'useRefCounting': useRefCounting},
            response_cls=SetPolicyResponse,
        )

    @classmethod
    def unregisterState(cls, index: int) -> bool:
        """
        Remove the specified registration.
        """
        return cls.execute_soa_method(
            method_name='unregisterState',
            library='Core',
            service_date='2012_02',
            service_name='Session',
            params={'index': index},
            response_cls=bool,
        )


class DataManagementService(TcService):

    @classmethod
    def validateIdValue(cls, input: List[CreateIn]) -> ValidationResponse:
        """
        This operation determines if the given 'MultiFieldKey' properties are unique based on the 'MultiFieldKey'
        definition.
        
        Use cases:
        Use this operation before creating a new object to validate if the 'MultiFieldKey' property combination is
        already used.  This is an existence check rather than a true validation. It does not validate the property
        values against Naming Rules.
        """
        return cls.execute_soa_method(
            method_name='validateIdValue',
            library='Core',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ValidationResponse,
        )

    @classmethod
    def whereUsed(cls, input: List[WhereUsedInputData], configParams: WhereUsedConfigParameters) -> WhereUsedResponse:
        """
        The 'whereUsed' service identifies all the parent Item and ItemRevision objects in the structure where the
        input Item or ItemRevision is used. User can provide RevisionRule to search for specific ItemRevision . By
        default all ItemRevision objects are returned. The number of levels of 'whereUsed' search indicates, whether to
        return one or top or all levels of assemblies. It supports 'whereUsed' search on any WorkspaceObject which
        implements the "'whereUsed'" interface.
        
        Use cases:
        A user performs 'whereUsed' search to find all the assemblies that contain a particular Item or ItemRevision.
        User inputs Item or ItemRevision and the search can be made with following options:
        - RevisionRule  This can be set to All, displaying all ItemRevision objects  that have an occurrence of target
        ItemRevision. If a specific RevisionRule is selected only the ItemRevision objects  configured by the rule are
        returned in the search.
        - Depth up to which numbers of levels are to be returned.
        - Boolean representing whether to only send back precise parents (used by ItemRevision specifically and not
        Item)
        
        
        
        Additional Configuration Parameters can be used to do customized whereUsed search. 'WhereUsedConfigParameters'
        has below maps:
        
        stringMap ( std::string, std::string ) 
        doubleMap ( std::string, double ) 
        intMap ( std::string, int ) 
        boolMap ( std::string, bool ) 
        dateMap ( std::string, Teamcenter::DateTime ) 
        tagMap ( std::string, BusinessObjectRef ( Teamcenter::BusinessObject ) ) 
        floatMap ( std::string, float ) 
        
        COTS whereUsed search uses 'tagMap' to specify the RevisionRule with revision_rule as a key, 'boolMap' to
        specify whereUsedPreciseFlag with whereUsedPreciseFlag as a key, and 'intMap' to specify number of levels with
        numLevels as a key. Similarly other maps can be used to pass additional parameters for customized whereUsed
        search. Teamcenter currently don't have any extension where additional Configuration Parameters can be
        considered for 'whereUsed' search if passed by user. User can implement "whereUsed" interface on any custom
        WorkspaceObject to consider additional Configuration Parameters for 'whereUsed' search.
        
        The output contains list of  each parent level search result in the structure.
        """
        return cls.execute_soa_method(
            method_name='whereUsed',
            library='Core',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input, 'configParams': configParams},
            response_cls=WhereUsedResponse,
        )

    @classmethod
    def bulkCreateObjects(cls, input: List[BulkCreIn]) -> CreateResponse:
        """
        This is a generic operation for bulk creation of Business Objects. This will create instances of the given
        quantity of the specified type in their specified containing folders. This will also create any
        secondary(compounded) objects that need to be created, assuming the CreateInput for the secondary object is
        represented in the recursive CreateInput object e.g. Item is Primary Object that also creates Item Master,
        ItemRevision and ItemRevision in turn creates ItemRevision Master. The input for all these levels is passed in
        through the recursive CreateInput object. This operation is applicable for bulk creation of Item, Form ,Dataset
        and Asp0Aspect Types only.
        
        Use cases:
        1. To create large number of objects of specified types namely Item, Dataset and Form each of specified
        quantities and save them through a single transaction to significantly reduce the number of sql queries
        incurred during object creation, thus improving object creation performance and making object creation scalable.
        2. To create large number of Asp0Aspect objects of specified types and save them through a single transaction
        to significantly reduce the number of sql queries incurred during object creation, thus improving object
        creation performance and making object creation scalable.
        """
        return cls.execute_soa_method(
            method_name='bulkCreateObjects',
            library='Core',
            service_date='2012_02',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateResponse,
        )


class OperationDescriptorService(TcService):

    @classmethod
    def getDeepCopyData(cls, deepCopyDataInput: List[DeepCopyDataInput]) -> GetDeepCopyDataResponse:
        """
        This operation returns information required to perform SaveAs on a Business Object instance.
        
        Use cases:
        Client constructs the SaveAs dialog for a Business Object using this operation. The information returned by
        this operation allows a client to construct the SaveAs dialogs and the DeepCopy panels for user input. Once the
        user input is received, client can make subsequent invocation to the 'DataManagement.saveAsObjects' operation
        to execute SaveAs on the object.
        """
        return cls.execute_soa_method(
            method_name='getDeepCopyData',
            library='Core',
            service_date='2012_02',
            service_name='OperationDescriptor',
            params={'deepCopyDataInput': deepCopyDataInput},
            response_cls=GetDeepCopyDataResponse,
        )
