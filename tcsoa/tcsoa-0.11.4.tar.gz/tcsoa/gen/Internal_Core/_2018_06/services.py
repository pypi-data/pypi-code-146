from __future__ import annotations

from tcsoa.gen.Internal.Core._2017_11.LogicalObject import LogicalObjectTypeResponse, AddMemberAndPresentedPropsResponse
from tcsoa.gen.Internal.Core._2018_06.LogicalObject import UpdateMemberInput, LogicalObjectTypeInput2, AddMembersPresentedPropsInput2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class LogicalObjectService(TcService):

    @classmethod
    def updateMembers(cls, updateMemberInputStruct: UpdateMemberInput) -> ServiceData:
        """
        This operation updates a list of logical object member definitions based on the specified input.
        
        Use cases:
        This operation is invoked to update member definitions to an already defined logical object type based on input
        values.
        
        Use Case: 
        
        For example, consider the below use case data for the use case(s) specified: 
        
        Use Case Data:
        Logical object definition 1
        Name                               : "Logical Object 1"
        Root business object   : Item
        
        Member : MemberRevision
        {
            Member ID      : MemberRevision
            Display Name : Revision Member
            Retrieve Classification Data : False
            Navigation Path : vector<TraversalHop2>:REF(fnd0Root, Item).REFBY(items_tag, ItemRevision)
        }
        
        
        Use Case 1: 
        Update member name
        
        UpdateMemberInput
        {
            logicalObjectType = "Logical Object 1"
            membersToBeUpdated = {  < "MemberRevision"
                                                                  MemberPropertyDefinition2
                                                                  { 
                                                                         Member ID : MemberRevision_update
                                                                         Display Name: 
                                                                         Retrieve Classification Data : false
                                                                         Navigation Path:
                                                                  }
                                                             >   
                                                         }                            
        }                                
        
        SOA will update the name of member "MemberRevision" to "MemberRevision_update".
        
        
        Use Case 2: 
        Update member display name and Retrieve classification Data flag
        
        UpdateMemberInput
        {
            logicalObjectType = "Logical Object 1"
            membersToBeUpdated = {  < "MemberRevision"
                                                                  MemberPropertyDefinition2
                                                                  { 
                                                                         Member ID : MemberRevision
                                                                         Display Name: Revision Member update
                                                                         Retrieve Classification Data : true
                                                                         Navigation Path:
                                                                  }
                                                             >   
                                                         }                            
        }                                
        
        SOA will update the display name of member from "Revision Member" to "Revision member update" and update
        retrieve classification data flag to true.
        
        Use Case 3: 
        Update member navigation path
        
        UpdateMemberInput
        {
            logicalObjectType = "Logical Object 1"
            membersToBeUpdated = {  < "MemberRevision"
                                                                  MemberPropertyDefinition2
                                                                  { 
                                                                         Member ID : MemberRevision
                                                                         Display Name: Revision Member update
                                                                         Retrieve Classification Data : false
                                                                         Navigation Path: vector<TraversalHop2>
                                                                  }
                                                             >   
                                                         }                            
        }                                
        
        TraversalHop2[0]
        {
           propertyName = "fnd0Root"
           direction           = "forward"
           destinationType  = "Item"
           propertyType      = ""
           destinationObjectCriteria = ""
        }
        
        TraversalHop2[1]
        {
           propertyName = "IMAN_reference"
           direction  ="forward"
           destinationType  = "Part"
           propertyType     = ""
          destinationObjectCriteria = ""
        } 
        
        SOA will update the navigation path of the member "MemberRevision" to reflect new navigation path.
        
        Use Case 4: 
        Update destinationObjectCriteria of the member navigation path
        
        UpdateMemberInput
        {
            logicalObjectType = "Logical Object 1"
            membersToBeUpdated = {  < "MemberRevision"
                                                                  MemberPropertyDefinition2
                                                                  { 
                                                                         Member ID : MemberRevision
                                                                         Display Name: Revision Member update
                                                                         Retrieve Classification Data : false
                                                                         Navigation Path: vector<TraversalHop2>
                                                                  }
                                                             >   
                                                         }                            
        }                                
        
        TraversalHop2[0]
        {
           propertyName = "IMAN_reference"
           direction           = "forward"
           destinationType  = "ItemRevision"
           propertyType      = "relation"
           destinationObjectCriteria = "$ConfigurationContext"
        }
        
        SOA will update the navigation path of the member "MemberRevision" to reflect new navigation path including
        updated destinationObjectCriteria. Other possible values for destinationObjectCriteria include
        $ConfigurationContext = puid1, and $CurrentUserSessionProject.
        """
        return cls.execute_soa_method(
            method_name='updateMembers',
            library='Internal-Core',
            service_date='2018_06',
            service_name='LogicalObject',
            params={'updateMemberInputStruct': updateMemberInputStruct},
            response_cls=ServiceData,
        )

    @classmethod
    def addMembersAndPresentedProps2(cls, addMembersAndPresentedProps: AddMembersPresentedPropsInput2) -> AddMemberAndPresentedPropsResponse:
        """
        This operation adds a list of members with the capability to select a filter criteria on the destination object
        and presented properties to an existing Logical Object Type based on the specified input. 
        A Logical Object Type is a sub-type of Fnd0LogicalObject.
        
        Use cases:
        This operation is invoked to add members and presented properties to an existing Logical Object Type.
        Configuration Context can optionally be added to the Traversal Hop structure for filtering during Logical
        Object retrieval.
        
        Use Case 1: 
        The user wants to add a member to a Logical Object Type (subtype of Fnd0LogicalObject)  with default
        Configuration Context criteria specified.
        Note the input value for destinationObjectCriteria  must be the selected value from Dynamic Filter Criteria LOV.
        
        TraversalHop2 = {
            propertyName            = IMAN_reference; 
        propertyType            = relation;
        destinationType            = ItemRevision; 
        direction            = forward; 
        destinationObjectCriteria    = $ConfigurationContext; 
        }
        
        Use Case 2: 
        The user wants to add a member to a Logical Object Type (subtype of Fnd0LogicalObject)  with a specific
        Configuration Context criteria specified.
        
        TraversalHop2 = {
            propertyName            = IMAN_reference; 
        propertyType            = relation;
        destinationType            = ItemRevision; 
        direction            = forward; 
        destinationObjectCriteria    = $ConfigurationContext = puid1; 
        }
        
        Use Case 3: 
        The user wants to add a member to a Logical Object Type (subtype of Fnd0LogicalObject)  with the Current User
        Session Project criteria specified.
        
        TraversalHop2 = {
            propertyName            = IMAN_reference; 
        propertyType            = relation;
        destinationType            = Item; 
        direction            = forward; 
        destinationObjectCriteria    = $CurrentUserSessionProject; 
        }
        
        Use Case 4: 
        The user wants to add a member to a Logical Object Type (subtype of Fnd0LogicalObject)  with default
        Configuration Context and the Current User Session Project criteria specified.
        
        TraversalHop2 = {
            propertyName            = IMAN_reference; 
        propertyType            = relation;
        destinationType            = Item; 
        direction            = forward; 
        destinationObjectCriteria    = $CurrentUserSessionProject  and   
           $ConfigurationContext; 
        }
        """
        return cls.execute_soa_method(
            method_name='addMembersAndPresentedProps2',
            library='Internal-Core',
            service_date='2018_06',
            service_name='LogicalObject',
            params={'addMembersAndPresentedProps': addMembersAndPresentedProps},
            response_cls=AddMemberAndPresentedPropsResponse,
        )

    @classmethod
    def createLogicalObjectTypes2(cls, logicalObjectTypeInputs: List[LogicalObjectTypeInput2]) -> LogicalObjectTypeResponse:
        """
        This operation creates a list of Logical Object Types (subtypes of Fnd0LogicalObject) based on the specified
        input. The name, display name, description and root type are the mandatory fields required to create a Logical
        Object Type. This operation has the capabiltiy to add a list of members and to select a filter criteria on the
        destination object and presented properties to an existing Logical Object Type.
        A Logical Object Type is created only if its definition data satisfies the pre-defined constraints.
        
        Use cases:
        This operation is invoked to create Logical Object Types (subtypes of Fnd0LogicalObject)  after obtaining the
        user input fields from the logical object creation dialog.
        
        Use Case 1: 
        The user wants to create a Logical Object Type(subtype of Fnd0LogicalObject)  with a root business object and
        without member and presented properties. In this case the input structure to create a Logical Object Type would
        look like the following
        LogicalObjectTypeInput = {
        name = loName; 
        displayName = logicalObjectName;
        description = Logical Object Type; 
        rootType = Item; 
        parentType = Fnd0LogicalObject;
        }
        Use Case 2: 
        The user wants to create a Logical Object Type with root business object, member and presented properties as
        below
        1.root business object : Item 
        2.member object: ItemRevision 
        3.presented properties : item_revision_id and item_id. 
        In this case the input structures to create a Logical Object Type with member and presented property
        definitions would look like the following
        LogicalObjectTypeInput2 = {
        name = loName; 
        displayName= logicalObjectName;
        description = Logical Object Type; 
        rootType = Item; 
        parentType = Fnd0LogicalObject; 
        memberPropertyDefinitions = exampleMemberPropertyDefinitions;
        presentedPropertyDefinitions = examplePresentedPropertyDefinitions;
        }
        exampleMemberPropertyDefinitions[0] = {
        memberPropertyName = itemRevisionMember;
        displayName= Item Revision;
        description= Item Revision members;
        traversalPath = exampleTraversalPaths;
        }
        exampleTraversalPaths [0] = {
        propertyName = fnd0Root
        propertyType = refrence
        destinationType = Item
        direction = forward
        destinationObjectCriteria = USER
        }
        exampleTraversalPaths [1] = {
        propertyName = items_tag
        propertyType = reference
        destinationType = ItemRevision
        direction = reverse
        destinationObjectCriteria = 
        }
        examplePresentedPropertyDefinitions[0] = {
        presentedPropertyName = ItemRevisionId; 
        displayName = ItemRevisionId; 
        description = Presented property from member: ItemRevissionId; 
        rootOrMemberName = itemRevisionMember;
        sourcePropertyName = item_revision_id;
        }
        examplePresentedPropertyDefinitions[1] = {
        presentedPropertyName = ItemId; 
        displayName = ItemId; 
        description = Presented property from root: ItemId; 
        rootOrMemberName = fnd0Root;
        sourcePropertyName = item_id;
        """
        return cls.execute_soa_method(
            method_name='createLogicalObjectTypes2',
            library='Internal-Core',
            service_date='2018_06',
            service_name='LogicalObject',
            params={'logicalObjectTypeInputs': logicalObjectTypeInputs},
            response_cls=LogicalObjectTypeResponse,
        )
