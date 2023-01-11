from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from drf_extra_utils.middleware import get_current_user


class TimeStampedBase(models.Model):
    """
    An abstract base model class that provides fields for keeping track of when the object was created and last modified.
    """

    created = models.DateTimeField(
        _("Creation Date and Time"),
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        _("Modification Date and Time"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class CreatorBase(models.Model):
    """
    CreatorBase is an abstract Model class that represents a model with a creator field. The creator field is a foreign
    key to the AUTH_USER_MODEL specified in Django's settings, and is used to store the user who created the object.
    """

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("creator"),
        editable=False,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if not self.creator:
            self.creator = get_current_user()
        super().save(*args, **kwargs)

    save.alters_data = True
