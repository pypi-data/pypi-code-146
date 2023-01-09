from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # NOQA
from push_notifications.gcm import GCMDevice
from swapper import load_model

from .signals import bulk_notify, firebase_push_notify

User = get_user_model()


class NotificationPreference(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notice_preferences",
        verbose_name=_("User"),
    )

    # Notification settings
    article_notification = models.BooleanField(
        default=True,
        verbose_name=_("Article Notice"),
        help_text=_("Receive article notification"),
    )

    class Meta:
        verbose_name = _("Notification Preference")
        verbose_name_plural = _("Notification Preferences")

    def __str__(self):
        return f"{self.user}"


class Broadcast(models.Model):
    recipient = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="notification_messages",
        verbose_name=_("User"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
        null=True,
        blank=True,
    )
    # image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name="+",
    #     verbose_name=_("image"),
    #     help_text=_("Make sure your image size atleast 1366x768px and 72 DPI resolution."),
    # )
    message = models.TextField(
        verbose_name=_("Message"),
        null=True,
        blank=True,
    )
    action_url = models.URLField(
        verbose_name=_("Action URL"),
    )
    action_title = models.CharField(
        max_length=255,
        verbose_name=_("Action Title"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("created at"),
    )
    last_sent_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("last sent"),
    )
    sent_counter = models.IntegerField(
        default=0,
        verbose_name=_("Counter"),
    )

    class Meta:
        verbose_name = _("Broadcast")
        verbose_name_plural = _("Broadcasts")

    def __str__(self):
        return f"{self.title}"

    def send(self, actor, **kwargs):
        recipients = self.get_recipients()

        # get dictionary extra data
        data = self.get_data()
        data.update(kwargs)

        # Send web notification
        try:
            bulk_notify.send(
                self, actor=actor, verb="broadcast", recipients=recipients, **data
            )
            self.sent_counter += 1
            self.last_sent_at = timezone.now()
            self.save()

            # send push notifications
            firebase_push_notify.send(
                self,
                recipients=recipients,
                title=self.title,
                message=self.message,
                data=data,
            )
        except Exception as err:
            print(err)

    def get_title(self):
        return self.title

    def get_message(self):
        return self.message

    def get_data(self):
        data = {
            "type": "broadcast",
            "title": self.title,
            "message": self.message,
            "actions": {
                "url": self.action_url,
                "title": self.action_title,
            },
        }
        if self.image is not None:
            data["image"] = {
                "url": self.image.file.url,
                "width": self.image.width,
                "height": self.image.height,
            }
        return data

    def get_recipients(self):
        if self.recipient is None:
            return User.objects.filter(is_active=True)
        else:
            return self.recipient.user_set.filter(is_active=True)


def bulk_notification_handler(verb, **kwargs):
    """
    Handler function to bulk create Notification instance upon action signal call.
    """

    EXTRA_DATA = True

    # Pull the options out of kwargs
    kwargs.pop("signal", None)
    recipient = kwargs.pop("recipients")
    actor = kwargs.pop("actor")
    optional_objs = [
        (kwargs.pop(opt, None), opt) for opt in ("target", "action_object")
    ]
    public = bool(kwargs.pop("public", True))
    description = kwargs.pop("description", None)
    timestamp = kwargs.pop("timestamp", timezone.now())
    Notification = load_model("notifications", "Notification")
    level = kwargs.pop("level", Notification.LEVELS.info)

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    for recipient in recipients:
        newnotify = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(actor),
            actor_object_id=actor.pk,
            verb=str(verb),
            public=public,
            description=description,
            timestamp=timestamp,
            level=level,
        )

        # Set optional objects
        for obj, opt in optional_objs:
            if obj is not None:
                setattr(newnotify, "%s_object_id" % opt, obj.pk)
                setattr(
                    newnotify,
                    "%s_content_type" % opt,
                    ContentType.objects.get_for_model(obj),
                )

        if kwargs and EXTRA_DATA:
            newnotify.data = kwargs
        new_notifications.append(newnotify)

    new_notifications = Notification.objects.bulk_create(new_notifications)
    return new_notifications


def firebase_notification_handler(recipients, title, message, **kwargs):
    kwargs.pop("signal", None)
    # recipients = kwargs.pop("recipients")
    # title = kwargs.pop("title")
    # message = kwargs.pop("message")
    recipient_ids = [user.id for user in recipients]
    gcm_devices = GCMDevice.objects.filter(user_id__in=recipient_ids, active=True)

    try:
        gcm_devices.send_message(message, title=title, payload=kwargs)
    except Exception as err:
        print(err)


# connect the signal
bulk_notify.connect(
    bulk_notification_handler, dispatch_uid="notifications.models.notification"
)
firebase_push_notify.connect(
    firebase_notification_handler, dispatch_uid="push_notification.gcm.firebase"
)
