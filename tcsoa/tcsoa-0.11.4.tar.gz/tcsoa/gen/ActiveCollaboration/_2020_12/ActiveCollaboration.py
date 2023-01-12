from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User, Ac0Comment, Ac0Conversation
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateOrUpdateCommentRequest(TcBaseObj):
    """
    The CreateOrUpdateCommentRequest is a data structure that contains the parameters required for the create or update
    comment request.
    
    :var richText: The original formatted text and content entered by the user using ckeditor.
    :var rootComment: The Ac0Comment  root comment object.  This will be null if it is the first comment on the
    conversation.
    :var comment: The Ac0Comment  object to be updated. This is empty if the comment is being created.
    :var conversation: The Ac0Conversation object this new or updated comment belongs to.
    """
    richText: str = ''
    rootComment: Ac0Comment = None
    comment: Ac0Comment = None
    conversation: Ac0Conversation = None


@dataclass
class CreateOrUpdateConversationRequest(TcBaseObj):
    """
    The CreateOrUpdateConversationRequest is a data structure that contains the parameters required for a create or
    update conversation request.
    
    :var sourceObjects: A list   containing BusinessObject objects  that are the conversation&rsquo;s source objects.  
     A sourceObject can be any WorkspaceObject users want to have a conversation about.
    :var listOfPartipants: A list  containing User objects that are the conversation&rsquo;s participants.  This field
    is null for public conversations. For private conversations this is a mandatory parameter.
    :var defaultCommentText: The original formatted text and content entered by the user using ckeditor.   This field
    contains the text of the initial comment on a conversation.
    :var conversation: The Ac0Conversation object if the conversation is being updated.  This parameter is null when
    the conversation is new.
    """
    sourceObjects: List[BusinessObject] = ()
    listOfPartipants: List[User] = ()
    defaultCommentText: str = ''
    conversation: Ac0Conversation = None


@dataclass
class ReadResponse(TcBaseObj):
    """
    The ReadResponse is a data structure that holds maps containing the requested users and objects where read
    privileges have not been granted.
    
    :var userObjectMap: The map (User, list of BusinessObject) of User entries that correspond to a list of
    WorkspaceObject objects for which the User does not have read permissions.  The map will be empty if all provided
    users have read access to all provided objects.
    :var objectUserMap: The map (BusinessObject, list of User) of WorkspaceObject entries that correspond to a list of
    User objects that do not have read permission for the given WorkspaceObject.
    :var serviceData: The Service Data.
    """
    userObjectMap: UserObjectMap = None
    objectUserMap: ObjectUserMap = None
    serviceData: ServiceData = None


"""
The objectUserMap contains objects and a corresponding list of users that do not have read access to the given object.
"""
ObjectUserMap = Dict[BusinessObject, List[User]]


"""
The userObjectMap contains user objects and a corresponding list of business objects that the given user does not have read access to.
"""
UserObjectMap = Dict[User, List[BusinessObject]]
