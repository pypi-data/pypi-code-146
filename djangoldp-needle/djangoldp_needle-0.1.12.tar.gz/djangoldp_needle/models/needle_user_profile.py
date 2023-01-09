from django.conf import settings
from django.db import models
from djangoldp.models import Model


class NeedleUserProfile(Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='needle_user_profiles',
                                null=True,
                                on_delete=models.CASCADE
                                )

    activity_crossed_yarn_last_date = models.DateTimeField(auto_now_add=True)
    activity_followed_yarn_last_date = models.DateTimeField(auto_now_add=True)
    activity_pads_last_date = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=16)

    class Meta(Model.Meta):
        rdf_type = 'hd:user_profile'
        owner_field = 'creator'
        owner_perms = ['view', 'change']
