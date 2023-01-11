from __future__ import annotations

from tcsoa.gen.Internal.Core._2017_11.LogicalObject import LogicalObjectTypeResponse, LogicalObjectTypeInput, AddMembersPresentedPropsInput, DeleteMembersPresentedPropsInput, AddMemberAndPresentedPropsResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Core._2017_11.Type import GetSubTypeHierarchicalTreeInput, GetSubTypeHierarchicalTreeResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Internal.Core._2017_11.DataManagement import TCSessionAndAnalyticsInfo
from tcsoa.base import TcService


class TypeService(TcService):

    @classmethod
    def getSubTypeHierarchicalTrees(cls, givenTypes: List[GetSubTypeHierarchicalTreeInput]) -> GetSubTypeHierarchicalTreeResponse:
        """
        This operation returns hierarchical tree structures of sub types for given types.
        """
        return cls.execute_soa_method(
            method_name='getSubTypeHierarchicalTrees',
            library='Internal-Core',
            service_date='2017_11',
            service_name='Type',
            params={'givenTypes': givenTypes},
            response_cls=GetSubTypeHierarchicalTreeResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def getTCSessionAnalyticsInfo(cls, extraInfoIn: List[str]) -> TCSessionAndAnalyticsInfo:
        """
        This operation provides information about the current user&rsquo;s Teamcenter session and data required for
        Teamcenter Software Analytics processing.
        
        Use cases:
        After the user logs into Active Workspace this operation is invoked by the Teamcenter client to get information
        related to the user session like Groups, Projects, the Teamcenter Server version, platform type,License type,
        preference related to the time interval and product excellence agreement as required by analytics.
        """
        return cls.execute_soa_method(
            method_name='getTCSessionAnalyticsInfo',
            library='Internal-Core',
            service_date='2017_11',
            service_name='DataManagement',
            params={'extraInfoIn': extraInfoIn},
            response_cls=TCSessionAndAnalyticsInfo,
        )


class LogicalObjectService(TcService):

    @classmethod
    def addMembersAndPresentedProps(cls, addMembersAndPresentedProps: AddMembersPresentedPropsInput) -> AddMemberAndPresentedPropsResponse:
        """
        This operation adds a list of members and presented properties to an existing Logical Object type based on the
        specified input.
        
        Use cases:
        This operation is invoked to add members and presented properties to an already defined logical object type
        based on input values.
        """
        return cls.execute_soa_method(
            method_name='addMembersAndPresentedProps',
            library='Internal-Core',
            service_date='2017_11',
            service_name='LogicalObject',
            params={'addMembersAndPresentedProps': addMembersAndPresentedProps},
            response_cls=AddMemberAndPresentedPropsResponse,
        )

    @classmethod
    def createLogicalObjectTypes(cls, logicalObjectTypeInputs: List[LogicalObjectTypeInput]) -> LogicalObjectTypeResponse:
        """
        This operation creates a list of logical object types based on the specified input. The name, display name,
        description and root type are the mandatory fields required to create a logical object type. A logical object
        type is created only if its definition data satisfies the pre-defined constraints.
        
        Use cases:
        This operation is invoked to create logical object types after obtaining the user input fields from the logical
        object creation dialog.
        
        Use Case 1:
        The user wants to create a logical object type with a root business object and without member and presented
        properties.
        
        In this case the input structure to create a logical object type would look like the following
        
        LogicalObjectTypeInput = {
        name                = loName;
        displayName   = logicalObjectName;
        description      = Logical Object Type;
        rootType          = Item;
        parentType      = Fnd0LogicalObject;
        }
        
        Use Case 2:
        The user wants to create a logical object type with root business object, member and presented properties as
        below
        
        1.  root business object    :   Item
        2.  member object            :   ItemRevision
        3.  presented properties   :   item_revision_id and item_id.
        
        
        In this case the input structures to create a logical object type with member and presented property
        definitions would look like the following
        
        LogicalObjectTypeInput = {
        name                                             = loName;
        displayName                                = logicalObjectName;
        description                                   = Logical Object Type;
        rootType                                       = Item;
        parentType                                   = Fnd0LogicalObject;
        memberPropertyDefinitions      = exampleMemberPropertyDefinitions;
        presentedPropertyDefinitions    = examplePresentedPropertyDefinitions;
        }
        
        exampleMemberPropertyDefinitions[0] = {
        memberPropertyName     = itemRevisionMember;
        displayName                       = Item Revision;
        description                          = Item Revision members;
        traversalPath                       = exampleTraversalPaths;
        }
        
        exampleTraversalPaths [0] = {
        propertyName       = fnd0Root
        propertyType         = refrence
        destinationType     = Item
        direction                  = forward
        }
        exampleTraversalPaths [1] = {
        propertyName        = items_tag
        propertyType          = reference
        destinationType     = ItemRevision
        direction                  = reverse
        }
        
        examplePresentedPropertyDefinitions[0] = {
        presentedPropertyName = ItemRevisionId;
        displayName                     = ItemRevisionId;
        description                        = Presented property from member: ItemRevissionId;
        rootOrMemberName      = itemRevisionMember;
        sourcePropertyName      = item_revision_id;
        }
        examplePresentedPropertyDefinitions[1] = {
        presentedPropertyName   = ItemId;
        displayName                       = ItemId;
        description                          = Presented property from root: ItemId;
        rootOrMemberName        = fnd0Root;
        sourcePropertyName        = item_id;
        }
        """
        return cls.execute_soa_method(
            method_name='createLogicalObjectTypes',
            library='Internal-Core',
            service_date='2017_11',
            service_name='LogicalObject',
            params={'logicalObjectTypeInputs': logicalObjectTypeInputs},
            response_cls=LogicalObjectTypeResponse,
        )

    @classmethod
    def deleteLogicalObjectTypes(cls, logicalObjects: List[BusinessObject]) -> ServiceData:
        """
        This operation deletes a list of logical object definitions and its member and presented property definitions.
        """
        return cls.execute_soa_method(
            method_name='deleteLogicalObjectTypes',
            library='Internal-Core',
            service_date='2017_11',
            service_name='LogicalObject',
            params={'logicalObjects': logicalObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteMembersAndPresentedProps(cls, deleteMembersAndPresentedProps: List[DeleteMembersPresentedPropsInput]) -> ServiceData:
        """
        This operation deletes a list of logical object member definitions and/or a list of logical object presented
        property definitions or a list of included logical object definitions. When a logical object member is deleted
        all presented properties that are from this member are also implicitly deleted.
        """
        return cls.execute_soa_method(
            method_name='deleteMembersAndPresentedProps',
            library='Internal-Core',
            service_date='2017_11',
            service_name='LogicalObject',
            params={'deleteMembersAndPresentedProps': deleteMembersAndPresentedProps},
            response_cls=ServiceData,
        )
