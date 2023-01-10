from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User, Ac0Comment, Ac0Conversation
from tcsoa.gen.ActiveCollaboration._2020_12.ActiveCollaboration import CreateOrUpdateCommentRequest, CreateOrUpdateConversationRequest, ReadResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ActiveCollaborationService(TcService):

    @classmethod
    def createOrUpdateComment(cls, request: List[CreateOrUpdateCommentRequest]) -> ServiceData:
        """
        This operation creates or updates a comment.
        
        Use cases:
        &bull;    A user replies to a comment in a conversation.
        &bull;    A user updates an existing comment in the conversation
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateComment',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'request': request},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateConversation(cls, request: CreateOrUpdateConversationRequest) -> ServiceData:
        """
        This operation creates or updates a conversation.
        
        Use cases:
        &bull;    A user creates a new public conversation on any Teamcenter object.
        Any user can create or update a conversation.  Conversations are typically created through Active Workspace on
        the conversations panel.  A conversation must have one or more source objects.  A source object can be any
        Teamcenter WorkspaceObject.  
        
        &bull;    A user creates a new private conversation on any Teamcenter object.
        Any user can create or update a conversation.  Conversations are typically created through Active Workspace on
        the conversations panel.  A conversation must have one or more source objects.  A source object can be any
        Teamcenter WorkspaceObject.  Private conversations must contain at least one participant.  A participant is a
        Teamcenter User object.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateConversation',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'request': request},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteComment(cls, objsToDelete: List[Ac0Comment]) -> ServiceData:
        """
        This operation deletes one or more Ac0Comment object(s).
        """
        return cls.execute_soa_method(
            method_name='deleteComment',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'objsToDelete': objsToDelete},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteConversation(cls, objsToDelete: List[Ac0Conversation]) -> ServiceData:
        """
        This operation deletes one or more Ac0Conversation object(s).
        """
        return cls.execute_soa_method(
            method_name='deleteConversation',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'objsToDelete': objsToDelete},
            response_cls=ServiceData,
        )

    @classmethod
    def getReadInfo(cls, users: List[User], objects: List[BusinessObject]) -> ReadResponse:
        """
        Given a list of users and a list of objects, this operation returns the users and objects where the user(s) do
        not have read access to the object(s).
        
        Use cases:
        &bull;    A user creating a conversation needs to know which source objects the given participants do not have
        read access to.  
        
        When creating conversations in Active Workspace, a user can select one or more participants for a conversation
        on one or more source objects.  The user creating the conversation needs to know which participants do not have
        read access to all source objects.   
        
        For each participant that does not have read access to one or more source objects, the operation returns a
        mapping of the participant and the source objects for which that participant does not have read access.    
        
        Using this information, a user creating the conversation can then either know that a participant will not be
        able to see the message they are writing, or they may do what is needed have the permissions changed for the
        participant(s) or the source object(s).
        
        &bull;    A user creating a conversation needs to know which participants do not have read access for the
        source objects on the conversation.
        
        When creating conversations in Active Workspace, a user can select one or more participants for a conversation
        on one or more source objects.  The user creating the conversation needs to know which source objects are not
        readable by all participants.   
        
        For each source object on which any participant does not have read access, the operation returns the source
        object and the participants that do not have read access to that object. 
        
        Using this information, a user creating the conversation can then either know that a participants will not be
        able to see the message they are writing, or they may do what is needed have the permissions changed for the
        participant(s) or the source object(s).
        """
        return cls.execute_soa_method(
            method_name='getReadInfo',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'users': users, 'objects': objects},
            response_cls=ReadResponse,
        )

    @classmethod
    def manageSubscriptions(cls, conversations: List[Ac0Conversation], sourceObjects: List[BusinessObject], subscriptionFlag: bool) -> ServiceData:
        """
        This operation subscribes or unsubscribes the current user to a list of Ac0Conversation or source objects. The
        source objects are expected to be WorkspaceObject type. If user subscribe to an Ac0Conversation object, then
        when new comments are added to the conversation as replies the user will be notified.  If user subscribe to a
        WorkspaceObject, then when new conversations are created for that WorkspaceObject or new comments are added as
        replies to existing Conversations on that WorkspaceObject, the user will be notified.
        
        Use cases:
        &bull;    Follow or Subscribe to a Conversation
        When a user clicks on the "follow" button in an expanded conversation, they will receive notifications when
        replies are made to the conversation.  A conversation is any Ac0Conversation.
        
        &bull;    Unfollow or Unsubscribe to a Conversation
        If a user has subscribed to a conversation by clicking on the Follow button on the Conversation, they will now
        see an "Unfollow" button.  Click the Unfollow button to stop receiving notifications when replies are made to
        the conversation.  A conversation is any Ac0Conversation
        
        &bull;    Follow or Subscribe to Conversations for a source object
        When a user clicks on the "follow" button in the Conversation panel, they will receive notifications for any
        replies to existing conversations, as well as for any new conversations created, where the currently selected
        business object is a source object on the conversation.  A source object can be any Teamcenter WorkspaceObject.
        
        &bull;    Unfollow or Unsubscribe to Conversations for a source object
        If a user has subscribed to conversations for a source object, they will now see an "Unfollow" button next to
        the selected source object in the conversation panel.  Click the "Unfollow" button to stop receiving
        notifications for conversation activity related to the selected source object.  A source object can be any
        Teamcenter WorkspaceObject.
        """
        return cls.execute_soa_method(
            method_name='manageSubscriptions',
            library='ActiveCollaboration',
            service_date='2020_12',
            service_name='ActiveCollaboration',
            params={'conversations': conversations, 'sourceObjects': sourceObjects, 'subscriptionFlag': subscriptionFlag},
            response_cls=ServiceData,
        )
