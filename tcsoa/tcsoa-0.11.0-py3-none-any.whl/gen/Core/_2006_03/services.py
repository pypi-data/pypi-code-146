from __future__ import annotations

from tcsoa.gen.Core._2006_03.DataManagement import ItemRevPropertyMap, AttributeNameValueMap, CreateRelationsResponse, DatasetProperties, ReviseResponse, CreateFoldersResponse, CreateItemsResponse, ObjectOwner, CreateDatasetsResponse, GenerateItemIdsAndInitialRevisionIdsResponse, GenerateRevisionIdsProperties, GenerateRevisionIdsResponse, ItemProperties, GenerateItemIdsAndInitialRevisionIdsProperties, Relationship, CreateFolderInput
from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, GroupMember
from tcsoa.gen.Core._2006_03.FileManagement import CommitDatasetFileInfo, GetDatasetWriteTicketsResponse, FileTicketsResponse, GetDatasetWriteTicketsInputData
from tcsoa.gen.Core._2006_03.Session import PreferencesResponse, GetGroupMembershipResponse, PrefSetting, GetSessionGroupMemberResponse, LoginResponse, GetAvailableServicesResponse
from tcsoa.gen.Core._2006_03.Reservation import GetReservationHistoryResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getProperties(cls, objects: List[BusinessObject], attributes: List[str]) -> ServiceData:
        """
        This service operation is provided to get property values of instances outside of the current object property
        policy for a particular business object.  Net result of this operation includes the properties expressly
        defined in the input attributes as well as the properties defined in the current Object Property Policy.
        
        This operation takes care of following:
        - Since all relations are stored as properties on the primary object, this operation supports the expanding of
        relations.  
        - Properties in the input attribute argument that reference other objects  (relations) will have the properties
        for those referenced objects returned as defined by the Object Property Policy.
        
        
        Limitation:
        - Classification objects attached to WorkspaceObjects using "IMAN_classification" relation are not returned by
        this operation. User need to use findClassificationObjects operation from Classification service to retrieve
        properties of such objects. For more information about findClassificationObjects operation please refer
        classification service guide.
        
        """
        return cls.execute_soa_method(
            method_name='getProperties',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'objects': objects, 'attributes': attributes},
            response_cls=ServiceData,
        )

    @classmethod
    def revise(cls, input: ItemRevPropertyMap) -> ReviseResponse:
        """
        Revises a list of next Item Revisions based on input existing Item Revision object references and any
        additional attributes.  Uses deep copy rules to propagate existing relations from the Item Revision or to
        create new references.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='revise',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ReviseResponse,
        )

    @classmethod
    def setDisplayProperties(cls, objects: List[BusinessObject], attributes: AttributeNameValueMap) -> ServiceData:
        """
        This operation is provided to update the Teamcenter objects for the given name/display value pairs. This
        operation works for all supported property value types to set display values. When setting this operation it
        invokes the server PROP_UIF_set_value extensions. For updating an array property, display values need to be
        comma (,) separated which server parses them into individual values before assigning.
        Note:  Since LOVs support the display as feature where internal values of the LOV can be different from
        displayable values, this operation expects that internal value of the selection to be passed and not the
        display value.
        """
        return cls.execute_soa_method(
            method_name='setDisplayProperties',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'objects': objects, 'attributes': attributes},
            response_cls=ServiceData,
        )

    @classmethod
    def createDatasets(cls, input: List[DatasetProperties]) -> CreateDatasetsResponse:
        """
        This operation creates a list of Datasets and creates the specified relation between created Dataset and input
        container object.
        """
        return cls.execute_soa_method(
            method_name='createDatasets',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateDatasetsResponse,
        )

    @classmethod
    def createFolders(cls, folders: List[CreateFolderInput], container: BusinessObject, relationType: str) -> CreateFoldersResponse:
        """
        This operation creates a list of new Folder objects with the given names, descriptions and attaches them to the
        parent container. If attaching a created Folder to its parent container fails, the Folder will not be deleted.
        """
        return cls.execute_soa_method(
            method_name='createFolders',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'folders': folders, 'container': container, 'relationType': relationType},
            response_cls=CreateFoldersResponse,
        )

    @classmethod
    def createItems(cls, properties: List[ItemProperties], container: BusinessObject, relationType: str) -> CreateItemsResponse:
        """
        This operation creates a list of Items and associated data (ItemRevision/ItemMasterForm/ItemRevisionMasterForm)
        based on the input attribute structures and the specified relation type between created Item and input object. 
        If container and relation type are not input, none of the Items will be related to a container. (There is no
        default, if any destination is desired, it must be provided as input). Note: createItems are for items
        creation, if a compound object such as ItemRevision adds a required property in BMIDE, createItems will fail
        since it only accepts required properties for item types, not for its associated data such as ItemRevision.
        Also, if any other properties including object description and custom properties are added as required on Item,
        createItems will fail. In this case, user should use 'createObjects' instead.
        """
        return cls.execute_soa_method(
            method_name='createItems',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'properties': properties, 'container': container, 'relationType': relationType},
            response_cls=CreateItemsResponse,
        )

    @classmethod
    def createRelations(cls, input: List[Relationship]) -> CreateRelationsResponse:
        """
        Creates the specified relation between the input objects (primary and secondary objects). If the relation name
        is not specified then default relation name specified in either the preference
        ParentTypeName_ChildTypeName_default_relation or ParentTypeName_default_relation is considered as the relation
        name. In case none of these preferences are set the relation between the primary and secondary object is not
        created. If the primary object has a relation property by the specified relation name, then the secondary
        object is associated with the primary object through the relation property.
        """
        return cls.execute_soa_method(
            method_name='createRelations',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateRelationsResponse,
        )

    @classmethod
    def deleteObjects(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation deletes the input objects.  In the case of Item, it also deletes all ItemRevision objects, 
        associated ItemMaster, ItemRevisionMaster forms, and Dataset objects.  The input object can be an ImanRelation.
        """
        return cls.execute_soa_method(
            method_name='deleteObjects',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteRelations(cls, input: List[Relationship]) -> ServiceData:
        """
        Deletes the specified relation between the primary and secondary object for each input structure.
        """
        return cls.execute_soa_method(
            method_name='deleteRelations',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def generateItemIdsAndInitialRevisionIds(cls, input: List[GenerateItemIdsAndInitialRevisionIdsProperties]) -> GenerateItemIdsAndInitialRevisionIdsResponse:
        """
        This operation generates a list of Item IDs and initial ItemRevision IDs.  The initial revision ID is defined
        as the first revision ID for the given type.
        """
        return cls.execute_soa_method(
            method_name='generateItemIdsAndInitialRevisionIds',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GenerateItemIdsAndInitialRevisionIdsResponse,
        )

    @classmethod
    def generateRevisionIds(cls, input: List[GenerateRevisionIdsProperties]) -> GenerateRevisionIdsResponse:
        """
        This operation generates a set of revision IDs.  The ID can be either the next ID for an existing Item or the
        first revision ID for a new Item.
        """
        return cls.execute_soa_method(
            method_name='generateRevisionIds',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GenerateRevisionIdsResponse,
        )

    @classmethod
    def changeOwnership(cls, input: List[ObjectOwner]) -> ServiceData:
        """
        This operation can be used to change the ownership on a given business object to the given user and group. 
        Owning user attribute on the business object will be changed to the given user and owning group attribute is
        changed to the given group.  The user needs CHANGE_OWNER privilege and WRITE privilege on the business object
        to be able to change its ownership.  If user does not have the required privileges then this operation will
        return error code 515001. If the given user is invalid or given group is invalid then this operation will
        return error code 515024.
        
        Use cases:
        Change owner menu action calls this operation.
        """
        return cls.execute_soa_method(
            method_name='changeOwnership',
            library='Core',
            service_date='2006_03',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )


class ReservationService(TcService):

    @classmethod
    def getReservationHistory(cls, objects: List[BusinessObject]) -> GetReservationHistoryResponse:
        """
        This operation gets the reservation history for a set of business objects, such as Dataset, Item, ItemRevision
        and many other business object types.  An object which has never been checked out will have a valid reservation
        history with an empty sequence of events.
        """
        return cls.execute_soa_method(
            method_name='getReservationHistory',
            library='Core',
            service_date='2006_03',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=GetReservationHistoryResponse,
        )

    @classmethod
    def checkin(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation checks-in a set of previously checked-out business objects. This operation takes care of all
        complex business logic involved to check-in passed in business objects.  Each input object is verified that it
        is locally owned, site owned, and not transferred to another user after the checkout was performed. This
        operation validates precondition defined per type in COTS object and site customization and performs basic
        check-in. Dataset, ItemRevision and many other business object types have their own business logic for
        check-in. This operation calls underlying 'checkin' method of those individual objects.
        """
        return cls.execute_soa_method(
            method_name='checkin',
            library='Core',
            service_date='2006_03',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )

    @classmethod
    def checkout(cls, objects: List[BusinessObject], comment: str, changeId: str) -> ServiceData:
        """
        This operation checks  out a set of business objects with given comment and change identifier. Only one user
        can perform a check-out transaction on the object. The user must have sufficient  privilege on the object or
        the check out will fail. This operation allows for remote check-out and records the check-out transaction event.
        """
        return cls.execute_soa_method(
            method_name='checkout',
            library='Core',
            service_date='2006_03',
            service_name='Reservation',
            params={'objects': objects, 'comment': comment, 'changeId': changeId},
            response_cls=ServiceData,
        )

    @classmethod
    def cancelCheckout(cls, objects: List[BusinessObject]) -> ServiceData:
        """
        This operation cancels a check-out for a set of previously checked-out business objects. The objects will be
        restored to the pre-check-out state. Only one user can perform a cancel check-out transaction on the object if
        the user has enough privilege on the object.  This action may be applied to remote checked out objects, and
        will cancel the check-out and records the cancel check-out transaction event. Cancel checkout is not supported
        for some of the business objects for e.g. - Item, BOMView,BOMViewRevision, Schedule.
        """
        return cls.execute_soa_method(
            method_name='cancelCheckout',
            library='Core',
            service_date='2006_03',
            service_name='Reservation',
            params={'objects': objects},
            response_cls=ServiceData,
        )


class SessionService(TcService):

    @classmethod
    def getSessionGroupMember(cls) -> GetSessionGroupMemberResponse:
        """
        Get the Group and Role for the current session. The group and role are set at login, either to default values
        or as specified by the input arguments to the login operation. The group and role can be changed at any time
        throughout the session through the 'setSessionGroupMember' or 'setUserSessionState' operations.
        """
        return cls.execute_soa_method(
            method_name='getSessionGroupMember',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={},
            response_cls=GetSessionGroupMemberResponse,
        )

    @classmethod
    def login(cls, username: str, password: str, group: str, role: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the user's credentials and initialize a Teamcenter session for this client. The operation will
        throw an 'InvalidCredentialsException' if the 'username', 'password' or 'group' is not valid.
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
        - 515143:    The logon was refused due to invalid 'username' or 'password'
        - 515144:    The logon was refused due to invalid 'username' or 'password'
        - 515142:    The logon was refused due to an invalid 'group'.
        
        """
        return cls.execute_soa_method(
            method_name='login',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={'username': username, 'password': password, 'group': group, 'role': role, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )

    @classmethod
    def loginSSO(cls, username: str, ssoCredentials: str, group: str, role: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the user using Single-Sign-On (SSO) credentials and initialize a Teamcenter session for this
        client. The 'username' and 'ssoCredentials' arguments must be obtained from Teamcenter's Security Services. The
        'SsoCredentials' class offers a simple API to get these values. The operation will throw an
        'InvalidCredentialsException' if the 'username', 'ssoCredentials' or group is not valid.
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
        Teamcenter 'server' instance. This is similar to the blank sessionDiscriminator argument; the difference is
        that only multiple instances of the client application using myApp started by jdoe share the same Teamcenter
        server instance.
        - Unique     If the user jdoe logs on using a unique random-generated string (for example, jdoe/akdk938lakc),
        the client application will be assigned to a dedicated instance of the Teamcenter server.
        
        
         
        The scenario you use depends on how your client application is used in the integrated environment. The most
        common case is the unique 'sessionDiscriminator' value.
        
        Exceptions:
        >When the credentials supplied are invalid or the requested locale is not allowed.  
        - 515143:    The logon was refused due to invalid 'username' or 'ssoCredentials'
        - 515144:    The logon was refused due to invalid 'username' or 'ssoCredentials'
        - 515142:    The logon was refused due to an invalid 'group'.
        
        """
        return cls.execute_soa_method(
            method_name='loginSSO',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={'username': username, 'ssoCredentials': ssoCredentials, 'group': group, 'role': role, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )

    @classmethod
    def logout(cls) -> ServiceData:
        """
        Logout and terminate the Teamcenter session. If the Teamcenter server is being shared with multiple client
        applications, it will not be terminated until each client has issued the 'logout'.
        """
        return cls.execute_soa_method(
            method_name='logout',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={},
            response_cls=ServiceData,
        )

    @classmethod
    def setPreferences(cls, settings: List[PrefSetting]) -> PreferencesResponse:
        """
        Set preference values
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='setPreferences',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={'settings': settings},
            response_cls=PreferencesResponse,
        )

    @classmethod
    def setSessionGroupMember(cls, groupMember: GroupMember) -> ServiceData:
        """
        Set the Group and Role for the current session. The group and role are set at login, either to default values
        or as specified by the input arguments to the login operation. The group and role can be changed at any time
        throughout the session through this operation or the 'setUserSessionState' operations. The
        'getSessionGroupMember' will return the current group and roll.
        """
        return cls.execute_soa_method(
            method_name='setSessionGroupMember',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={'groupMember': groupMember},
            response_cls=ServiceData,
        )

    @classmethod
    def getAvailableServices(cls) -> GetAvailableServicesResponse:
        """
        This operation returns a list of services and service operations that this Teamcenter server instance supports.
        This is useful for client applications that expose different functionality based on the version of the
        Teamcenter server it is connecting to.
        """
        return cls.execute_soa_method(
            method_name='getAvailableServices',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={},
            response_cls=GetAvailableServicesResponse,
        )

    @classmethod
    def getGroupMembership(cls) -> GetGroupMembershipResponse:
        """
        Get the valid groups and roles for the current user.
        """
        return cls.execute_soa_method(
            method_name='getGroupMembership',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={},
            response_cls=GetGroupMembershipResponse,
        )

    @classmethod
    def getPreferences(cls, prefScope: str, prefNames: List[str]) -> PreferencesResponse:
        """
        Get preference values
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='getPreferences',
            library='Core',
            service_date='2006_03',
            service_name='Session',
            params={'prefScope': prefScope, 'prefNames': prefNames},
            response_cls=PreferencesResponse,
        )


class FileManagementService(TcService):

    @classmethod
    def commitDatasetFiles(cls, commitInput: List[CommitDatasetFileInfo]) -> ServiceData:
        """
        This operation supports the upload (addition) of files to a Teamcenter volume.  The mechanism for a client
        application adding files to a Teamcenter volume contains several steps.  This mechanism is implemented in the
        'com.teamcenter.soa.client.FileManagementUtility' class, which provides this functionality to clients in a
        consistent, reusable package.    The 'com.teamcenter.soa.client.FileManagementUtility' class invokes this
        operation after successfully uploading a file to a Teamcenter volume.
        This operation was unintentionally published.  It is supported only for internal Siemens PLM purposes. 
        Customers should not invoke this operation.
        
        Use cases:
        This operation supports the upload (addition) of files representing named references of a Dataset object to a
        Teamcenter volume.
        """
        return cls.execute_soa_method(
            method_name='commitDatasetFiles',
            library='Core',
            service_date='2006_03',
            service_name='FileManagement',
            params={'commitInput': commitInput},
            response_cls=ServiceData,
        )

    @classmethod
    def getDatasetWriteTickets(cls, inputs: List[GetDatasetWriteTicketsInputData]) -> GetDatasetWriteTicketsResponse:
        """
        This operation obtains File Management System (FMS) write tickets and file storage information for a set of
        supplied Dataset objects. The write tickets are used to transfer files from a local storage to Teamcenter
        volume, and the file storage information can be used to commit Dataset objects referencing those transferred
        files.
        The caller will provide a vector of 'GetDatasetWriteTicketsInputData' objects that contains one or more Dataset
        objects and information about each associated file (e.g., filename, text/binary flag, etc.).  Upon return, the
        'GetDatasetWriteTicketsResponse' object will contain FMS write tickets that can be used to upload the file to
        the Teamcenter volume, and Dataset information that can be used to commit the changes to the database by using
        the 'FileManagementService' 'commitDatasetFiles'() operation.
        This operation supports the upload (addition) of files representing named references of a Dataset object to a
        Teamcenter volume.
        This operation was unintentionally published.  It is supported only for internal Siemens PLM purposes. 
        Customers should not invoke this operation.
        
        Use cases:
        This operation supports the upload (addition) of files representing named references of a Dataset object to a
        Teamcenter volume.
        """
        return cls.execute_soa_method(
            method_name='getDatasetWriteTickets',
            library='Core',
            service_date='2006_03',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=GetDatasetWriteTicketsResponse,
        )

    @classmethod
    def getFileReadTickets(cls, files: List[ImanFile]) -> FileTicketsResponse:
        """
        This operation obtains File Management System (FMS) read tickets for a set of supplied
        ImanFile objects.  The supplied tickets are used to transfer files from a Teamcenter volume 
        to local storage.  The 'files' input parameter contains a list of the ImanFile objects to be read 
        from the Teamcenter volume and transferred to local storage.
        FMS requires tickets for all file transfers to and from Teamcenter volumes.  An FMS read ticket is 
        required to obtain a file from a Teamcenter volume, while an FMS write ticket is needed to place a file in the
        Teamcenter volume.  It is often times more expedient to request several tickets at one time, especially if it
        is known ahead of time that many files will need to be moved.  For this reason, the caller may supply multiple
        ImanFile objects, for which FMS tickets are desired, in the input vector.
        This operation was unintentionally published.  It is supported only for internal Siemens PLM purposes. 
        Customers should not invoke this operation.
        
        Use cases:
        This operation supports the download of data files represented by ImanFile objects from a Teamcenter volume
        into a local client environment.
        """
        return cls.execute_soa_method(
            method_name='getFileReadTickets',
            library='Core',
            service_date='2006_03',
            service_name='FileManagement',
            params={'files': files},
            response_cls=FileTicketsResponse,
        )
