from __future__ import annotations

from tcsoa.gen.ProjectManagement._2007_06.ScheduleManagement import ScheduleCopyOptionsContainer, TaskDeliverableContainer, DeleteNotificationRuleContainer, NotificationRulesList, GetNotificationRuleContainer, NotificationRuleContainer, MultiScheduleCopyResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def copySchedules(cls, scheduleCopyContainer: List[ScheduleCopyOptionsContainer]) -> MultiScheduleCopyResponse:
        """
        Makes a deep copy of the schedule with options to reset work and copy existing baselines.
        """
        return cls.execute_soa_method(
            method_name='copySchedules',
            library='ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'scheduleCopyContainer': scheduleCopyContainer},
            response_cls=MultiScheduleCopyResponse,
        )

    @classmethod
    def createOrUpdateNotificationRules(cls, notificationsContainers: List[NotificationRuleContainer]) -> ServiceData:
        """
        Creates a list of notification rules for Schedule or ScheduleTask based on the notifications container. You use
        notifications to notify individuals, including yourself, of important events associated with selected objects.
        Notifications utilize Teamcenter mail and the Subscription Manager. To receive notifications and subscriptions,
        a system administrator must set the value of the Mail_server_name preference to a name of a valid mail server
        (this task needs only to be performed once). The e-mail address in the Person object for every user that's
        expected to receive a notification.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateNotificationRules',
            library='ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'notificationsContainers': notificationsContainers},
            response_cls=ServiceData,
        )

    @classmethod
    def createTaskDeliverableTemplates(cls, taskDeliverableData: List[TaskDeliverableContainer]) -> ServiceData:
        """
        Creates new task deliverable template and relates them to the task. This is done by going through each
        deliverable, checks if the user has write access on the specified task, and then checking if the task
        deliverable already exists for the task.  If it does not exist it will create an instance of the task
        deliverable and add to the list of task deliverables.
        """
        return cls.execute_soa_method(
            method_name='createTaskDeliverableTemplates',
            library='ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'taskDeliverableData': taskDeliverableData},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteNotificationRules(cls, notificationRuleContainer: List[DeleteNotificationRuleContainer]) -> ServiceData:
        """
        Delete notification rules for Schedule or ScheduleTask based on the contents of the delete notifications
        container. After deleting the notification will rule, the users attached to that rule will not receive any more
        notifications for that specific action.
        """
        return cls.execute_soa_method(
            method_name='deleteNotificationRules',
            library='ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'notificationRuleContainer': notificationRuleContainer},
            response_cls=ServiceData,
        )

    @classmethod
    def getNotificationRules(cls, notificationRuleContainer: List[GetNotificationRuleContainer]) -> NotificationRulesList:
        """
        Get a list of notification rules for Schedule or ScheduleTask based on the notifications container. Use
        notifications to notify individuals, including yourself, of important events associated with selected objects.
        Notifications utilize Teamcenter mail and the Subscription Manager. To receive notifications and subscriptions,
        a system administrator must set the value of the Mail_server_name preference to a name of a valid mail server
        (this task needs only to be performed once). The e-mail address in the Person object for every user that's
        expected to receive a notification.
        """
        return cls.execute_soa_method(
            method_name='getNotificationRules',
            library='ProjectManagement',
            service_date='2007_06',
            service_name='ScheduleManagement',
            params={'notificationRuleContainer': notificationRuleContainer},
            response_cls=NotificationRulesList,
        )
