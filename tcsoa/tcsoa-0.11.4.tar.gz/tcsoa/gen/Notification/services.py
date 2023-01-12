from tcsoa.gen.Notification._2014_10.services import SubscriptionManagementService as imp0
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):
    createSubscriptions = imp0.createSubscriptions
    findSubscriptions = imp0.findSubscriptions
    getSubscriptions = imp0.getSubscriptions
    modifySubscriptions = imp0.modifySubscriptions
