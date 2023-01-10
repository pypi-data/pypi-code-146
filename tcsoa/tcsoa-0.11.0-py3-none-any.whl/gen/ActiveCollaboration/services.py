from tcsoa.gen.ActiveCollaboration._2020_12.services import ActiveCollaborationService as imp0
from tcsoa.base import TcService


class ActiveCollaborationService(TcService):
    createOrUpdateComment = imp0.createOrUpdateComment
    createOrUpdateConversation = imp0.createOrUpdateConversation
    deleteComment = imp0.deleteComment
    deleteConversation = imp0.deleteConversation
    getReadInfo = imp0.getReadInfo
    manageSubscriptions = imp0.manageSubscriptions
