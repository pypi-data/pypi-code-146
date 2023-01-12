from django.db import models
from psu_base.classes.Log import Log
from django.urls import reverse

log = Log()


class EndpointDefinition(models.Model):
    """Endpoints that can be called on a schedule"""

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    app_code = models.CharField(
        max_length=15,
        blank=False, null=False, db_index=True
    )
    title = models.CharField(
        max_length=80,
        blank=False, null=False
    )
    endpoint = models.CharField(
        max_length=200,
        blank=False, null=False
    )

    def url(self):
        return reverse(self.endpoint)

    @classmethod
    def get(cls, cls_id):
        try:
            return cls.objects.get(pk=cls_id)
        except cls.DoesNotExist:
            return None
