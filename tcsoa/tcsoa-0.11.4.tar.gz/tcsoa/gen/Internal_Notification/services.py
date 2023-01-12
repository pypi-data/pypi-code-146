from tcsoa.gen.Internal_Notification._2015_10.services import SubscriptionManagementService as imp0
from tcsoa.gen.Internal_Notification._2015_03.services import SubscriptionManagementService as imp1
from tcsoa.gen.Internal_Notification._2017_11.services import SubscriptionManagementService as imp2
from tcsoa.gen.Internal_Notification._2014_10.services import SubscriptionManagementService as imp3
from tcsoa.gen.Internal_Notification._2015_10.services import MessageManagementService as imp4
from tcsoa.gen.Internal_Notification._2015_03.services import MessageManagementService as imp5
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):
    createSubscriptionTemplates = imp0.createSubscriptionTemplates
    createSubscriptions = imp1.createSubscriptions
    findSubscriptions = imp1.findSubscriptions
    getApplicableSubscriptionTemplates = imp0.getApplicableSubscriptionTemplates
    getAssignEventData = imp1.getAssignEventData
    getAttachEventData = imp1.getAttachEventData
    getAttachEventData2 = imp0.getAttachEventData2
    getEventTypes2 = imp1.getEventTypes2
    getSubscribableProperties = imp2.getSubscribableProperties
    getSubscribableTypes = imp1.getSubscribableTypes
    getSubscriptionConditions = imp3.getSubscriptionConditions
    getSubscriptionInput = imp1.getSubscriptionInput
    modifySubscriptionTemplates = imp0.modifySubscriptionTemplates
    modifySubscriptions = imp1.modifySubscriptions
    saveAsSubscription = imp0.saveAsSubscription
    transferNotifications = imp1.transferNotifications
    unsubscribe = imp0.unsubscribe


class MessageManagementService(TcService):
    getUnreadMessages = imp4.getUnreadMessages
    getUserGroupAlias = imp5.getUserGroupAlias
    initializeAsynchMessaging = imp4.initializeAsynchMessaging
