from django.conf import settings
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import StringPreference

from aleksis.core.registries import site_preferences_registry

paweljong = Section("paweljong", verbose_name=_("Paweljong"))


@site_preferences_registry.register
class EventNotificationRecipient(StringPreference):
    """Mail recipient for event nofications (e.g. registrations)."""

    section = paweljong
    name = "event_notification_recipient"
    default = settings.ADMINS[0][1]
    verbose_name = _("Mail recipient for event notifications")
    field_class = EmailField
    required = True
