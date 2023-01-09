from django.conf import settings
from django.db import models
from djangoldp.models import Model


class Tag(Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='tags',
                                null=True,
                                on_delete=models.SET_NULL
                                )
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=16)

    class Meta(Model.Meta):
        rdf_type = 'hd:tag'
        authenticated_perms = ['add']
        owner_field = 'creator'
        owner_perms = ['view']
