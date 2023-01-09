from django.conf import settings
from django.db import models
from djangoldp.models import Model
from .annotation_target import AnnotationTarget
from . import Tag

class Annotation(Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='yarn',
                                null=True,
                               on_delete=models.SET_NULL
                                )
    creation_date = models.DateTimeField(auto_now_add=True)
    target = models.ForeignKey(AnnotationTarget, null=True, on_delete=models.SET_NULL, related_name='annotations')
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField(null=True)

    class Meta(Model.Meta):
        rdf_type = 'hd:annotation'
        #rdf_context = 'https://www.w3.org/ns/anno.jsonld'
        authenticated_perms = ['add', 'view']
        auto_author = 'creator'
        owner_field = 'creator'
        owner_perms = ['view', 'delete']
