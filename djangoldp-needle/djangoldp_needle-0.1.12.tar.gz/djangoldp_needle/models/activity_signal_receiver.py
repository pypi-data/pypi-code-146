from django.db import models
from djangoldp.models import Model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from ..views.needle_activity import create_welcome_needle_activity
from ..views.annotation import create_first_annotation_activity_annotation_with_connections, \
    create_first_annotation_activity_annotation_without_connections, \
    create_first_annotation_activity_first_annotation_with_connections, \
    create_first_annotation_activity_first_annotation_without_connections

from ..models.annotation import Annotation
from ..models.annotation_target import AnnotationTarget
from ..models.needle_activity import NeedleActivity, ACTIVITY_TYPE_NEW_USER, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, instance, created, **kwargs):
    # print("UPDATE USER: {0} with id {1}".format(instance, instance.pk))
    if created and not Model.is_external(instance):
        # print("NEW USER: {0} with id {1}".format(instance, instance.pk))
        create_welcome_needle_activity(instance);


@receiver(post_save, sender=Annotation)
def post_save_annotation(sender, instance, created, **kwargs):
    # print("UPDATE ANNOTATION: {0} with id {1}".format(instance, instance.pk))
    if created and not Model.is_external(instance):
        # print("NEW ANNOTATION: {0} with id {1}".format(instance, instance.pk))
        # retourne les annotation avec la même target
        result_annotation_same_target = Annotation.objects.filter(target=instance.target)
        # retourne les annotations du même utilisateur
        result_annotation_current_user = Annotation.objects.filter(creator=instance.creator)
        # Première annotation ?
        if result_annotation_current_user.count() == 1:
            # Première annotation target ?
            if result_annotation_same_target.count() == 1:
                create_first_annotation_activity_first_annotation_without_connections(instance)
            else:
                create_first_annotation_activity_first_annotation_with_connections(instance)

        else:
            # Première annotation target ?
            if result_annotation_same_target.count() == 1:

                result_needle_activity = \
                    NeedleActivity.objects.filter(creator=instance.creator,
                                                  activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)
                # L'utilisateur a-t'il déjà reçu une notification de ce type ?
                if result_needle_activity.count() == 0:
                    create_first_annotation_activity_annotation_without_connections(instance)
            else:
                result_needle_activity = \
                    NeedleActivity.objects.filter(creator=instance.creator,
                                                  activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)
                # L'utilisateur a-t'il déjà reçu une notification de ce type ?
                if result_needle_activity.count() == 0:
                    create_first_annotation_activity_annotation_with_connections(instance)


@receiver(post_save, sender=AnnotationTarget)
def post_save_annotation_target(sender, instance, created, **kwargs):
    pass
    # print("UPDATE ANNOTATION TARGET: {0} with id {1}".format(instance, instance.pk))
    # if created and not Model.is_external(instance):
    #     print("NEW ANNOTATION TARGET: {0} with id {1}".format(instance, instance.pk))
