from django.conf import settings
from django.db import models
from djangoldp.models import Model

ACTIVITY_TYPE_NEW_USER = "ACTIVITY_TYPE_NEW_USER";
ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS = "ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS";
ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS = "ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS";


class NeedleActivity(Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='needle_activities',
                                null=True,
                                on_delete=models.CASCADE
                                )
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=1024, default="")
    content = models.TextField(max_length=4096)
    activity_type = models.TextField(max_length=255, default="")
    read = models.BooleanField(default=False)

    class Meta(Model.Meta):
        rdf_type = 'hd:activity'
        owner_field = 'creator'
        owner_perms = ['view', 'change']
