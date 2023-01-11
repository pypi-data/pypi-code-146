from __future__ import annotations

from tcsoa.gen.Core._2011_06.PropDescriptor import AttachedPropDescsResponse
from tcsoa.gen.BusinessObjects import BusinessObject, Envelope
from tcsoa.gen.Core._2011_06.Session import Credentials, ClientCacheInfo, LoginResponse
from tcsoa.gen.Core._2011_06.LOV import LOVAttachmentsInput, LOVAttachmentsResponse
from typing import List
from tcsoa.gen.Core._2011_06.Reservation import OkToCheckoutResponse
from tcsoa.gen.Common import PolicyType
from tcsoa.gen.Core._2007_06.PropDescriptor import PropDescInfo
from tcsoa.gen.Core._2011_06.OperationDescriptor import SaveAsDescResponse
from tcsoa.gen.Core._2011_06.DataManagement import SaveAsIn, TraceabilityInfoInput, TraceabilityReportOutput, SaveAsObjectsResponse, ValidateRevIdsResponse, ValidateRevIdsInfo
from tcsoa.gen.Server import ServiceData, TypeSchema
from tcsoa.base import TcService


class OperationDescriptorService(TcService):

    @classmethod
    def getSaveAsDesc(cls, targetObjects: List[BusinessObject]) -> SaveAsDescResponse:
        """
        This operation returns information required to save a business object. The 'SaveAsDescriptor' includes the
        metadata information for the properties required when saving a business object, i.e., the property is
        mandatory, the property is visible, if value is to be copied from original object, etc.  The 'SaveAsDescriptor'
        also includes the 'DeepCopyData' which is a recursive data structure. The 'DeepCopyData' contains information
        about how the secondary objects (related and referenced objects) are to be copied (reference, copy as object,
        no copy).
        
        Use cases:
        Get SaveAsDescriptor for the SaveAs wizard
        Client constructs the SaveAs dialog for a Business Object using this operation. The information returned by
        this operation allows a client to construct the SaveAs dialogs and DeepCopy panels for user input. Once the
        user input is received, client can make subsequent invocation to the 'DataManagement.saveAsObjects' operation
        to execute SaveAs on the object.
        """
        return cls.execute_soa_method(
            method_name='getSaveAsDesc',
            library='Core',
            service_date='2011_06',
            service_name='OperationDescriptor',
            params={'targetObjects': targetObjects},
            response_cls=SaveAsDescResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def getTraceReport(cls, input: TraceabilityInfoInput) -> TraceabilityReportOutput:
        """
        This operation will generate a Trace Report on the objects selected by user.  User will get information about
        complying as well as defining objects which are connected to selected object using  FND_TraceLink or its
        subtype of GRM relation.
        
        Trace links can be between following objects:
        
                1.    Between occurrences of an ItemRevision
                2.    Between ItemRevisions
                3.    Between Items
                4.    Between any two WorkspaceObject.
        
        If indirect trace report flag is set to true during this operation, then user will get trace report for
        ItemRevision if selected object is Occurrence, and trace report for Items if selected objects is ItemRevision
        in addition to direct trace report for the selected object.
        
        
        Use cases:
        Suppose user created trace link between Requirement R1 as start point and R2 as end point and creates trace
        link from Requirement R3 as start and R1 as end point.
        When user runs traceability report on R1 requirement he will get R2 object as complying object and R3 will come
        as defining object.
        """
        return cls.execute_soa_method(
            method_name='getTraceReport',
            library='Core',
            service_date='2011_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=TraceabilityReportOutput,
        )

    @classmethod
    def saveAsObjects(cls, saveAsIn: List[SaveAsIn]) -> SaveAsObjectsResponse:
        """
        This operation is generic operation for saving of Business Objects. It will also save any secondary objects
        that also need to be saved based on deep copy rule information
        
        Use cases:
        Client constructs the SaveAs dialog for a Business Object using 'OperationDescriptor.getSaveAsDesc' operation. 
        The information returned by that operation allows client to construct the SaveAs dialogs and DeepCopy panels
        for user input. Once the user input is received, client can make subsequent invocation to this
        ('DataManagement.saveAsObjects') operation to execute SaveAs on the object.
        """
        return cls.execute_soa_method(
            method_name='saveAsObjects',
            library='Core',
            service_date='2011_06',
            service_name='DataManagement',
            params={'saveAsIn': saveAsIn},
            response_cls=SaveAsObjectsResponse,
        )

    @classmethod
    def validateRevIds(cls, inputs: List[ValidateRevIdsInfo]) -> ValidateRevIdsResponse:
        """
        Validates and/or modifies the Revision Id based on the naming rules/revision naming rules and user exit
        callbacks.
        
        Use cases:
        This operation is generally used to validate revision id before providing it as input for create, revise and
        save-as operations.
        """
        return cls.execute_soa_method(
            method_name='validateRevIds',
            library='Core',
            service_date='2011_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ValidateRevIdsResponse,
        )


class SessionService(TcService):

    @classmethod
    def getTypeDescriptions(cls, typeNames: List[str]) -> TypeSchema:
        """
        Get the Meta data for the named Business Model object types. This includes type and property descriptions and
        LOV information.
        """
        return cls.execute_soa_method(
            method_name='getTypeDescriptions',
            library='Core',
            service_date='2011_06',
            service_name='Session',
            params={'typeNames': typeNames},
            response_cls=TypeSchema,
        )

    @classmethod
    def login(cls, credentials: Credentials) -> LoginResponse:
        """
        Authenticates the user's credentials and initialize a Teamcenter session for this client. The operation will
        throw an 'InvalidCredentialsException' if the 'username', 'password' or 'group' is not valid.
        When the client application is deployed to a 4Tier environment (communication through HTTP or TCCS) the login
        operation also contributes to the assignment of a Teamcenter server instance to the client session. The
        Teamcenter architecture varies from other client server architectures in that there is a dedicated instance of
        the Teamcenter server per client application. However, there are use cases where it is desirable for a single
        user to have multiple desktop applications running and each sharing a single instance of a Teamcenter server.
        This is controlled through the following elements:
        - hostPath    From the Connection class constructor, this specifies  the address (URI) the Teamcenter server is
        hosted on.
        - username    From this login operation, this specifies the user's Teamcenter user name.
        - sessionDiscriminator    From this login operation, this identifies the client session.
        
        
        
        The 'hostPath' argument determines the server machine that the client connects to. Once there, the pool manager
        on that host uses the 'username' and 'sessionDiscriminator' arguments of the login request to determine which
        Teamcenter server instance to assign the client to. If the pool manager has an existing Teamcenter server
        instance with the 'username'/'sessionDiscriminator' key, the client is assigned to that existing instance of
        the Teamcenter server, and therefore sharing the server with another client; otherwise, a new instance of the
        Teamcenter server is used. There are a few general scenarios for the 'sessionDiscriminator' argument:
        
        - Blank     If the user jdoe logs on to Teamcenter using two or more client applications using a blank
        'sessionDiscriminator' argument (for example, jdoe/ ), all of those clients are assigned to the same Teamcenter
        server instance. These client applications can be running on the same or different client hosts.
        - Constant     If the user jdoe logs on to Teamcenter using two or more client applications using a constant or
        fixed 'sessionDiscriminator' argument (for example, jdoe/MyApp ), those clients are assigned to the same
        Teamcenter server instance. This is similar to the blank 'sessionDiscriminator' argument; the difference is
        that only multiple instances of the client application using myApp started by jdoe share the same Teamcenter
        server instance.
        - Unique     If the user jdoe logs on using a unique random-generated string (for example, jdoe/akdk938lakc),
        the client application will be assigned to a dedicated instance of the Teamcenter server.
        
        
         
        The scenario you use depends on how your client application is used in the integrated environment. The most
        common case is the unique 'sessionDiscriminator' value.
        
        Exceptions:
        >When the credentials supplied are invalid or the requested locale is not allowed.  
        - 515143:     The logon was refused due to invalid 'username' or 'password'.
        - 515144:     The logon was refused due to invalid 'username' or 'password'.
        - 515142:     The logon was refused due to an invalid 'group'.
        - 128001: The logon was refused due to conflict with the encoding of the database instance. 
        - 128002:    The logon was refused due to missing localization.
        
        """
        return cls.execute_soa_method(
            method_name='login',
            library='Core',
            service_date='2011_06',
            service_name='Session',
            params={'credentials': credentials},
            response_cls=LoginResponse,
        )

    @classmethod
    def loginSSO(cls, credentials: Credentials) -> LoginResponse:
        """
        Authenticates the user using Single-Sign-On (SSO) credentials and initialize a Teamcenter session for this
        client. The 'username' and 'password' arguments must be obtained from Teamcenter's Security Services. The
        'SsoCredentials' class offers a simple API to get these values. The operation will throw an
        'InvalidCredentialsException' if the 'user', 'password' or 'group' is not valid.
        When the client application is deployed to a 4Tier environment (communication through HTTP or TCCS) the login
        operation also contributes to the assignment of a Teamcenter server instance to the client session. The
        Teamcenter architecture varies from other client server architectures in that there is a dedicated instance of
        the Teamcenter server per client application. However, there are use cases where it is desirable for a single
        user to have multiple desktop applications running and each sharing a single instance of a Teamcenter server.
        This is controlled through the following elements:
        - 'hostPath'    From the Connection class constructor, this specifies  the address (URI) the Teamcenter server
        is hosted on.
        - 'username'    From this login operation, this specifies the user's Teamcenter user name.
        - 'sessionDiscriminator'    From this login operation, this identifies the client session.
        
        
        
        The 'hostPath' argument determines the server machine that the client connects to. Once there, the pool manager
        on that host uses the 'username' and 'sessionDiscriminator' arguments of the logon request to determine which
        Teamcenter server instance to assign the client to. If the pool manager has an existing Teamcenter server
        instance with the 'username'/'sessionDiscriminator' key, the client is assigned to that existing instance of
        the Teamcenter server, and therefore sharing the server with another client; otherwise, a new instance of the
        Teamcenter server is used. There are a few general scenarios for the sessionDiscriminator argument:
        
        - Blank     If the user jdoe logs on to Teamcenter using two or more client applications using a blank
        'sessionDiscriminator' argument (for example, jdoe/ ), all of those clients are assigned to the same Teamcenter
        server instance. These client applications can be running on the same or different client hosts.
        - Constant     If the user jdoe logs on to Teamcenter using two or more client applications using a constant or
        fixed 'sessionDiscriminator' argument (for example, jdoe/MyApp ), those clients are assigned to the same
        Teamcenter server instance. This is similar to the blank 'sessionDiscriminator' argument; the difference is
        that only multiple instances of the client application using myApp started by jdoe share the same Teamcenter
        server instance.
        - Unique     If the user jdoe logs on using a unique random-generated string (for example, jdoe/akdk938lakc),
        the client application will be assigned to a dedicated instance of the Teamcenter server.
        
        
         
        The scenario you use depends on how your client application is used in the integrated environment. The most
        common case is the unique 'sessionDiscriminator' value.
        
        Exceptions:
        >When the credentials supplied are invalid or the requested locale is not allowed.  
        - 515143:    The logon was refused due to invalid 'username' or 'password'
        - 515144:    The logon was refused due to invalid 'username' or 'password'
        - 515142:    The logon was refused due to an invalid 'group'.
        - 128001:     The logon was refused due to conflict with the encoding of the database instance. 
        - 128002:    The logon was refused due to missing localization.
        
        """
        return cls.execute_soa_method(
            method_name='loginSSO',
            library='Core',
            service_date='2011_06',
            service_name='Session',
            params={'credentials': credentials},
            response_cls=LoginResponse,
        )

    @classmethod
    def updateObjectPropertyPolicy(cls, policyID: str, addProperties: List[PolicyType], removeProperties: List[PolicyType]) -> str:
        """
        Update the named policy, adding and removing the named properties. This operation only applies to object
        property policies that have been defined on the client side.
        
        Exceptions:
        >If the named policy does not exist in the server's memory (error code 214106).
        """
        return cls.execute_soa_method(
            method_name='updateObjectPropertyPolicy',
            library='Core',
            service_date='2011_06',
            service_name='Session',
            params={'policyID': policyID, 'addProperties': addProperties, 'removeProperties': removeProperties},
            response_cls=str,
        )

    @classmethod
    def getClientCacheData(cls, features: List[str]) -> ClientCacheInfo:
        """
        This operation returns information required to maintain a client cache. The Teamcneter server maintains a set
        of Datasets with static or near static data that is pertainant to a client application.  This static data can
        be downloaded through FMS to the cleint host one time, and available for each subsequent client session, thus
        improving the overall performance of the client application. These Datasets are updated as part of the deploy
        process from the BMIDE. The cleint cache consits of serveral features, each of these features can be used
        independnatly of each other. The following features are available:
        
        - ClientMetaModel :The is the client side version of the server`s Meta Model. This includes type descriptions,
        property descriptions, List Of Values data, and Dataset tool data. The use of the ClientMetaModel cache
        replaces the need to use the getTypeDescriptions  service calls. By setting the
        'Connection.setOption(OPT_USE_CLIENT_META_MODEL_CACHE, true)', the SOA client framework will use the cache for
        Client  Meta Model data. The SOA client framework takes care of calling this service opeation and FMS to
        populate the cache. This feature includes the Dataset:Types, Lov, ToolsData, types_local (one for each locale
        i.e types_en_US), lov_local (one for each locale i.e lov_en_US).
        - TextData: This contains the localized string available in the Teamcenter server's Text Server. Using the
        localized data from this cache replaces the need to call the getDisplayStrings service operation.
        
        """
        return cls.execute_soa_method(
            method_name='getClientCacheData',
            library='Core',
            service_date='2011_06',
            service_name='Session',
            params={'features': features},
            response_cls=ClientCacheInfo,
        )


class ReservationService(TcService):

    @classmethod
    def okToCheckout(cls, objects: List[BusinessObject]) -> OkToCheckoutResponse:
        """
        This operation determines whether or not the input objects may be checked out given the type of object, access
        rules, and current checkout state of the object.
        """
        return cls.execute_soa_method(
            method_name='okToCheckout',
            library='Core',
            service_date='2011_06',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=OkToCheckoutResponse,
        )


class EnvelopeService(TcService):

    @classmethod
    def sendAndDeleteEnvelopes(cls, envelopes: List[Envelope]) -> ServiceData:
        """
        This operation sends mails to the recipients of each Envelope business object in envelopes. All the envelopes
        passed to this operation are deleted after they are processed, even if the processing is not successful. Each
        Envelope business object contains mail information such as subject, body, recipients, and attachments.
        Recipients can be Teamcenter users, groups and address lists, or, external email addresses. Teamcenter users
        receive envelopes in their Teamcenter Mailbox and also as emails if Mail_OSMail_activated site preference is
        set to 'true'.To send the emails, the site preference Mail_server_name should be properly configured. Any
        errors that occur while sending envelopes are returned as partial errors in ServiceData.
        
        Use cases:
        Use case 1: Send envelopes to Teamcenter users
        You can send envelopes to the Mailbox of Teamcenter users by specifying the users as recipients on Envelope
        business objects.  Also, email messages can be sent to Teamcenter users if Mail_OSMail_activated site
        preference is set to 'true'.
        
        User case 2: Send emails to external email addresses
        Email messages can be sent to external users by specifying their email addresses as recipients on Envelope
        business objects.
        """
        return cls.execute_soa_method(
            method_name='sendAndDeleteEnvelopes',
            library='Core',
            service_date='2011_06',
            service_name='Envelope',
            params={'envelopes': envelopes},
            response_cls=ServiceData,
        )


class PropDescriptorService(TcService):

    @classmethod
    def getAttachedPropDescs2(cls, inputs: List[PropDescInfo]) -> AttachedPropDescsResponse:
        """
        Returns a list of Property Descriptors based on the input structure.  The Property Descriptors contain the
        Display Name, Description and other information about the input property.
        
        Use cases:
        This operation provides following use case for retrieving a set of Property Descriptors given a type name and
        list of property names for that type.
        
        Use Case 1:Retrieve a set of Property Descriptors for a list of property names.
        - Create a new PropDescInfo input structure.
        - Populate the type name and input list of property names.
        - Call getAttachedPropDescs2 with the newly created input structure.
        
        
        
        Exceptions:
        >.
        """
        return cls.execute_soa_method(
            method_name='getAttachedPropDescs2',
            library='Core',
            service_date='2011_06',
            service_name='PropDescriptor',
            params={'inputs': inputs},
            response_cls=AttachedPropDescsResponse,
        )


class LOVService(TcService):

    @classmethod
    def getLOVAttachments(cls, objectStructArray: List[LOVAttachmentsInput]) -> LOVAttachmentsResponse:
        """
        Returns valid LOV attachments for the properties of each object passed in as input. It may return LOV or null
        based on condition validations. If none of the conditions evaluated to be True, then no LOV attachment is
        returned for the property of an instance.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='getLOVAttachments',
            library='Core',
            service_date='2011_06',
            service_name='LOV',
            params={'objectStructArray': objectStructArray},
            response_cls=LOVAttachmentsResponse,
        )
