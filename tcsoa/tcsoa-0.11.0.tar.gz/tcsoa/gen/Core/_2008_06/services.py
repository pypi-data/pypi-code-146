from __future__ import annotations

from tcsoa.gen.Core._2008_06.DataManagement import CreateOrUpdateGDELinksResponse, ConnectionProperties, BOWithExclusionIn, CreateOrUpdateRelationsInfo, AddParticipantOutput, DatasetProperties2, GDELinkInfo, ReviseInfo, CreateOrUpdateRelationsResponse, ReviseResponse2, NRAttachInfo, GetItemAndRelatedObjectsResponse, CreateIn, SaveAsNewItemResponse2, CreateResponse, TypeAndItemRevInfo, AddParticipantInfo, ItemElementProperties, GetNRPatternsWithCountersResponse, InfoForNextId, GetNextIdsResponse, GetRevNRAttachResponse, CreateConnectionsResponse, CreateOrUpdateItemElementsResponse, GetItemAndRelatedObjectsInfo, SaveAsNewItemInfo, DisplayableSubBOsResponse, Participants
from tcsoa.gen.BusinessObjects import BusinessObject, User
from tcsoa.gen.Core._2006_03.DataManagement import CreateDatasetsResponse
from tcsoa.gen.Core._2008_06.PropDescriptor import CreateDescResponse
from tcsoa.gen.Core._2008_06.DispatcherManagement import CreateDispatcherRequestResponse, CreateDispatcherRequestArgs
from tcsoa.gen.Core._2008_06.StructureManagement import GetPrimariesOfInStructureAssociationResponse, GetSecondariesOfInStructureAssociationResponse, GetPrimariesOfInStructureAssociationInfo, CreateInStructureAssociationResponse, GetSecondariesOfInStructureAssociationInfo, InStructureAssociationInfo, RemoveInStructureAssociationsInfo, RemoveInStructureAssociationsResponse
from tcsoa.gen.Core._2008_06.Session import GetDisplayStringsResponse
from tcsoa.gen.Core._2008_06.ManagedRelations import GetManagedRelationResponse, GetManagedRelationInput
from typing import List
from tcsoa.gen.Core._2006_03.Session import LoginResponse
from tcsoa.gen.Common import ObjectPropertyPolicy
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getRevNRAttachDetails(cls, typeAndItemRevInfos: List[TypeAndItemRevInfo]) -> GetRevNRAttachResponse:
        """
        This operation gets all the possible initial, secondary and supplemental revision next Ids for an ItemRevision
        along with the available formats and the set of excluded letters for revision. The Revision Type Name and the
        current revision are passed in the input typeAndItemRevInfos structure. The input for this operation contains a
        list of this structure. The return structure contains list of Initial Revision details, Secondary Revision
        details, Supplemental Revision details and exclude Skip letters along with the service data member.
        
        Use cases:
        This operation is used to get the next available options for revision id for a new or existing object. User can
        select one of the values returned by this operation and use as revision id input value for create, revise or
        save-as operation.
        """
        return cls.execute_soa_method(
            method_name='getRevNRAttachDetails',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'typeAndItemRevInfos': typeAndItemRevInfos},
            response_cls=GetRevNRAttachResponse,
        )

    @classmethod
    def removeParticipants(cls, participants: List[Participants]) -> ServiceData:
        """
        This operation allows the user to remove Participant objects associated with specified Item Revision. If a
        participant being removed is no longer associated with any other objects, it gets deleted.
        
        Use cases:
        This operation can be used to remove the assigned Participant objects like Analyst, Proposed Reviewers etc.
        from the change objects. Change creator can use 'addParticipants' service operation to assign an analyst or use
        this operation to remove an assigned analyst.
        """
        return cls.execute_soa_method(
            method_name='removeParticipants',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'participants': participants},
            response_cls=ServiceData,
        )

    @classmethod
    def revise2(cls, info: List[ReviseInfo]) -> ReviseResponse2:
        """
        This operation provides the ability to revise the ItemRevision objects given in the input list and carries
        forward relations to existing objects. When applying deep copy rules, if user overridden deep copy information
        is provided in the input, relations are propagated to the new ItemRevision based on that input. If no deep copy
        information is provided in the input, the deep copy rules in the database are used to propagate relations to
        the new ItemRevision.  If the input contains property values for the master form, those values are set on the
        new ItemRevision master form.
        """
        return cls.execute_soa_method(
            method_name='revise2',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ReviseResponse2,
        )

    @classmethod
    def saveAsNewItem2(cls, info: List[SaveAsNewItemInfo]) -> SaveAsNewItemResponse2:
        """
        This operation provides the capability to create one or more new Item objects based on a list of existing
        ItemRevision objects. It optionally carries forward ItemRevision relations based on the 'deepCopyRequired'
        flag. When applying deep copy rules, if user overridden deep copy information is provided in the input, then
        old ItemRevision relations are propagated to the new ItemRevision based on the input. If no deep copy rule
        information is provided in the input, the deep rules in the database will be applied. If user provides new
        property values for the Item and ItemRevision master forms in the input, then these will be copied to the
        master forms of the newly created Item and ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='saveAsNewItem2',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'info': info},
            response_cls=SaveAsNewItemResponse2,
        )

    @classmethod
    def createConnections(cls, properties: List[ConnectionProperties], container: BusinessObject, relationType: str) -> CreateConnectionsResponse:
        """
        Creates a list of Connection objects and any associated data (ConnectionRevision, ConnectionMaster Form and
        ConnectionRevision Master Form) based on the input properties structure. It also creates the specified relation
        type between newly created Connection object and input container object. If container and relation type are not
        supplied, none of the Connection objects will be related to a container. If any destination to paste the newly
        created objects is desired then it must be supplied as input.
        
        Use cases:
        This operation supports creation of single or multiple Connection objects.
        """
        return cls.execute_soa_method(
            method_name='createConnections',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'properties': properties, 'container': container, 'relationType': relationType},
            response_cls=CreateConnectionsResponse,
        )

    @classmethod
    def createDatasets2(cls, input: List[DatasetProperties2]) -> CreateDatasetsResponse:
        """
        This operation creates a list of Dataset objects and creates the specified relation type between created
        Dataset and input container object.
        """
        return cls.execute_soa_method(
            method_name='createDatasets2',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateDatasetsResponse,
        )

    @classmethod
    def createObjects(cls, input: List[CreateIn]) -> CreateResponse:
        """
        Generic operation for creation of Business Objects. This will also create any secondary(compounded) objects
        that need to be created, assuming the CreateInput for the secondary object is represented in the recursive
        CreateInput object e.g. Item is Primary Object that also creates Item Master and ItemRevision. ItemRevision in
        turn creates ItemRevision Master. The input for all these levels is passed in through the recursive CreateInput
        object.
        
        Use cases:
        This operation to create an object is invoked after obtaining user input on the fields of the create dialog.
        This call is typically preceded by a call to Teamcenter::Soa::Core::_2008_06::PropDescriptor::getCreateDesc or
        to the SOA Client Metamodel layer to retrieve Create Descriptor for a Business Object. 
        
        For example, to create an Item, client will get the Create Descriptor associated with the Item from the client
        metamodel (The associated descriptor type can be found by looking at the constant value for the CreateInput
        constant that is attached to Item). Alternatively, for clients that do not use the SOA client metamodel, the
        Descriptor for Item can be obtained by invoking getCreateDesc operation. The descriptor information can then be
        used to populate the Create dialog for the Business Object. Once the Create dialog is populated the
        createObjects operation can be called to create the object.
        """
        return cls.execute_soa_method(
            method_name='createObjects',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateResponse,
        )

    @classmethod
    def createOrUpdateGDELinks(cls, gdeLinkInfos: List[GDELinkInfo]) -> CreateOrUpdateGDELinksResponse:
        """
        Create and/or update GeneralDesignElementLink(GDELink) objects based on the input properties structure. If the
        given GDELink object exists in Teamcenter then the operation will be treated as an update based on the input
        properties structure
        
        Use cases:
        This operation supports creation or updation of GDELink objects
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateGDELinks',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'gdeLinkInfos': gdeLinkInfos},
            response_cls=CreateOrUpdateGDELinksResponse,
        )

    @classmethod
    def createOrUpdateItemElements(cls, properties: List[ItemElementProperties]) -> CreateOrUpdateItemElementsResponse:
        """
        Allows the user to create a new GeneralDesignElement (GDE) or its subtype and set its properties. In the case
        of existing GDE, user can update the properties.
        
        Use cases:
        This operation can be used when user wants to create a GDE in a product structure or wants to update the
        properties of an existing GDE. User has to pass unique client Id, name and type when a new element has to be
        created. Whenever properties of an existing GDE have to be updated the itemElement business object and
        itemElemAttributes should be passed
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateItemElements',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'properties': properties},
            response_cls=CreateOrUpdateItemElementsResponse,
        )

    @classmethod
    def createOrUpdateRelations(cls, infos: List[CreateOrUpdateRelationsInfo], sync: bool) -> CreateOrUpdateRelationsResponse:
        """
        Creates the specified relation between the input objects (primary and secondary objects) for each input
        structure. If the 'sync' flag is specified, then if any Generic Relationship Management (GRM) relations exist
        between the primary and secondary objects and they are not specified in the input they will be deleted. If
        'sync' flag is provided, the relations member of 'CreateOrUpdateRelationsInfo' is ignored.
        
        Use cases:
        Use Case 1: Create a relation based on the GRM rule definition.
        
        One can create a relation specified by name of the relation in the input structure between the primary and
        secondary object, when there exists a GRM rule between the primary and secondary object with the given relation
        type.
        
        Use Case 2: Update a relation based on the GRM rule definition.
        
        One can update a relation specified by name of the relation in the input structure between the primary and
        secondary object, when there exists a GRM rule between the primary and secondary object with the given relation
        type.
        
        Use Case 3: Remove a relation based on the GRM rule definition.
        
        One can remove a relation by setting the sync to true and do not provide any relation between the primary and
        secondary object in the input structure. When there exists a GRM rule between the primary and secondary object
        with the given relation type, and the sync flag is set to true, then if any GRM relations exist between the
        primary and secondary objects and they are not specified in the input they will be deleted.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRelations',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'infos': infos, 'sync': sync},
            response_cls=CreateOrUpdateRelationsResponse,
        )

    @classmethod
    def addParticipants(cls, addParticipantInfo: List[AddParticipantInfo]) -> AddParticipantOutput:
        """
        This operation creates the Participant objects and adds them to the input Item Revision. If a Participant
        object with specified attributes already exists, it is added to the Item Revision.
        
        Use cases:
        For Change Management use cases, user may need to add different participants to the change objects like
        analyst, change specialist etc. The creator of the change object will assign the analyst for the change where
        this operation can be used.
        """
        return cls.execute_soa_method(
            method_name='addParticipants',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'addParticipantInfo': addParticipantInfo},
            response_cls=AddParticipantOutput,
        )

    @classmethod
    def findDisplayableSubBusinessObjects(cls, input: List[BOWithExclusionIn]) -> DisplayableSubBOsResponse:
        """
        Operation to retrieve sub Business Object Names for a Business Object that are displayable to the login user in
        the object creation dialog. e.g File-new, select Item, what types to be displayed for Item
        """
        return cls.execute_soa_method(
            method_name='findDisplayableSubBusinessObjects',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=DisplayableSubBOsResponse,
        )

    @classmethod
    def getItemAndRelatedObjects(cls, infos: List[GetItemAndRelatedObjectsInfo]) -> GetItemAndRelatedObjectsResponse:
        """
        This operation returns Items, ItemRevisions, Dataset and NamedReference information based on the input. Input
        is a list of 'GetItemAndRelatedObjectsInfo' structures each of which contains item uid or id, revison
        information and optionally a list of filters to determine the datasets to be returned. For the Datasets the
        client can request information about the NamedReferences. NamedReferences are how Data files are attached to
        Datasets. The Data file is what a CAD client is really interested in. The return is a
        'GetItemAndRelatedObjectsResponse' which contains a list of 'GetItemAndRelatedObjectsItemOutput' and a
        'ServiceData'.
        
        Use cases:
        The client has an item of ItemRevision and needs to know what CAD data is attached to the ItemRevision. The
        client fills in either the Item or ItemRevision information along with the information about the types of
        Dataset and NamedReferences the client is interested in. For the NamedReferences the user can get the tickets
        which will allow the client retrieve the files attached to the Datasets. The results of the query will give the
        client all the information about the Datasets and NamedReferences and optional tickets.
        """
        return cls.execute_soa_method(
            method_name='getItemAndRelatedObjects',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'infos': infos},
            response_cls=GetItemAndRelatedObjectsResponse,
        )

    @classmethod
    def getNRPatternsWithCounters(cls, vAttachInfo: List[NRAttachInfo]) -> GetNRPatternsWithCountersResponse:
        """
        This operation gives the list of Patterns which has counters along with preferred patterns and conditions for
        the Naming Rule attached to the property of an object Type. The Type name and the Property name are passed in
        the input structure. The input for this operation contains a list of this structure. The return structure
        contains the vector of patterns with counters, preferredPattern and condition, along with the service data
        member.
        
        Use cases:
        This operation is used in create, revise or save-as dialogs to receive list of applicable patterns for item and
        revision ids. The list of patterns returned is displayed in these dialogs for user selection. After user
        selects a pattern and clicks "Assign" button, an id is generated matching the pattern selected and populated in
        the corresponding field's box.
        """
        return cls.execute_soa_method(
            method_name='getNRPatternsWithCounters',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'vAttachInfo': vAttachInfo},
            response_cls=GetNRPatternsWithCountersResponse,
        )

    @classmethod
    def getNextIds(cls, vInfoForNextId: List[InfoForNextId]) -> GetNextIdsResponse:
        """
        The operation generates the next id as per the input pattern in the attached Naming Rule to the property of an
        object type. The type name, property name and pattern are passed in the input structure. The input for this
        operation contains a  list of this structure. The return structure contains the list of nextId along with the
        service data member. In the case where no pattern is specified, a default ID will be returned if the type,
        property combination is Item / item_id, Dataset / pubr_object_id or ItemRevision/item_revision_id. For all
        other type, property combinations, the operation will not generate a default ID.
        
        Use cases:
        This operation is called on click of "Assign" button in create, revise and save-as dialogs to generate the next
        available options for item and revision ids. The generated values are used as input for create, revise and
        save-as operations.
        """
        return cls.execute_soa_method(
            method_name='getNextIds',
            library='Core',
            service_date='2008_06',
            service_name='DataManagement',
            params={'vInfoForNextId': vInfoForNextId},
            response_cls=GetNextIdsResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def getSecondariesOfInStructureAssociation(cls, inputs: List[GetSecondariesOfInStructureAssociationInfo]) -> GetSecondariesOfInStructureAssociationResponse:
        """
        Given the primary object and association type, returns the secondary BOMLine business objects of in structure
        associations. These associations can be ConnectTo, ImplementedBy, RealizedBy, RoutedBy, FixingToSegment,
        DeviceToConnector, SignalToSource, SignalToTarget, SignalToTransmitter, ProcessVariable or RedundantSignal. It
        takes a vector of GetSecondariesOfInStructureAssociationInfo as input.
        
        Use cases:
        Users shall use this operation to get secondary BOMLine business objects for a given association type and the
        primary object associated with it. 
        For instance, this operation could be used to get all the secondary GDE lines connected to a PSConnection by
        passing the association type as ConnectTo. Similarly, it can be used to get the connector lines connected to
        the Device Line by passing appropriate primary Device and the association type as DeviceToConnector.
        """
        return cls.execute_soa_method(
            method_name='getSecondariesOfInStructureAssociation',
            library='Core',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=GetSecondariesOfInStructureAssociationResponse,
        )

    @classmethod
    def removeInStructureAssociations(cls, inputs: List[RemoveInStructureAssociationsInfo]) -> RemoveInStructureAssociationsResponse:
        """
        Given the primary BOMLine, the association type, and the secondary BOMLines this operation removes the
        instructure associations between the BOMLines. These associations can be ConnectTo, ImplementedBy, RealizedBy,
        RoutedBy, FixingToSegment, DeviceToConnector, SignalToSource, SignalToTarget, SignalToTransmitter,
        ProcessVariable or RedundantSignal. The operation takes a vector of RemoveInStructureAssociationsInfo as Input.
        If input primary is Signal object's BOMLine, then for associatiion type input between signal and secondary as
        source or target can be optional, and if input association type is empty, then the secondary BOMLine
        association to input primary Signal BOMLine  as source and target will be removed.
        
        Use cases:
        Developers shall use this operation when an association has to be removed between the BOMLines. This is a
        generic Teamcenter service to remove various types of associations. 
        In the case of ConnectTo, if the secondary BOMLines are passed as null then all the secondary associations with
        the primary BOMLine shall be removed.
        """
        return cls.execute_soa_method(
            method_name='removeInStructureAssociations',
            library='Core',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=RemoveInStructureAssociationsResponse,
        )

    @classmethod
    def createInStructureAssociations(cls, inputs: List[InStructureAssociationInfo]) -> CreateInStructureAssociationResponse:
        """
        This operation creates the specified association between primary and secondary BOMLine objects in a structure. 
        As the name indicates, these associations are created in a specific context and are applicable only in that
        context. The context is specified as an additional input in the input structure, by the caller. Some examples
        of these associations are: the ConnectTo, ImplementedBy, RealizedBy, SignalToSource, SignalToTarget,
        SignalToTransmitter, ProcessVariable, RedundantSignal relations that are provided in Teamcenter [see Use case].
        This operation takes a vector of InStructureAssociationInfo as input. The input structures contain information
        on the BOMLine objects that need to be associated, what context they need to be associated in and the type of
        association. Note that the associations created are only valid in the context specified.
        If input primary is Signal object's BOMLine, then for associating signal BOMLine to secondary as source or
        target, the association type is optional, and if input association type is empty, the secondary BOMLine objects
        GDE object direction attirbute value will be used for associating signal BOMLine to secondary as source or
        target.
        
        Use cases:
        Use this operation to create an association between BOMLine objects. This is a generic Teamcenter service to
        create various types of associations. The type of the association that gets created depends on the Association
        Type specified in the input structure. 
        The ConnectTo  functionality establishes an association between 1 or more BOMLine objects and a Connection
        BOMLine. The association signifies that the BOMLine objects are connected to the Connection BOMLine in a
        certain context.  Outside of that context the association is not valid. The caller of this operation provides
        as input, one or more BOMLine objects, and a Connection BOMLine. The associationType should be set in the input
        structure to ConnectTo and specifies a BOMLine that will act as a context line within which the association is
        valid.
        """
        return cls.execute_soa_method(
            method_name='createInStructureAssociations',
            library='Core',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=CreateInStructureAssociationResponse,
        )

    @classmethod
    def getPrimariesOfInStructureAssociation(cls, inputs: List[GetPrimariesOfInStructureAssociationInfo]) -> GetPrimariesOfInStructureAssociationResponse:
        """
        This operation gets the primary BOMLines like PSConnection, Signal of an association given the secondary object
        and association type.  Examples of these associations are: ConnectTo, ImplementedBy, RealizedBy, RoutedBy,
        FixingToSegment, DeviceToConnector, SignalToTransmitter, SignalToSource, SignalToTarget, ProcessVariable,
        RedundantSignal. This operation takes a vector of GetPrimariesOfInStructureAssociationInfo as input.
        
        Use cases:
        A typical usecase for this operation is where callers would like to obtain primary BOMLine objects by providing
        the association type and the corresponding secondary BOMLine associated.  In a SignalToTransmitter association
        for example, if the transmitting BOMLine  is provided, callers can get the corresponding Signal which is the
        primary BOMLine in this relation.
        """
        return cls.execute_soa_method(
            method_name='getPrimariesOfInStructureAssociation',
            library='Core',
            service_date='2008_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=GetPrimariesOfInStructureAssociationResponse,
        )


class SessionService(TcService):

    @classmethod
    def login(cls, username: str, password: str, group: str, role: str, locale: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the user`s credentials and initialize a Teamcenter session for this client. The operation will
        throw an 'InvalidCredentialsException' if the 'username', 'password' or 'group' is not valid.
        When the client application is deployed to a 4Tier environment (communication through HTTP or TCCS) the 'login'
        operation also contributes to the assignment of a Teamcenter server instance to the client session. The
        Teamcenter architecture varies from other client server architectures in that there is a dedicated instance of
        the Teamcenter server per client application. However, there are use cases where it is desirable for a single
        user to have multiple desktop applications running and each sharing a single instance of a Teamcenter server.
        This is controlled through the following elements:
        - 'hostPath'    From the Connection class constructor, this specifies  the address (URI) the Teamcenter server
        is hosted on.
        - 'username'    From this login operation, this specifies the user`s Teamcenter user name.
        - 'sessionDiscriminator'    From this login operation, this identifies the client session.
        
        
        
        The 'hostPath' argument determines the server machine that the client connects to. Once there, the pool manager
        on that host uses the 'username' and 'sessionDiscriminator' arguments of the 'logon' request to determine which
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
        - Unique     If the user jdoe logs on using a unique random generated string (for example, jdoe/akdk938lakc),
        the client application will be assigned to a dedicated instance of the Teamcenter server.
        
        
         
        The scenario you use depends on how your client application is used in the integrated environment. The most
        common case is the unique 'sessionDiscriminator' value.
        
        Exceptions:
        >When the credentials supplied are invalid or the requested locale is not allowed.  
        - 515143:    The logon was refused due to invalid 'username' or 'password'
        - 515144:    The logon was refused due to invalid 'username' or 'password'
        - 515142:    The logon was refused due to an invalid 'group'.
        - 128001: The logon was refused due to conflict with the encoding of the database instance. 
        - 128002:    The logon was refused due to missing localization.
        
        """
        return cls.execute_soa_method(
            method_name='login',
            library='Core',
            service_date='2008_06',
            service_name='Session',
            params={'username': username, 'password': password, 'group': group, 'role': role, 'locale': locale, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )

    @classmethod
    def loginSSO(cls, username: str, ssoCredentials: str, group: str, role: str, locale: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the user using Single-Sign-On (SSO) credentials and initialize a Teamcenter session for this
        client. The 'username' and 'ssoCredentials' arguments must be obtained from Teamcenter's Security Services. The
        'SsoCredentials' class offers a simple API to get these values. The operation will throw an
        'InvalidCredentialsException' if the 'username', 'ssoCredentials' or 'group' is not valid.
        When the client application is deployed to a 4Tier environment (communication through HTTP or TCCS) the login
        operation also contributes to the assignment of a Teamcenter server instance to the client session. The
        Teamcenter architecture varies from other client server architectures in that there is a dedicated instance of
        the Teamcenter server per client application. However, there are use cases where it is desirable for a single
        user to have multiple desktop applications running and each sharing a single instance of a Teamcenter server.
        This is controlled through the following elements:
        'hostPath'    From the Connection class constructor, this specifies  the address (URI) the Teamcenter server is
        hosted on.
        'username'    From this login operation, this specifies the user's Teamcenter user name.
        'sessionDiscriminator'    From this login operation, this identifies the client session.
        
        The 'hostPath' argument determines the server machine that the client connects to. Once there, the pool manager
        on that host uses the 'username' and 'sessionDiscriminator' arguments of the login request to determine which
        Teamcenter server instance to assign the client to. If the pool manager has an existing Teamcenter server
        instance with the 'username'/'sessionDiscriminator' key, the client is assigned to that existing instance of
        the Teamcenter server, and therefore sharing the server with another client; otherwise, a new instance of the
        Teamcenter server is used. There are a few general scenarios for the 'sessionDiscriminator' argument:
        
        - Blank     If the user jdoe logs on to Teamcenter using two or more client applications using a blank
        sessionDiscriminator argument (for example, jdoe/ ), all of those clients are assigned to the same Teamcenter
        server instance. These client applications can be running on the same or different client hosts.
        - 'Constant'     If the user jdoe logs on to Teamcenter using two or more client applications using a constant
        or fixed sessionDiscriminator argument (for example, jdoe/MyApp ), those clients are assigned to the same
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
        - 128001: The logon was refused due to conflict with the encoding of the database instance.
        
        """
        return cls.execute_soa_method(
            method_name='loginSSO',
            library='Core',
            service_date='2008_06',
            service_name='Session',
            params={'username': username, 'ssoCredentials': ssoCredentials, 'group': group, 'role': role, 'locale': locale, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )

    @classmethod
    def setObjectPropertyPolicy(cls, policy: ObjectPropertyPolicy) -> str:
        """
        Sets the current object property policy. The business logic of a service operation determines what business
        objects are returned, while the object property policy determines which properties are returned on each
        business object instance.  This allows the client application to determine how much or how little data is
        returned based on how the client application uses those returned business objects. The policy is applied
        uniformly to all service operations. 
        By default, all applications use the Default object property policy, defined on the Teamcenter server
        '$TC_DATA/soa/policies/default.xml.' It is this policy that is applied to all service operation responses until
        the client application changes the policy. Siemens PLM Software strongly recommends that all applications
        change the policy to one applicable to the client early in the session.
        The object property policy will stay in affect for this session until changed by another call to
        'setObjectPRopertyPolicy'. The current policy can be modified with calls to 'updatObjectPropertyPolicy'.
        
        Like any other service operation, this operation cannot be called before establishing a session with the
        'login' serivce operation, so if you need a policy other than the Default policy for the business objects
        returned by the 'login' operation, use the _2011_06 version of the' login/loginSso' operation to authenticate
        and establish a session without returning business objects. The 'setObjectPropertyPolicy' operation can then be
        called to establish the policy for the session.
        """
        return cls.execute_soa_method(
            method_name='setObjectPropertyPolicy',
            library='Core',
            service_date='2008_06',
            service_name='Session',
            params={'policy': policy},
            response_cls=str,
        )

    @classmethod
    def getDisplayStrings(cls, info: List[str]) -> GetDisplayStringsResponse:
        """
        Get the localized text string for each input key from the info array. The input key must correspond to a key
        defined in the Text Server. If the input array is empty, the returned array will also be empty.
        """
        return cls.execute_soa_method(
            method_name='getDisplayStrings',
            library='Core',
            service_date='2008_06',
            service_name='Session',
            params={'info': info},
            response_cls=GetDisplayStringsResponse,
        )


class ReservationService(TcService):

    @classmethod
    def transferCheckout(cls, objects: List[BusinessObject], userId: User) -> ServiceData:
        """
        This operation transfers the previously checked-out business objects to the user given from input. This
        operation takes care of all complex business logic involved in transfer checked-out based on passed in objects.
        Each input object is verified that it is valid for transferring its checkout. 
        This operation validates precondition defined per type in COTS object and site customization before performing
        transfer checked-out objects to the target user. Dataset, ItemRevision and many other business object types
        have their own business logic for transfer check-out. This operation calls underlying transfer checkout method
        of those individual objects.
        """
        return cls.execute_soa_method(
            method_name='transferCheckout',
            library='Core',
            service_date='2008_06',
            service_name='Reservation',
            params={'objects': objects, 'userId': userId},
            response_cls=ServiceData,
        )


class DispatcherManagementService(TcService):

    @classmethod
    def createDispatcherRequest(cls, inputs: List[CreateDispatcherRequestArgs]) -> CreateDispatcherRequestResponse:
        """
        Create a DispatcherRequest within Teamcenter for use with Dispatcher Management Services.
        
        Use cases:
        The Dispatcher Management application provides the ability to process requests in an asynchronous fashion thus
        removing the processing burden from the clients to provisioned machine dedicated to processing these requests. 
        There are quite a few services, within Teamcenter and other applications that use this application.
        
        Here are a few examples:
        - Asynchronous Processing (if configured)
        - NXtoPVDirect (provided with NX)
        - PreviewService
        
        """
        return cls.execute_soa_method(
            method_name='createDispatcherRequest',
            library='Core',
            service_date='2008_06',
            service_name='DispatcherManagement',
            params={'inputs': inputs},
            response_cls=CreateDispatcherRequestResponse,
        )


class PropDescriptorService(TcService):

    @classmethod
    def getCreateDesc(cls, businessObjectTypeNames: List[str]) -> CreateDescResponse:
        """
        The operation returns information required to create a Business Object. The Create Descriptor (CreateDesc
        object) includes the metadata information for the properties required when creating a business object  i.e,
        property is mandatory, property is visible, etc. The CreateDesc is a recursive data structure. The CreateDesc
        object can also reference CreateDesc on secondary objects through a reference or relation property. For
        example, the CreateDesc for Item points to CreateDesc on its related secondary objects, ItemRevison and Item
        Master. The CreateDesc for ItemRevision in turn points to the CreateDesc for ItemRevision Master.
        
        NOTE:  The operation will be deprecated as of Teamcenter 10. All the metadata information necessary for the
        Create operation can be retrieved from the SOA client metamodel.
        
        
        Use cases:
        Get Create Descriptor information for the Create wizard for an object.
        This call is made to populate the Create dialog for any Business Object. After obtaining the user input on the
        fields of the create dialog, a call is made to the
        'Teamcenter::Soa::Core::_2008_06::DataManagement::createObjects' operation to create the object
        """
        return cls.execute_soa_method(
            method_name='getCreateDesc',
            library='Core',
            service_date='2008_06',
            service_name='PropDescriptor',
            params={'businessObjectTypeNames': businessObjectTypeNames},
            response_cls=CreateDescResponse,
        )


class ManagedRelationsService(TcService):

    @classmethod
    def getManagedRelations(cls, inputdata: GetManagedRelationInput) -> GetManagedRelationResponse:
        """
        This operation will return tracelinks between primary and secondary objects
        """
        return cls.execute_soa_method(
            method_name='getManagedRelations',
            library='Core',
            service_date='2008_06',
            service_name='ManagedRelations',
            params={'inputdata': inputdata},
            response_cls=GetManagedRelationResponse,
        )
